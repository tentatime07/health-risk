from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .risk_model import PatientInput, calculate_risk


class RiskRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    sex: Literal["female", "male", "other"]
    bmi: float = Field(ge=12, le=70)
    systolic_bp: int = Field(ge=80, le=240)
    diastolic_bp: int = Field(ge=40, le=140)
    hba1c: float = Field(ge=3.5, le=15)
    smoker: bool
    family_history: bool
    activity_level: Literal["low", "medium", "high"]


app = FastAPI(
    title="HealthRisk AI API",
    description="A beginner-friendly educational risk prediction API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:5174",
        "http://localhost:5174",
        "http://127.0.0.1:5180",
        "http://localhost:5180",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict:
    return {"message": "HealthRisk AI API is running"}


@app.post("/predict")
def predict_risk(request: RiskRequest) -> dict:
    patient = PatientInput(**request.model_dump())
    return calculate_risk(patient)
