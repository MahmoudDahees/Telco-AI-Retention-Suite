from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import numpy as np
from models import user
from database import Sessionlocal
from sqlalchemy.orm import Session
from typing import Annotated
from database import Base,engine
import shap
import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage
from fastapi import HTTPException
#load_dotenv()
#sender_email = os.getenv("Sender_email")
#password = os.getenv("Password")
class gmail(BaseModel):
    sender_gmail:str
    password:str

data = pd.read_csv(r"Dataset\WA_Fn-UseC_-Telco-Customer-Churn.csv")


def generate_html_email(
    category_title,
    headline,
    body_paragraph,
    cta_text="Claim Offer in Dashboard",
    cta_url="https://github.com/MahmoudDahees",
):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{headline}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f4f6f9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f6f9; padding: 40px 15px;">
    <tr>
      <td align="center">
        <!-- Main Card Container -->
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e9ecef;">
          
          <!-- Top Accent Bar -->
          <tr>
            <td style="background-color: #2563eb; height: 6px; line-height: 6px; font-size: 6px;">&nbsp;</td>
          </tr>

          <!-- Header Section -->
          <tr>
            <td style="padding: 35px 40px 20px 40px; text-align: left;">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td>
                    <!-- Brand Category Badge -->
                    <span style="display: inline-block; padding: 6px 12px; background-color: #eff6ff; color: #1d4ed8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; border-radius: 20px; border: 1px solid #dbeafe;">
                      {category_title}
                    </span>
                    <!-- Main Headline -->
                    <h1 style="margin: 18px 0 0 0; color: #0f172a; font-size: 22px; font-weight: 700; line-height: 1.35; letter-spacing: -0.5px;">
                      {headline}
                    </h1>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body Content -->
          <tr>
            <td style="padding: 0 40px 25px 40px; text-align: left;">
              <p style="margin: 0; color: #334155; font-size: 15px; line-height: 1.65; letter-spacing: 0.1px;">
                {body_paragraph}
              </p>
            </td>
          </tr>

          <!-- Highlight Box -->
          <tr>
            <td style="padding: 0 40px 30px 40px;">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f8fafc; border-left: 4px solid #2563eb; border-radius: 4px; padding: 14px 18px;">
                <tr>
                  <td style="color: #475569; font-size: 13px; line-height: 1.5;">
                    <strong style="color: #0f172a;">Priority Benefit:</strong> This tailored adjustment has been pre-approved and linked to your primary account identifier.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Call to Action Button -->
          <tr>
            <td style="padding: 0 40px 40px 40px; text-align: left;">
              <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center" style="border-radius: 8px; background-color: #2563eb;">
                    <a href="{cta_url}" target="_blank" style="display: inline-block; padding: 14px 28px; font-size: 14px; font-weight: 600; color: #ffffff; text-decoration: none; border-radius: 8px; background-color: #2563eb; letter-spacing: 0.3px;">
                      {cta_text} &rarr;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Footer Section -->
          <tr>
            <td style="background-color: #f8fafc; padding: 25px 40px; border-top: 1px solid #e2e8f0; text-align: center;">
              <p style="margin: 0 0 8px 0; color: #64748b; font-size: 12px; line-height: 1.5;">
                You are receiving this communication regarding your registered service account.
              </p>
              <p style="margin: 0; color: #94a3b8; font-size: 11px;">
                &copy; 2026 Telecommunications &amp; Digital Services. All rights reserved. &bull; <a href="#" style="color: #64748b; text-decoration: underline;">Privacy Policy</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return html_content

