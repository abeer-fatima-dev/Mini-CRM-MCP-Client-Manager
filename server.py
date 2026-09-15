"""Mini CRM MCP server backed by a local JSON file."""

import json
import re
from pathlib import Path
from typing import Any

from mcp.server import MCPServer


mcp = MCPServer(
    name="Mini-CRM-Client-Manager",
    version="1.0.0",
    description="A beginner-friendly MCP server for managing local CRM client records.",
)

DATA_FILE = Path(__file__).with_name("clients.json")
ALLOWED_STATUSES = {"lead", "active", "inactive"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_clients() -> list[dict[str, Any]]:
    """Load client records, treating a missing or empty file as an empty CRM."""
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("clients.json could not be read as valid JSON.") from exc

    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise RuntimeError("clients.json must contain a JSON array of client objects.")
    return data


def save_clients(clients: list[dict[str, Any]]) -> None:
    """Save client records as readable JSON."""
    try:
        DATA_FILE.write_text(
            json.dumps(clients, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        raise RuntimeError("clients.json could not be saved.") from exc


def find_client(
    clients: list[dict[str, Any]], client_id: int
) -> dict[str, Any] | None:
    """Find a client by its numeric ID."""
    return next((client for client in clients if client.get("id") == client_id), None)


def is_valid_email(email: str) -> bool:
    """Perform a small, beginner-friendly email validation check."""
    return bool(EMAIL_PATTERN.fullmatch(email))


def error_response(message: str) -> dict[str, Any]:
    return {"ok": False, "error": message}


def load_or_error() -> tuple[list[dict[str, Any]] | None, dict[str, Any] | None]:
    try:
        return load_clients(), None
    except RuntimeError as exc:
        return None, error_response(str(exc))


@mcp.tool(description="Add a new client to the local CRM.")
def add_client(
    name: str,
    email: str,
    phone: str = "",
    company: str = "",
    status: str = "lead",
) -> dict[str, Any]:
    """Add a client after validating required fields, status, and email uniqueness."""
    if not isinstance(name, str) or not name.strip():
        return error_response("Name is required and cannot be empty.")
    if not isinstance(email, str) or not email.strip():
        return error_response("Email is required and cannot be empty.")
    if not isinstance(phone, str) or not isinstance(company, str):
        return error_response("Phone and company must be text.")
    if not isinstance(status, str):
        return error_response("Status must be text.")

    normalized_email = email.strip()
    normalized_status = status.strip().lower()
    if not is_valid_email(normalized_email):
        return error_response("Please provide a valid email address.")
    if normalized_status not in ALLOWED_STATUSES:
        return error_response("Status must be one of: lead, active, inactive.")

    clients, error = load_or_error()
    if error:
        return error
    assert clients is not None
    if any(
        str(client.get("email", "")).strip().lower() == normalized_email.lower()
        for client in clients
    ):
        return error_response("A client with this email already exists.")

    new_id = max(
        (client.get("id", 0) for client in clients if isinstance(client.get("id"), int)),
        default=0,
    ) + 1
    client = {
        "id": new_id,
        "name": name.strip(),
        "email": normalized_email,
        "phone": phone.strip(),
        "company": company.strip(),
        "status": normalized_status,
    }
    clients.append(client)
    try:
        save_clients(clients)
    except RuntimeError as exc:
        return error_response(str(exc))
    return {"ok": True, "message": "Client added successfully.", "client": client}


@mcp.tool(description="List all clients or filter them by CRM status.")
def list_clients(status: str = "all") -> dict[str, Any]:
    """Return all clients or clients with the requested status."""
    if not isinstance(status, str):
        return error_response("Status must be text.")
    normalized_status = status.strip().lower()
    if normalized_status != "all" and normalized_status not in ALLOWED_STATUSES:
        return error_response("Status must be one of: all, lead, active, inactive.")

    clients, error = load_or_error()
    if error:
        return error
    assert clients is not None
    filtered = (
        clients
        if normalized_status == "all"
        else [client for client in clients if client.get("status") == normalized_status]
    )
    return {
        "ok": True,
        "count": len(filtered),
        "status": normalized_status,
        "clients": filtered,
    }


@mcp.tool(description="Retrieve one client by its positive integer ID.")
def get_client(client_id: int) -> dict[str, Any]:
    """Return a client or a friendly not-found error."""
    if not isinstance(client_id, int) or isinstance(client_id, bool) or client_id <= 0:
        return error_response("client_id must be a positive integer.")
    clients, error = load_or_error()
    if error:
        return error
    assert clients is not None
    client = find_client(clients, client_id)
    return {"ok": True, "client": client} if client else error_response(
        f"Client {client_id} was not found."
    )


@mcp.tool(description="Update one or more fields on an existing client.")
def update_client(
    client_id: int,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    company: str | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    """Update only supplied fields while preserving all other values."""
    if not isinstance(client_id, int) or isinstance(client_id, bool) or client_id <= 0:
        return error_response("client_id must be a positive integer.")
    supplied = {
        "name": name,
        "email": email,
        "phone": phone,
        "company": company,
        "status": status,
    }
    if not any(value is not None for value in supplied.values()):
        return error_response("Provide at least one field to update.")
    if any(value is not None and not isinstance(value, str) for value in supplied.values()):
        return error_response("Updated client fields must be text.")

    clients, error = load_or_error()
    if error:
        return error
    assert clients is not None
    client = find_client(clients, client_id)
    if client is None:
        return error_response(f"Client {client_id} was not found.")

    if name is not None:
        if not name.strip():
            return error_response("Name cannot be empty.")
        client["name"] = name.strip()
    if email is not None:
        normalized_email = email.strip()
        if not is_valid_email(normalized_email):
            return error_response("Please provide a valid email address.")
        if any(
            other.get("id") != client_id
            and str(other.get("email", "")).strip().lower() == normalized_email.lower()
            for other in clients
        ):
            return error_response("Another client already uses this email.")
        client["email"] = normalized_email
    if phone is not None:
        client["phone"] = phone.strip()
    if company is not None:
        client["company"] = company.strip()
    if status is not None:
        normalized_status = status.strip().lower()
        if normalized_status not in ALLOWED_STATUSES:
            return error_response("Status must be one of: lead, active, inactive.")
        client["status"] = normalized_status

    try:
        save_clients(clients)
    except RuntimeError as exc:
        return error_response(str(exc))
    return {
        "ok": True,
        "message": f"Client {client_id} updated successfully.",
        "client": client,
    }


@mcp.tool(description="Delete an existing client by its positive integer ID.")
def delete_client(client_id: int) -> dict[str, Any]:
    """Delete a client or return a friendly not-found error."""
    if not isinstance(client_id, int) or isinstance(client_id, bool) or client_id <= 0:
        return error_response("client_id must be a positive integer.")
    clients, error = load_or_error()
    if error:
        return error
    assert clients is not None
    client = find_client(clients, client_id)
    if client is None:
        return error_response(f"Client {client_id} was not found.")
    try:
        save_clients([item for item in clients if item.get("id") != client_id])
    except RuntimeError as exc:
        return error_response(str(exc))
    return {
        "ok": True,
        "message": f"Client {client_id} deleted successfully.",
        "deleted_client": client,
    }


@mcp.resource(
    "clients://all",
    name="all_clients",
    description="Read-only JSON snapshot of all current CRM clients.",
    mime_type="application/json",
)
def all_clients_resource() -> str:
    """Return all current records as read-only JSON."""
    clients = load_clients()
    return json.dumps({"count": len(clients), "clients": clients}, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
