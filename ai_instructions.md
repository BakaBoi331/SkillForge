# AI Guidance Rules & Constraints

**Role:** You are acting as a junior developer pair-programming with a Senior Staff Engineer. Your output will be strictly evaluated on simplicity, correctness, and interface safety. 

**Core Mandate:** Small, well-structured, and readable code scores higher than large, feature-rich, complex code. Do not hallucinate scope outside of the current specific prompt.

Before generating any code for this project, you must adhere to the following constraints:

## 1. Structure & Simplicity
* **No Spaghetti Code:** Backend logic must be separated. Use Flask Blueprints for routing and SQLAlchemy models for database schema. Do not put database logic inside `run.py`.
* **Simple > Clever:** Write predictable, readable code. Avoid obscure one-liners that are difficult to debug.
* **Frontend Modularity:** React components should be focused. Keep state management as local as possible.

## 2. Correctness & Interface Safety
* **Never Trust the Client:** The Flask API must validate all incoming data, even if the frontend already validated it. 
* **Early Returns:** Use the "early return" pattern in Python routes to immediately reject invalid states (e.g., negative numbers, empty strings, missing fields) before touching the database.
* **Strict Frontend Types:** Use TypeScript interfaces for all data. Use `Zod` (or similar) to parse and validate forms before submission. Disable submission vectors if data is invalid.
* **Observability:** API endpoints must return precise HTTP status codes (201 for creation, 400 for bad requests, 404 for not found, 409 for conflicts, 422 for unprocessable entities) along with clear JSON error messages.

## 3. Change Resilience & Verification
* **Relational Integrity:** Ensure foreign keys use appropriate cascading behaviors (`cascade="all, delete-orphan"`) so deleting a parent resource cleanly handles child resources without leaving orphaned data.
* **Test-Driven Focus:** You must be prepared to write `pytest` functions that prove the core business logic works.
* **Test Isolation:** Do not mock the database in a way that skips relational logic. Tests must run against an ephemeral, in-memory SQLite database to prove the ORM models behave correctly under real query conditions.