from sqlalchemy import Column, INTEGER, String, Float
from database import Base


class user(Base):
    __tablename__ = "customers"
    customerID = Column(INTEGER,primary_key=True, index=True)
    gender = Column(String(50))
    SeniorCitizen = Column(INTEGER)
    Partner = Column(String(50))
    Dependents = Column(String(50))
    tenure = Column(INTEGER)
    PhoneService = Column(String(50))
    MultipleLines = Column(String(50))
    InternetService = Column(String(50))
    OnlineSecurity = Column(String(50))
    OnlineBackup = Column(String(50))
    DeviceProtection = Column(String(50))
    TechSupport = Column(String(50))
    StreamingTV = Column(String(50))
    StreamingMovies = Column(String(50))
    Contract = Column(String(50))
    PaperlessBilling = Column(String(50))
    PaymentMethod = Column(String(50))
    MonthlyCharges = Column(Float)
    TotalCharges = Column(Float)
    Gmail = Column(String(50))
    Churn = Column(String(50))
    Churn_Reason = Column(String(50))
    Percentage = Column(Float)
    