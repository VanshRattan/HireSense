# HireSense 🎤👁️

HireSense is an AI-powered interview assessment platform that helps candidates practice mock interviews and receive real-time, actionable feedback based on their audio, speech patterns, and facial expressions.

## Architecture 🏛️

*   **Frontend**: Next.js 15 (React App Router) + Tailwind CSS + Framer Motion for a stunning, glassmorphic UI.
*   **Backend**: FastAPI, connected to PostgreSQL via SQLAlchemy.
*   **ML Pipeline**:
    *   **Audio**: OpenAI Whisper for Speech-to-Text inference, plus basic NLP heuristics for filler-word counting.
    *   **Video**: OpenCV + MediaPipe Face Mesh to extrapolate eye contact quality and facial emotion (e.g. smiling for engagement score).
*   **Infrastructure**: Docker Compose for orchestrating the Frontend, Backend, and Database all in one command.

## Local Dev Setup 🚀

To get up and running:

1.  **Clone the repository**.
2.  **Copy the env file**: `cp .env.example .env` (adjust `.env` if needed).
3.  **Run Docker Compose**:
    ```bash
    docker-compose up --build
    ```
4.  **Access the app**:
    *   Frontend: `http://localhost:3000`
    *   Backend API Docs: `http://localhost:8000/docs`

### Manual Run (Without Docker)

You can run each service manually.

**Terminal 1 (Backend)**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Terminal 2 (Frontend)**
```bash
cd frontend
npm install
npm run dev
```

Enjoy practicing your interviews!
