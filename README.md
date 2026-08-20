# HealthRisk AI

A beginner-friendly full-stack health risk calculator. The goal is not to diagnose disease. It shows how a simple backend model can turn patient inputs into a risk estimate, explain which factors mattered most, and display the result in a React app.

This version is intentionally scoped so a freshman or sophomore CS student could understand and explain it in an internship interview.

## What It Does

- Collects basic health inputs such as age, BMI, blood pressure, HbA1c, smoking, activity level, and family history.
- Sends those inputs to a FastAPI backend.
- Uses a small transparent scoring model to estimate diabetes / cardiometabolic risk.
- Returns a risk percentage, category, top contributing factors, and simple prevention tips.
- Displays everything in a clean React dashboard.

## Tech Stack

- Frontend: React + Vite
- Backend: Python + FastAPI
- Model: simple weighted scoring function with a sigmoid conversion
- Testing: pytest for the model logic

## Project Structure

```text
health-risk/
  backend/
    app/
      main.py
      risk_model.py
    tests/
      test_risk_model.py
    requirements.txt
  frontend/
    src/
      App.jsx
      main.jsx
      styles.css
    package.json
  README.md
```

## Run Locally

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will run at `http://127.0.0.1:8000`.

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The app will run at `http://127.0.0.1:5173`.

If port 5173 is already being used, run:

```bash
npm run dev -- --port 5180 --strictPort
```

## Run Tests

```bash
cd backend
python -m pytest
```

## How To Explain This In An Interview

"I built a small full-stack health risk app. The frontend is a React form where a user enters common health measurements. The backend is a FastAPI server with one prediction endpoint. Instead of using a complicated black-box model, I made a transparent weighted scoring model so I could explain exactly how each feature affects the final risk score. The API returns both the percentage and the main factors that increased risk, and the frontend turns that into a simple dashboard."

Good talking points:

- You separated frontend UI from backend logic.
- You validated inputs with Pydantic.
- You kept the model explainable by showing feature contributions.
- You wrote tests for the prediction logic.
- You clearly state this is an educational screening tool, not a medical diagnosis.

## Possible Next Steps

- Replace the hand-written weights with a scikit-learn logistic regression model.
- Train on a public dataset such as NHANES.
- Add charts for model evaluation.
- Store anonymous prediction history in a database.
