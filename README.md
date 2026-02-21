# SkillForge

SkillForge is a tightly-scoped progression tracker that maps real-world learning to RPG-style leveling. Users define specific skills and log concentrated training sessions to earn XP and level up. 

This project was built specifically for the Better Software Associate Software Engineer assessment. The scope was intentionally kept small to focus entirely on system structure, interface safety, and strict verification over feature bloat.

## 🧠 Key Technical Decisions

* **Database (PostgreSQL & SQLAlchemy):** Opted for a robust relational structure (One Skill -> Many Sessions). Enforced `cascade="all, delete-orphan"` at the ORM level to guarantee database integrity and prevent orphaned session data if a skill is deleted.
* **Interface Safety (Zod + TypeScript):** The React frontend strictly types all state. Forms use `Zod` schema validation to trap impossible states (e.g., negative duration, unselected skills) *before* triggering network requests.
* **Defense in Depth (Flask API):** The backend fundamentally does not trust the frontend. Routes utilize an "early return" pattern for secondary validation, catching malformed payloads and returning precise HTTP status codes (400, 409, 422) rather than allowing the database to throw internal 500 errors.
* **Architecture (App Factory):** Structured the Flask backend using the Application Factory pattern and Blueprints. This isolates routing from database initialization, making the system highly resilient to future changes.

## 🤖 AI Usage & Review Process

I utilized AI as a pair-programming partner, strictly bound by the rules in `ai_instructions.md`. 
* **Usage:** Leveraged AI to scaffold the Vite/React boilerplate, generate the Flask factory pattern, and draft the initial structure for the automated tests.
* **Critical Review & Verification:** I actively intervened to prevent the AI from over-engineering. For example, I rejected suggestions to implement complex user authentication flows that would violate the "simplicity" mandate for a 48-hour assessment. I also manually verified the `pytest` logic to ensure the mathematical assertions for the RPG leveling system were 100% accurate.

## ⚠️ Tradeoffs, Risks, & Extension

* **Tradeoff / Risk:** To deliver a verified, heavily tested core engine within the timeline, I explicitly omitted User Authentication. The immediate risk is that the current API assumes a single-tenant environment.
* **Extension Approach:** If the system scales, the first step is implementing `Flask-JWT-Extended` to issue secure session tokens. The database schema would be extended to include a `Users` table, with `Skills` holding a foreign key to `user_id`, allowing for secure, isolated, and multi-tenant progress tracking.

## 💻 Local Setup & Verification

**1. Clone & Backend Setup**
\`\`\`bash
git clone https://github.com/BakaBoi331/SkillForge.git
cd SkillForge
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

**2. Database Configuration**
* Create a local PostgreSQL database named `skillforge`.
* Create a `.env` file in the root directory: 
    `DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/skillforge`
* Initialize the tables by running these commands in a python shell:
    \`\`\`python
    from app import create_app, db
    app = create_app()
    with app.app_context():
        db.create_all()
    \`\`\`

**3. Run the System**
* **Backend:** `python run.py` (Runs on http://127.0.0.1:5000)
* **Frontend:** `cd frontend` -> `npm run dev` (Runs on http://localhost:5173)

**4. Run Automated Tests**
Prove the system remains correct by running the test suite (spins up an isolated, in-memory SQLite DB):
\`\`\`bash
python -m pytest -v
\`\`\`