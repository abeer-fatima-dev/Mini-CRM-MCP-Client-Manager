# Mini CRM MCP Viva Answers

## 1. What problem does MCP solve?

MCP provides a standard way for an AI application to discover and use tools and data from another program instead of needing a custom connector for every application.

## 2. What is an MCP client?

The client is the application that connects to a server, discovers its capabilities, and requests tool calls or resource reads. Inspector is the client in this lab.

## 3. What is an MCP server?

The server is the program that exposes capabilities. Here, `server.py` runs the CRM logic and reads and writes `clients.json`.

## 4. What is an MCP tool?

A tool is an action that a client can call. It has a name, description, input schema, and result.

## 5. Give an example tool from this project.

`add_client` validates a new client and saves it to the JSON file. It returns the new record and its generated ID.

## 6. What is the difference between a tool and a resource?

A tool performs an operation and can change data, such as `update_client`. A resource provides information, such as the read-only `clients://all` view.

## 7. What is transport?

Transport is the communication method used between the MCP client and server.

## 8. What transport does this project use?

It uses stdio. The client starts the local Python process and exchanges MCP messages through standard input and output.

## 9. What happens when Inspector calls `add_client`?

Inspector sends the tool name and JSON arguments. The SDK validates the schema, Python runs the function, the function validates the values and saves the record, and the structured result is returned to Inspector.

## 10. How does MCP know the inputs a tool accepts?

The Python SDK builds the input schema from the decorated function’s name, parameters, defaults, and type hints. For example, `client_id: int` becomes an integer input.

## 11. Explain `get_client`.

It accepts a positive integer ID, loads the JSON records, searches for that ID, and returns the client. If no record matches, it returns a friendly `ok: false` response.

## 12. How does error handling work?

The tools validate names, emails, statuses, IDs, duplicate emails, and required update fields. They return understandable error dictionaries instead of crashing for normal invalid requests. File problems are also reported as storage errors.

## 13. Why choose these five CRM tools?

Together they cover the basic lifecycle: create, list, retrieve, update, and delete. They are useful enough for a CRM while remaining small and easy to explain.

## 14. What does `clients://all` do?

It returns a JSON snapshot of all current client records. It is read-only, so it is registered as a resource rather than a tool.

## 15. Why use JSON instead of a database?

This is a beginner lab. JSON is easy to inspect, needs no external service, and keeps the focus on learning MCP. A production CRM would need a proper database.

## 16. What was a possible challenge?

One challenge was using the APIs that match the installed MCP SDK rather than an older tutorial. Another was distinguishing an omitted update field from an intentionally empty value.

## 17. What could improve a production CRM?

It could add authentication, a real database, audit history, search and pagination, stronger email and phone validation, concurrency protection, automated tests, logging, and access control.

## 18. What did building this teach you?

It taught me how an MCP client discovers server capabilities, how type hints become input schemas, how tools differ from resources, and how a local program can safely expose useful operations to an AI client.
