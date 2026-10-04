<div align="center">

# 📡 Telco AI Retention Suite
### End-to-End Churn Analytics, Root-Cause Explainability (TreeSHAP) & Automated Retention Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Powered-orange?logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![XAI](https://img.shields.io/badge/Explainability-TreeSHAP-yellow)](https://shap.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  A production-grade machine learning platform that doesn't just predict customer churn — it explains the exact behavioral drivers behind each customer's risk and dispatches personalized, automated retention campaigns in real-time.
</p>

</div>

---

<!-- 
💡 ملاحظة: يمكنك وضع ملف GIF التوضيحي هنا بعد تسجيل الشاشة 
ضع الصورة أو الـ GIF في مجلد assets/ واستبدل الرابط أدناه
-->
<div align="center">
  <img src="https://raw.githubusercontent.com/MahmoudDahees/Telco-AI-Retention-Suite/main/assets/demo.gif" alt="Platform Demo" width="85%" onerror="this.style.display='none'"/>
</div>

---

## 📌 Table of Contents
* [Key Highlights](#-key-highlights)
* [System Architecture](#-system-architecture)
* [Feature Breakdown](#-feature-breakdown)
* [Tech Stack](#-tech-stack)
* [Project Directory Tree](#-project-directory-tree)
* [Installation & Setup](#-installation--setup)
* [Running the Application](#-running-the-application)
* [API Endpoints Reference](#-api-endpoints-reference)
* [Author](#-author)

---

## ✨ Key Highlights

* **🎯 Production ML Pipeline:** High-performance binary classification model using **XGBoost Classifier** handled with SMOTE for class imbalance mitigation and Stratified K-Fold validation.
* **🔍 Explainable AI (TreeSHAP):** Millisecond-level inference decoding *which specific feature* (e.g., Monthly Charges, Contract Type, Fiber Optic issues) tipped the scale toward churning.
* **📧 Automated Retention Marketing:** Automatic mapping from SHAP driver to 18+ tailored, responsive **HTML email retention templates** ready for broadcast or single-dispatch via SMTP.
* **💻 Executive Analytics Portal:** High-end, responsive **Streamlit UI** customized with modern CSS metrics, Plotly interactive graphs, and database lifecycle management.
* **⚡ Robust REST API:** Built with **FastAPI**, backed by SQLAlchemy ORM with plug-and-play capability for **SQLite** (instant local run) or **MySQL** (enterprise deployment).

---

## 🏗️ System Architecture

```text
┌────────────────────────────────────────────────────────┐
│                   Streamlit Frontend                   │
│      (Executive Dashboard, CRUD Portal, Mail Dispatch) │
└───────────────────────────┬────────────────────────────┘
                            │
                      HTTP REST API
                            │
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
├────────────────────────────┬───────────────────────────┤
│    XGBoost + TreeSHAP      │      SQLAlchemy ORM       │
│  Inference & Explain Engine│   (Session & DB Router)   │
├────────────────────────────┼───────────────────────────┤
│    Automated SMTP Engine   │   SQLite / MySQL Server   │
│  Tailored HTML Campaigns   │     Customer Database     │
└────────────────────────────┴───────────────────────────┘
🧩 Feature Breakdown1. 📊 Real-Time Analytics DashboardLive KPIs: Total Profiles, At-Risk Accounts, Churn Rate %, and Average Monthly Spend.Churn segmentation chart and top aggregated SHAP churn drivers across the enterprise portfolio.Complete inspectable database table view.2. 🔮 Real-Time Scoring & OnboardingComprehensive multi-field ingestion (Demographics, Subscribed Services, Account Metrics).Simultaneous probability scoring, SHAP-derived driver allocation, and automated database persistence.3. ✏️ Profile Adjustment & Re-scoringSearch accounts by unique Customer ID.Modify service parameters (e.g., upgrade contract, downgrade pricing tier) and re-evaluate churn probability instantaneously.4. 📧 Automated Retention DispatcherSingle Dispatch: Target an individual at-risk customer with a promotional retention voucher tailored to their primary churn factor.Bulk Broadcast: Query all churn-prone customers in the database and trigger parallel HTML campaign deliveries via Gmail SMTP App Passwords.5. 🗑️ Database AdministrationSingle-customer removal or full-database purge with safety confirmations.🛠️ Tech StackComponentTechnology / LibraryLanguagePython 3.10+Machine LearningXGBoost, Scikit-Learn, Imbalanced-Learn (SMOTE)Model ExplainabilitySHAP (TreeExplainer)Backend FrameworkFastAPI, Uvicorn, Pydantic v2Database & ORMSQLAlchemy 2.0, SQLite (Default), PyMySQLFrontend FrameworkStreamlit, Plotly ExpressEmail ProtocolPython smtplib, email.message.EmailMessage📂 Project Directory TreePlaintextTelco-AI-Retention-Suite/
│
├── Dataset/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Historical training dataset
│
├── Project files/
│   ├── scaler.pkl                             # Fitted StandardScaler object
│   └── xgb_model.pkl                          # Trained XGBoost binary classifier
│
├── .env.example                               # Sample environment variables
├── .gitignore                                 # Git ignore patterns
├── database.py                                # SQLAlchemy engine & session setup
├── Main.py                                    # FastAPI server & inference logic
├── models.py                                  # SQLAlchemy customer schema
├── app.py                                     # Streamlit interactive UI application
├── The Churn prediction model.py             # Model training & exploration script
├── requirements.txt                           # Frozen project dependencies
└── README.md                                  # Documentation
⚙️ Installation & Setup1. Clone the RepositoryBashgit clone [https://github.com/MahmoudDahees/Telco-AI-Retention-Suite.git](https://github.com/MahmoudDahees/Telco-AI-Retention-Suite.git)
cd Telco-AI-Retention-Suite
2. Create and Activate Virtual EnvironmentBash# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install DependenciesBashpip install --upgrade pip
pip install -r requirements.txt
4. Configure Environment VariablesCreate your local .env file from the provided template:Bash# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
Database Configuration:By default, .env uses SQLite: DB_URL=sqlite:///./customers.db (Requires zero configuration, works instantly).If you want to use MySQL, update the URL to:DB_URL=mysql+pymysql://username:password@localhost:3306/customers🚀 Running the ApplicationYou will need two terminal tabs:Tab 1: Start the FastAPI BackendBashuvicorn Main:app --reload --port 8000
API Home: http://127.0.0.1:8000/Interactive OpenAPI Docs (Swagger UI): http://127.0.0.1:8000/docsTab 2: Start the Streamlit Web ApplicationBashstreamlit run app.py
Dashboard Interface: http://localhost:8501🔌 API Endpoints ReferenceMethodEndpointDescriptionGET/Retrieves all registered customer records from the database.POST/predictPredicts churn risk, computes SHAP root-cause, and stores record.GET/get_user/{customer_id}Fetches a single customer's full record by ID.PUT/update_user?id={id}Updates client features and recalculates churn probability.DELETE/delete_user?id={id}Removes a customer record by ID.DELETE/delete_all_usersPurges all customer data from the database.POST/send_one_email?id={id}Sends a tailored retention email to an individual churn-risk customer.POST/send_emailsDispatches retention campaigns in bulk to all customers marked as churn.👨‍💻 AuthorMahmoud DaheesGitHub: @MahmoudDaheesLinkedIn: Mahmoud Dahees
