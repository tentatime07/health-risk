from __future__ import annotations

from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class PatientInput:
    age: int
    sex: str
    bmi: float
    systolic_bp: int
    diastolic_bp: int
    hba1c: float
    smoker: bool
    family_history: bool
    activity_level: str


FACTOR_LABELS = {
    "age": "Age",
    "bmi": "BMI",
    "blood_pressure": "Blood pressure",
    "hba1c": "HbA1c",
    "smoker": "Smoking",
    "family_history": "Family history",
    "activity_level": "Low activity",
}


def _sigmoid(score: float) -> float:
    return 1 / (1 + exp(-score))


def _risk_category(risk_percent: float) -> str:
    if risk_percent < 20:
        return "Low"
    if risk_percent < 45:
        return "Moderate"
    return "High"


def _activity_score(activity_level: str) -> float:
    normalized = activity_level.lower().strip()
    if normalized == "low":
        return 0.55
    if normalized == "medium":
        return 0.2
    return 0.0


def calculate_risk(patient: PatientInput) -> dict:
    """Estimate risk with a simple explainable scoring model.

    The weights are intentionally readable for a student project. They are not
    clinically validated and should not be used for medical decisions.
    """
    contributions = {
        "age": max(patient.age - 35, 0) * 0.025,
        "bmi": max(patient.bmi - 25, 0) * 0.08,
        "blood_pressure": max(patient.systolic_bp - 120, 0) * 0.012
        + max(patient.diastolic_bp - 80, 0) * 0.01,
        "hba1c": max(patient.hba1c - 5.4, 0) * 0.9,
        "smoker": 0.45 if patient.smoker else 0.0,
        "family_history": 0.35 if patient.family_history else 0.0,
        "activity_level": _activity_score(patient.activity_level),
    }

    base_score = -3.0
    score = base_score + sum(contributions.values())
    risk_percent = round(_sigmoid(score) * 100, 1)

    top_factors = [
        {
            "name": FACTOR_LABELS[key],
            "impact": round(value, 2),
        }
        for key, value in sorted(
            contributions.items(), key=lambda item: item[1], reverse=True
        )
        if value > 0
    ][:3]

    return {
        "risk_percent": risk_percent,
        "category": _risk_category(risk_percent),
        "top_factors": top_factors,
        "tips": build_tips(patient, top_factors),
        "disclaimer": "Educational estimate only. This is not a medical diagnosis.",
    }


def build_tips(patient: PatientInput, top_factors: list[dict]) -> list[str]:
    tips = []
    factor_names = {factor["name"] for factor in top_factors}

    if "HbA1c" in factor_names:
        tips.append("Ask a clinician about follow-up blood sugar testing.")
    if "Blood pressure" in factor_names:
        tips.append("Track blood pressure regularly and discuss high readings.")
    if "BMI" in factor_names:
        tips.append("Small, steady nutrition and activity changes can lower risk.")
    if patient.smoker:
        tips.append("Smoking is a major risk factor; quitting support can help.")
    if patient.activity_level.lower() == "low":
        tips.append("Adding regular walks is a realistic first activity goal.")

    if not tips:
        tips.append("Keep monitoring routine health measurements over time.")

    return tips[:3]
