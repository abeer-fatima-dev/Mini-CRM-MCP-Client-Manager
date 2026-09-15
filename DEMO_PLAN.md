# 4–5 Minute Mini CRM Demo Plan

## 1. Introduce the project (30 seconds)

Explain that this is a local Mini CRM MCP server. It exposes five tools for the client lifecycle and stores records in `clients.json`.

## 2. Show discovery (30 seconds)

Run `mcp dev server.py`, connect Inspector over stdio, and show the five tools:

- `add_client`
- `list_clients`
- `get_client`
- `update_client`
- `delete_client`

Also show the `clients://all` resource.

## 3. Query 1: add and list (60 seconds)

Say: **“Add Sara Ahmed from TechNova as a lead and show me all leads.”**

Call `add_client`:

```json
{
  "name": "Sara Ahmed",
  "email": "sara@technova.com",
  "phone": "03001234567",
  "company": "TechNova",
  "status": "lead"
}
```

Note the returned `id`, then call `list_clients`:

```json
{"status":"lead"}
```

Explain that the record is now persisted in `clients.json`.

## 4. Query 2: update and retrieve (60 seconds)

Say: **“Sara became a customer. Change her status to active and show me her record.”**

Call `update_client` with Sara’s returned ID:

```json
{"client_id":1,"status":"active"}
```

Then call:

```json
{"client_id":1}
```

with `get_client` to show the updated record.

## 5. Demonstrate graceful errors (30 seconds)

Call `get_client` with `{"client_id":9999}`. Explain that the server returns `ok: false` and a friendly message instead of crashing. Optionally demonstrate duplicate email or invalid status.

## 6. Read the resource (30 seconds)

In Inspector, open **Resources**, choose `clients://all`, and read it. Explain: a tool performs an operation, while this resource is a read-only view of current data.