def send_email(reason: str,Sender_gmail:str ,password ,Gmail:str):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(Sender_gmail, password)
    
    RETENTION_CAMPAIGNS = {
    "MonthlyCharges": {
        "category": "High Cost / Pricing Sensitivity",
        "email_subject": r"Exclusive Courtesy: 20% Loyalty Reduction on Your Monthly Plan",
        "headline": "Special Rate Reduction Approved for Your Account",
        "body_text": "Dear Valued Customer, we continuously review our account portfolios to ensure optimal value. We understand that managing monthly expenses is essential; as a gesture of our commitment to your satisfaction, we have approved a <strong>20% discount on your current subscription for the next three billing cycles</strong>. Alternatively, our account team is available to help restructure your package into a tailored tier matching your usage.",
        "cta_text": "Apply 20% Discount Now",
    },
    "TotalCharges": {
        "category": "Cumulative Spend / Budget Concern",
        "email_subject": "Valued Partnership Recognition: Special Account Credit Applied",
        "headline": "A Special Loyalty Reward Has Been Credited",
        "body_text": "Dear Customer, we extend our sincere appreciation for your ongoing commitment. In recognition of your continued tenure and substantial investment with us, we have provisioned a <strong>direct loyalty reward balance</strong> applicable toward your upcoming invoices to ensure exceptional long-term value.",
        "cta_text": "View Account Balance",
    },
    "PaperlessBilling": {
        "category": "Billing Transparency Concern",
        "email_subject": "Enhanced Billing Clarity: Introducing Itemized Expenditure Alerts",
        "headline": "Complete Visibility Over Your Monthly Invoices",
        "body_text": "Transparent communication regarding your financial transactions is a cornerstone of our service. You can now enable <strong>customizable pre-invoice threshold alerts</strong> and comprehensive itemized reports, allowing you to effortlessly monitor usage trends prior to statement finalization.",
        "cta_text": "Configure Usage Alerts",
    },
    "PaymentMethod": {
        "category": "Payment Friction / Inconvenience",
        "email_subject": "Seamless Billing Management: Save 10% with Automated Payments",
        "headline": "Simplify Settlements & Receive an Instant 10% Credit",
        "body_text": "Avoid the risk of unintended service interruptions by enrolling in our secure Auto-Pay service. When you configure automated recurring settlements using your preferred credit card today, you will automatically receive a <strong>10% promotional credit applied to your next statement</strong>.",
        "cta_text": "Enable Secure Auto-Pay",
    },
    "Contract": {
        "category": "Flexible / High Attrition Contract",
        "email_subject": "Long-Term Rate Protection: Secure Fixed Pricing and 2 Months Complimentary",
        "headline": "Lock in Your Lowest Rate Tier + 2 Months Free",
        "body_text": "Protect your monthly budget against future rate adjustments while maximizing overall savings. By transitioning your existing month-to-month subscription to our standard annual agreement, you will secure our <strong>lowest guaranteed rate tier plus 2 full billing months of complimentary service</strong>.",
        "cta_text": "Upgrade to Annual Agreement",
    },
    "tenure": {
        "category": "New Customer Onboarding Risk",
        "email_subject": "Ensuring Excellence: A Personal Check-In on Your Initial Service Experience",
        "headline": "How Has Your Initial Network Experience Been?",
        "body_text": "Thank you for choosing us as your trusted service provider. As you complete your initial onboarding period, our primary objective is to verify that all configurations are performing to your complete satisfaction. Our <strong>specialized onboarding concierge team is available 24/7</strong> for personalized optimization.",
        "cta_text": "Schedule Optimization Call",
    },
    "InternetService": {
        "category": "Connectivity Quality / Fiber Concerns",
        "email_subject": "Infrastructure Optimization: Scheduled Network Diagnostic and Speed Upgrade",
        "headline": "Complimentary Fiber Line Calibration & Speed Boost",
        "body_text": "As part of our continuous commitment to engineering a resilient network environment, our operations team has scheduled a <strong>complimentary remote line-integrity diagnostic and bandwidth profile optimization</strong> for your connection to guarantee maximum throughput and minimal latency.",
        "cta_text": "Check Network Diagnostics",
    },
    "TechSupport": {
        "category": "Lack of Technical Assistance",
        "email_subject": "Priority Escalation Enabled: Direct Access to VIP Technical Concierge",
        "headline": "VIP Priority Technical Support Activated",
        "body_text": "Seamless operations and prompt issue resolution are critical. To ensure you receive immediate technical assistance whenever required, your profile has been elevated to <strong>VIP Priority Technical Support status</strong>, giving you direct routing to senior network engineers with zero queue hold times.",
        "cta_text": "Access VIP Tech Portal",
    },
    "OnlineSecurity": {
        "category": "Digital Safety Gap",
        "email_subject": "Comprehensive Cyber Threat Protection: Complimentary 90-Day Enterprise Defense",
        "headline": "Activate Your 90-Day Advanced Cyber Defense",
        "body_text": "Securing your household devices and personal data is paramount. Enjoy a <strong>90-day complimentary subscription to our Advanced Cyber Security Suite</strong>, featuring real-time malicious payload filtering, identity protection, and multi-device defense across all connected endpoints.",
        "cta_text": "Activate Security Module",
    },
    "OnlineBackup": {
        "category": "Data Protection Risk",
        "email_subject": "Enterprise Cloud Provisioning: 100 GB Secure Automated Backup Activated",
        "headline": "100 GB Encrypted Cloud Storage Provisioned",
        "body_text": "Safeguarding critical files and digital archives requires automated and redundant solutions. We have successfully provisioned <strong>100 GB of high-availability, end-to-end encrypted cloud backup capacity</strong> directly to your account at zero additional charge.",
        "cta_text": "Set Up Automated Backup",
    },
    "DeviceProtection": {
        "category": "Hardware / Device Maintenance",
        "email_subject": "Comprehensive Equipment Assurance: Zero-Downtime Hardware Coverage",
        "headline": "Zero-Downtime Hardware & Router Coverage",
        "body_text": "Eliminate unexpected repair costs and hardware failure concerns. Your subscription now includes <strong>priority on-site technician dispatch and instantaneous next-business-day router replacements</strong> in the event of any hardware degradation.",
        "cta_text": "Review Equipment Policy",
    },
    "StreamingTV": {
        "category": "Entertainment Engagement",
        "email_subject": "Premium Entertainment Upgrade: 50% Courtesy Discount and Full On-Demand Access",
        "headline": "50% Savings on Premium Streaming Channels",
        "body_text": "Enhance your home viewing portfolio with our most comprehensive television package. Expand your subscription to include <strong>premium broadcast channels at a 50% recurring discount</strong>, along with an all-inclusive 30-day pass to our on-demand cinema repository.",
        "cta_text": "Unlock TV Entertainment Pass",
    },
    "StreamingMovies": {
        "category": "Cinema & Media Retention",
        "email_subject": "Exclusive Entertainment Pass: Complimentary 4K Cinema Access Granted",
        "headline": "Your Complimentary 4K Cinema Pass Is Ready",
        "body_text": "We are pleased to present you with an exclusive Cinema Entertainment Pass, granting you <strong>unlimited access to our extensive catalogue of 4K Ultra HD blockbusters</strong> across all your screens with zero advertising interruptions.",
        "cta_text": "Start Watching in 4K",
    },
    "MultipleLines": {
        "category": "Family / Multi-user Expansion",
        "email_subject": "Account Consolidation Advantage: 30% Preferential Rate on Additional Lines",
        "headline": "Consolidate Family Plans & Save 30% per Line",
        "body_text": "Streamline household communication into a single statement. By adding family members to your existing primary profile today, you will receive a <strong>permanent 30% rate reduction per added line</strong> with unthrottled high-speed data and unlimited voice coverage.",
        "cta_text": "Add Discounted Lines",
    },
    "PhoneService": {
        "category": "Voice Calling Feature",
        "email_subject": "Enhanced Communication Capabilities: Unlimited Voice Bundles Activated",
        "headline": "Unlimited Nationwide & Regional Voice Calling",
        "body_text": "Maintaining seamless communication across borders should be simple and predictable. We have configured an <strong>exclusive unlimited voice package</strong> that integrates directly into your current plan with zero activation surcharges.",
        "cta_text": "Activate Unlimited Calling",
    },
    "SeniorCitizen": {
        "category": "Senior Care & Specialized Assistance",
        "email_subject": "Dedicated Client Care: Direct-Route Specialized Customer Assistance",
        "headline": "Dedicated Direct-Route Client Support",
        "body_text": "Our fundamental commitment is to deliver an accessible, straightforward, and supportive service experience. Your account has been assigned to our <strong>Specialized Care Desk</strong>, connecting you directly to senior representatives with patience and zero hold times.",
        "cta_text": "Connect with Dedicated Care",
    },
    "Partner": {
        "category": "Household Plan",
        "email_subject": "Shared Household Connectivity: Maximize Speeds and Multi-User Benefits",
        "headline": "Optimized Multi-Device Household Connectivity",
        "body_text": "Cohabitating and managing simultaneous high-bandwidth demands requires an intelligent network framework. Discover our curated <strong>household bundles that distribute dedicated bandwidth across all devices</strong> without latency spikes.",
        "cta_text": "Explore Shared Plans",
    },
    "Dependents": {
        "category": "Family & Parental Control",
        "email_subject": "Smart Family Protection: Advanced Content Filtering and Bandwidth Management",
        "headline": "Smart Parental Controls & Family Safeguards",
        "body_text": "Establishing a balanced online environment for children is a top priority. Deploy our <strong>Parental Control Center</strong> to set customized screen schedules, filter inappropriate web content, and allocate priority bandwidth for remote learning.",
        "cta_text": "Open Parental Dashboard",
    },
    "gender": {
        "category": "General Personalization",
        "email_subject": "Tailored Service Portfolio: Solutions Aligned with Your Preferences",
        "headline": "Curated Solutions Built Around Your Account",
        "body_text": "We are continuously refining our portfolio to ensure products integrate seamlessly with your lifestyle. Explore a <strong>hand-picked selection of performance upgrades and tailored commercial terms</strong> structured around your usage profile.",
        "cta_text": "View Personalized Offers",
    },
    }
    email_html_body = generate_html_email(
    category_title=RETENTION_CAMPAIGNS[reason]["category"],
    headline=RETENTION_CAMPAIGNS[reason]["headline"],
    body_paragraph=RETENTION_CAMPAIGNS[reason]["body_text"],
    cta_text=RETENTION_CAMPAIGNS[reason]["cta_text"],
    )
    msg = EmailMessage()
    msg["Subject"] = RETENTION_CAMPAIGNS[reason]['email_subject']
    msg["From"] = Sender_gmail
    msg["To"] = Gmail
    msg.set_content(RETENTION_CAMPAIGNS[reason]["body_text"])
    msg.add_alternative(email_html_body, subtype="html")
    server.send_message(msg)

