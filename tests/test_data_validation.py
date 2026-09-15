import pytest
from pydantic import ValidationError
from src.data.schema import CustomerInputSchema, GenderEnum, ContractEnum


def test_valid_customer_schema():
    """Vérifie qu'un dictionnaire client valide est correctement parsé par Pydantic."""
    valid_data = {
        "customerID": "7590-VHVEG",
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 1,
        "PhoneService": "No",
        "MultipleLines": "No phone service",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "Yes",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 29.85,
        "TotalCharges": 29.85,
    }

    customer = CustomerInputSchema(**valid_data)
    assert customer.customerID == "7590-VHVEG"
    assert customer.gender == GenderEnum.FEMALE
    assert customer.Contract == ContractEnum.MONTH_TO_MONTH
    assert customer.MonthlyCharges == 29.85


def test_invalid_tenure_raises_validation_error():
    """Vérifie qu'une ancienneté négative déclenche une erreur de validation."""
    invalid_data = {
        "gender": "Male",
        "SeniorCitizen": 0,
        "Partner": "No",
        "Dependents": "No",
        "tenure": -5,  # Invalide
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "DSL",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 50.0,
        "TotalCharges": 100.0,
    }

    with pytest.raises(ValidationError):
        CustomerInputSchema(**invalid_data)


def test_empty_string_total_charges_parsed_as_none():
    """Vérifie que les chaînes vides dans TotalCharges (clients tenure=0) sont converties en None."""
    data_with_blank_total = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "Yes",
        "tenure": 0,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "No",
        "OnlineSecurity": "No internet service",
        "OnlineBackup": "No internet service",
        "DeviceProtection": "No internet service",
        "TechSupport": "No internet service",
        "StreamingTV": "No internet service",
        "StreamingMovies": "No internet service",
        "Contract": "Two year",
        "PaperlessBilling": "No",
        "PaymentMethod": "Mailed check",
        "MonthlyCharges": 20.0,
        "TotalCharges": "  ",  # Espace vide
    }

    customer = CustomerInputSchema(**data_with_blank_total)
    assert customer.TotalCharges is None
