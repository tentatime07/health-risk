from app.risk_model import PatientInput, calculate_risk


def make_patient(**overrides):
    patient = {
        "age": 40,
        "sex": "female",
        "bmi": 24,
        "systolic_bp": 118,
        "diastolic_bp": 76,
        "hba1c": 5.2,
        "smoker": False,
        "family_history": False,
        "activity_level": "high",
    }
    patient.update(overrides)
    return PatientInput(**patient)


def test_low_risk_patient_has_low_category():
    result = calculate_risk(make_patient())

    assert result["category"] == "Low"
    assert result["risk_percent"] < 20


def test_higher_risk_inputs_raise_risk_score():
    low_risk = calculate_risk(make_patient())
    high_risk = calculate_risk(
        make_patient(
            age=62,
            bmi=34,
            systolic_bp=152,
            diastolic_bp=94,
            hba1c=6.4,
            smoker=True,
            family_history=True,
            activity_level="low",
        )
    )

    assert high_risk["risk_percent"] > low_risk["risk_percent"]
    assert high_risk["category"] in ["Moderate", "High"]


def test_top_factors_are_returned_in_descending_order():
    result = calculate_risk(make_patient(hba1c=6.6, bmi=33, smoker=True))
    impacts = [factor["impact"] for factor in result["top_factors"]]

    assert impacts == sorted(impacts, reverse=True)
