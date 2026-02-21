# ⚔️ SkillForge: RPG Progression Tracker

SkillForge is a full-stack, hyper-focused progression tracker that maps real-world learning to RPG-style leveling mechanics. Users can forge specific skills and log concentrated training sessions to earn XP and level up dynamically.

This project was engineered specifically for the **Better Software Associate Software Engineer** assessment. The scope was intentionally constrained to prioritize system structure, interface safety, and strict verification over feature bloat.

## 🚀 The Tech Stack
* **Backend:** Python + Flask (RESTful API), Application Factory Pattern
* **Frontend:** React + TypeScript (Vite), CSS-in-JS
* **Database:** PostgreSQL (via SQLAlchemy ORM)
* **Validation:** Zod (Frontend Schema), Strict Type Checking
* **Testing:** Pytest (with isolated, in-memory SQLite fixtures)

---

## 🧠 Key Technical Decisions & Architecture

### 1. Defense in Depth (Interface Safety)
The system assumes all client data is inherently untrustworthy.
* **Frontend:** Forms use `Zod` to strictly parse and validate state (e.g., trapping negative study durations or unselected skills) *before* triggering any network requests. 
* **Backend:** The Flask API implements an "Early Return" pattern. Routes immediately reject malformed payloads, returning precise HTTP status codes (400, 409, 422) to prevent the database from throwing internal 500 errors.

### 2. Relational Database Integrity
Built a strict One-to-Many relationship (`Skills` -> `Sessions`). Enforced `cascade="all, delete-orphan"` at the ORM layer. If a user deletes a skill, the database automatically cascades the deletion to all associated sessions, completely eliminating the risk of orphaned rows.

### 3. Server-Side Game Mechanics
The progressive RPG leveling math (`XP = 100 * (Level - 1)^2`) is executed entirely on the backend. The React client acts as a "dumb" UI, simply rendering the calculated progress percentages and levels provided by the API, preventing client-side state manipulation.

### 4. Advanced UX Polish
* **Custom Toast Engine:** Replaced blocking, native browser alerts with a custom, state-driven React toast notification system that auto-dismounts after 3 seconds.
* **Smart Duplication Checks:** Enforced case-insensitive uniqueness at the database query level (using `.ilike()`) so the system intelligently recognizes that "html" and "HTML" are the same skill.
* **Scroll-Locked UI:** Confined the skill list to a bounded, internally scrolling container to preserve a clean layout regardless of data volume.

---

## 🤖 AI Usage & Review Process
I utilized AI as a pair-programming partner, strictly bound by a custom `ai_instructions.md` directive. 
* **Usage:** Leveraged AI to rapidly scaffold the Vite/React boilerplate, establish the Flask Application Factory pattern, and draft the initial Pytest fixtures.
* **Review & Verification:** I actively managed the AI to prevent "feature creep" (e.g., rejecting complex multi-tenant auth setups to maintain a 48-hour scope). I manually verified and adjusted the Pytest assertions to ensure the mathematical logic for the leveling system was mathematically flawless.

---

## 🔮 Tradeoffs & V2 Roadmap
To deliver a mathematically proven, robust engine within the timeline, I explicitly omitted certain features to guarantee core stability. If this were a real production sprint, my V2 roadmap would include:

* **Security & Auth:** Implementing `Flask-JWT-Extended` and expanding the database schema to include a `Users` table for secure, multi-tenant accounts.
* **Complete CRUD:** Adding a `PUT` route to allow users to edit existing skill names.
* **Gamification UX:** Introducing visual CSS milestones (e.g., dynamic borders that upgrade at Levels 5, 10, and 50) and integrating audio cues upon leveling up.
* **Accessibility & UI:** Implementing a system-wide Dark Mode toggle and migrating the native `confirm()` deletion prompt to a custom React modal.

---

## 💻 Local Setup & Verification

**1. Clone & Backend Setup**
\`\`\`bash
git clone <https://www.github.com/BakaBoi331/SkillForge>
cd SkillForge
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

**2. Database Configuration**
* Ensure PostgreSQL is running locally.
* Create a database named `skillforge`.
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
* **Start Backend:** `python run.py` (Defaults to port 5000)
* **Start Frontend:** `cd frontend` then `npm run dev` (Defaults to port 5173)

**4. Run Automated Verification**
Prove the system's math and edge-case handling remain correct by running the test suite (spins up an isolated, in-memory SQLite DB):
\`\`\`bash
python -m pytest -v
\`\`\`