def preprocesing(data):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame([data])
    try:
        data = data.drop("Gmail",axis=1)
    except:
        pass
    try:
        data = data.drop(["Churn","customerID"],axis=1)
    except:
        pass
    data["gender"] = data["gender"].map({"Male": 1, "Female": 0})
    data["Partner"] = data["Partner"].map({"Yes": 1, "No": 0})
    data["Dependents"] = data["Dependents"].map({"Yes": 1, "No": 0})
    data["PhoneService"] = data["PhoneService"].map({"Yes": 1, "No": 0})
    data["MultipleLines"] = data["MultipleLines"].map({"Yes": 1, "No": 0, "No phone service": 2})
    data["InternetService"] = data["InternetService"].map({"DSL": 1, "Fiber optic": 2, "No": 0})
    data["OnlineSecurity"] = data["OnlineSecurity"].map({"Yes": 1, "No": 0, "No internet service": 2})
    data["OnlineBackup"] = data["OnlineBackup"].map({"Yes": 1, "No": 0, "No internet service": 2})
    data["DeviceProtection"] = data["DeviceProtection"].map({"Yes": 1, "No": 0, "No internet service": 2})
    data["TechSupport"] = data["TechSupport"].map({"Yes": 1, "No": 0, "No internet service": 2})
    data["StreamingTV"] = data["StreamingTV"].map({"Yes": 1, "No": 0, "No internet service": 2})
    data["StreamingMovies"] = data["StreamingMovies"].map({"Yes": 1, "No": 0, "No internet service": 2})
    data["Contract"] = data["Contract"].map({"Month-to-month": 1, "One year": 2, "Two year": 3})
    data["PaperlessBilling"] = data["PaperlessBilling"].map({"Yes": 1, "No": 0})
    data["PaymentMethod"] = data["PaymentMethod"].map({"Electronic check": 1, "Mailed check": 2, "Bank transfer (automatic)": 3, "Credit card (automatic)": 4})
    data["YearlyCharges"] = data["MonthlyCharges"] * 12
    data["SubscriptionSegment"]  = pd.cut(data["MonthlyCharges"], bins=[0, 30,60,119], labels=[0, 1, 2]).astype(int)
    data = data.drop(['gender', 'PhoneService', 'MultipleLines'],axis=1)
    data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce').fillna(0)
    return data,data.columns
