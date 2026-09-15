# Mini CRM / Client Manager MCP Server

A beginner-friendly [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for managing local client records. MCP gives an AI application a standard way to discover and call tools provided by another program. This project uses the Python MCP SDK and stores data in one local `clients.json` file.

## Project structure

```text
server.py         MCP server, storage helpers, five tools, and one resource
clients.json      Local client data (kept in the assignment)
requirements.txt  Python dependency
DEMO_PLAN.md      Short Inspector demonstration script
VIVA_ANSWERS.md  Beginner viva questions and answers
.gitignore        Local Python files excluded from Git
```

## Prerequisites

- Windows 11 (the commands below use PowerShell)
- Python 3.10 or newer (tested with Python 3.14)
- Node.js and `npx` (MCP Inspector uses them)
- `uv` is optional; the Python virtual-environment commands below use `venv`

## Setup on Windows

From this project folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal and activate again. The dependency is `mcp>=2,<3`, which matches the current SDK used by this project.

## Run and test with MCP Inspector

Start the development server and Inspector:

```powershell
mcp dev server.py
```

The command starts the server over stdio and launches the Inspector. If `mcp` is not on PATH, use `.\venv\Scripts\mcp.exe dev server.py`. The server can also be started directly with `python server.py`, although Inspector is the easiest way to test it.

In Inspector:

1. Leave the transport as **stdio** and confirm the command is `python` (or select the project virtual-environment Python).
2. Set the argument to `server.py` if Inspector asks for a server script, then click **Connect**.
3. Open **Tools** and confirm `add_client`, `list_clients`, `get_client`, `update_client`, and `delete_client`.
4. Use **Tools** to call each function with the examples below.
5. Open **Resources**, select `clients://all`, and click **Read resource**.

## MCP tools

### `add_client`

Required: `name`, `email`. Optional: `phone`, `company`, `status` (default `lead`). Status must be `lead`, `active`, or `inactive`; email addresses must be unique.

```json
{"name":"Ali Khan","email":"ali@example.com","phone":"03001234567","company":"ABC Solutions","status":"lead"}
```

### `list_clients`

Optional `status` defaults to `all`; use `all`, `lead`, `active`, or `inactive`.

```json
{"status":"lead"}
```

### `get_client`

Requires a positive integer `client_id`.

```json
{"client_id":1}
```

### `update_client`

Requires `client_id` and at least one of `name`, `email`, `phone`, `company`, or `status`. Unsupplied fields are preserved.

```json
{"client_id":1,"status":"active"}
```

### `delete_client`

Requires the positive integer ID to remove.

```json
{"client_id":1}
```

All tools return a structured dictionary with `ok: true` on success or `ok: false` and an understandable `error` message on validation, missing-record, storage, or duplicate-email failures. Examples include an empty name, `ali` as an invalid email, status `waiting`, ID `0`, ID `9999`, and an update with no fields.

## Read-only resource

`clients://all` returns a JSON snapshot containing `count` and every current client. It is a resource rather than a tool because it only exposes information and does not perform a CRM action or modify data.

## Storage and IDs

`clients.json` starts as `[]`. The server reads and writes it with Python’s standard `json` module. A missing or empty file is treated as an empty CRM; malformed JSON is reported as a storage error. IDs are positive integers generated from the highest existing ID plus one. No database, cloud service, authentication, frontend framework, or AI framework is used.

## Example workflow

An assistant can interpret “Add Sara Ahmed from TechNova as a lead and show me all leads” by calling `add_client`, then `list_clients` with `{"status":"lead"}`. Later it can call `update_client` with `{"client_id":1,"status":"active"}` and `get_client` to confirm the change.

## Troubleshooting

- **`mcp` is not recognized:** activate the venv or use `.\venv\Scripts\mcp.exe dev server.py`.
- **Inspector cannot connect:** run the command from the folder containing `server.py`, select stdio, and use the venv Python.
- **No tools appear:** reconnect Inspector and check that the server process has no Python traceback.
- **Duplicate email:** use a different email or update the existing record.
- **Unexpected old records:** inspect or reset `clients.json` to `[]` only when you intentionally want to clear the lab data.

## GitHub submission

Create a repository, add the project files (including `clients.json`), and push the project:

```powershell
git init
git add server.py clients.json requirements.txt README.md DEMO_PLAN.md VIVA_ANSWERS.md .gitignore
git commit -m "Build Mini CRM MCP server"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Do not commit `venv`, `.env`, or Python cache files; `.gitignore` already excludes them.
