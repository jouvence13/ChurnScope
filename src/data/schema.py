from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class YesNoEnum(str, Enum):
    YES = "Yes"
    NO = "No"


class MultipleLinesEnum(str, Enum):
    YES = "Yes"
    NO = "No"
    NO_PHONE_SERVICE = "No phone service"


class InternetServiceEnum(str, Enum):
    DSL = "DSL"
    FIBER_OPTIC = "Fiber optic"
    NO = "No"


class InternetFeatureEnum(str, Enum):
    YES = "Yes"
    NO = "No"
    NO_INTERNET_SERVICE = "No internet service"


class ContractEnum(str, Enum):
    MONTH_TO_MONTH = "Month-to-month"
    ONE_YEAR = "One year"
    TWO_YEAR = "Two year"


class PaymentMethodEnum(str, Enum):
    ELECTRONIC_CHECK = "Electronic check"
    MAILED_CHECK = "Mailed check"
    BANK_TRANSFER = "Bank transfer (automatic)"
    CREDIT_CARD = "Credit card (automatic)"


class CustomerInputSchema(BaseModel):
    """Validation stricte des caractéristiques d'un client."""

    customerID: Optional[str] = Field(
        default=None, description="Identifiant unique du client"
    )
    gender: GenderEnum
    SeniorCitizen: int = Field(ge=0, le=1, description="0 = Non sénior, 1 = Sénior")
    Partner: YesNoEnum
    Dependents: YesNoEnum
    tenure: int = Field(ge=0, le=100, description="Nombre de mois d'ancienneté")
    PhoneService: YesNoEnum
    MultipleLines: MultipleLinesEnum
    InternetService: InternetServiceEnum
    OnlineSecurity: InternetFeatureEnum
    OnlineBackup: InternetFeatureEnum
    DeviceProtection: InternetFeatureEnum
    TechSupport: InternetFeatureEnum
    StreamingTV: InternetFeatureEnum
    StreamingMovies: InternetFeatureEnum
    Contract: ContractEnum
    PaperlessBilling: YesNoEnum
    PaymentMethod: PaymentMethodEnum
    MonthlyCharges: float = Field(ge=0.0, le=500.0, description="Frais mensuels en €")
    TotalCharges: Optional[float] = Field(
        default=None, ge=0.0, le=20000.0, description="Total facturé en €"
    )

    @field_validator("TotalCharges", mode="before")
    @classmethod
    def parse_total_charges(cls, v):
        if v is None or v == "" or (isinstance(v, str) and v.strip() == ""):
            return None
        return float(v)


class PredictionResponse(BaseModel):
    """Format de réponse de prédiction."""

    churn_probability: float = Field(ge=0.0, le=1.0)
    churn_prediction: int = Field(ge=0, le=1)
    risk_level: str