Base.metadata.create_all(engine)
with open(r"Project files\xgb_model.pkl", "rb") as f:
    model = pickle.load(f)
with open(r"Project files\scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
background_data, col = preprocesing(data)[:200]
explainer = shap.Explainer(model.predict_proba, scaler.transform(background_data))
columns = background_data
print(col)
def shaping(data, prediction):
    if prediction == 1:
        shap_values = explainer(data)
        churn_reason1 = np.argmax(shap_values.values[0][:,1])
        churn_reason = col[churn_reason1]
        reason = churn_reason
    else:
        reason = "Nothing"
    return reason
get_nw_db = Annotated[Session,Depends(get_db)]

class customer(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float
    Gmail: str

class Updater(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_methods=["*"],
                   allow_credentials=True,
                   allow_headers=["*"],
                   allow_origins=["*"]
                   )

@app.get("/")
def get_data(db: get_nw_db):
    return db.query(user).all()
    

@app.post("/predict")

def predict(Customer:customer, db: get_nw_db):
    data = pd.DataFrame([Customer.model_dump()])
    cust_data3, col2 = preprocesing(data)
    cust_data = scaler.transform(cust_data3)
    prediction = model.predict(cust_data)
    prediction_str = "Churn" if prediction == 1 else "Not churn"
    prob = model.predict_proba(cust_data)
    cust_data2 = Customer.model_dump()
    cust_data2["Churn"] = prediction_str
    cust_data2["Churn_Reason"] = f"{shaping(cust_data,prediction)}"
    cust_data2["Percentage"] = prob[0][1]
    print(cust_data2)
    user1 = user(**cust_data2)
    db.add(user1)
    db.commit()
    return f"this client will {prediction_str} with probapilty of {prob[0][1]:.2%} becasue of {cust_data2['Churn_Reason']}"



@app.delete("/delete_user")


def delete_user(id:int, db:get_nw_db):
    user_2 = db.query(user).filter(user.customerID == id).first()
    if not user_2:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(user_2)
    db.commit()
    return "Deleted"

@app.delete("/delete_all_users")

def delete_all(db:get_nw_db):
    
    db.query(user).delete()
    db.commit()
    return "All deleted"

@app.get("/get_user/{customer_id}")
def get_user(customer_id:int, db:get_nw_db):
    
    user_1 = db.query(user).filter(user.customerID == customer_id).first()
    if not user_1:
        raise HTTPException(status_code=404, detail="Customer not found")
    return user_1

@app.put("/update_user")
def update_user(nw_data:Updater, id:int, db:get_nw_db):
    
    user_1 = db.query(user).filter(user.customerID == id).first()
    if not user_1:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in nw_data.model_dump().items():
        setattr(user_1,key,value)
    data = pd.DataFrame([nw_data.model_dump()])
    cust_data, col = preprocesing(data)
    
    cust_data = scaler.transform(cust_data)
    prediction = model.predict(cust_data)
    prob = model.predict_proba(cust_data)
    prediction_str = "Churn" if prediction == 1 else "Not churn"
    prob = model.predict_proba(cust_data)
    setattr(user_1,"Churn",prediction_str)
    nw_reason = shaping(cust_data, prediction)
    setattr(user_1,"Churn_Reason",nw_reason)
    setattr(user_1,"Percentage",prob[0][1])
    db.commit()
    return f"user will {user_1.Churn} and the reason is {nw_reason} and that's with percentage of {prob[0][1]:.2%}"

@app.post("/send_emails")

def send_emails(details:gmail, db:get_nw_db):

    churn_clients = db.query(user).filter(user.Churn == "Churn").all()
    
    for j,i in enumerate(churn_clients):
        send_email(reason=i.Churn_Reason,Sender_gmail=details.sender_gmail,password=details.password,Gmail=i.Gmail)    
        print(f"Email {j} sent")
    return "Emails sent"

@app.post("/send_one_email")

def send_email1(id:int, details:gmail, db:get_nw_db):

    churn_client = db.query(user).filter(user.Churn == "Churn", user.customerID == id).first()
    send_email(reason=churn_client.Churn_Reason,Sender_gmail=details.sender_gmail,password=details.password,Gmail=churn_client.Gmail)    
    return "Emails sent"