================================================================================
          TELCO AI RETENTION SUITE - COMPLETE PROJECT DOCUMENTATION
================================================================================

An End-to-End Enterprise Solution for Churn Prediction, Root-Cause Explainability 
(SHAP), and Automated Retention Marketing Workflows.

Author: Mahmoud Dahees
GitHub: https://github.com/MahmoudDahees


--------------------------------------------------------------------------------
1. PROJECT OVERVIEW
--------------------------------------------------------------------------------
Customer churn is one of the highest priority operational challenges across the 
telecommunication sector. Telco AI Retention Suite bridges the gap between machine 
learning inference and marketing operations through three synchronized layers:

1. High-Performance Prediction: An optimized XGBoost Classifier trained on SMOTE-
   resampled data to accurately forecast churn risk under imbalanced conditions.
2. Explainable AI (SHAP): Uses SHAP value decomposition to explain the exact 
   behavioral or financial driver that tipped the scale toward churning.
3. Automated Retention Campaigns: Maps the dominant SHAP driver to 18+ responsive 
   HTML retention offers, dispatched via automated SMTP email infrastructure.
4. Interactive Management Suite: A full-stack Streamlit frontend powered by a 
   FastAPI REST backend with persistent SQLAlchemy ORM storage.


--------------------------------------------------------------------------------
2. KEY HIGHLIGHTS & CAPABILITIES
--------------------------------------------------------------------------------
* Real-Time Scoring: Demographic, account, and service parameters are ingested, 
  scaled, and scored instantaneously.
* Root-Cause Attribution: Automated identification of whether churn is driven by 
  pricing (MonthlyCharges, TotalCharges), contract inflexibility, network quality, 
  or service support gaps.
* Automated Email Dispatch: Bulk broadcast to all at-risk clients or precision 
  targeting of a single customer with pre-configured retention vouchers.
* Full CRUD Control: Fetch, review, update contract details, re-calculate risk, 
  and purge database records cleanly.
* Database-Agnostic: Zero-setup local operation via SQLite with seamless 
  production configuration for MySQL or PostgreSQL.


--------------------------------------------------------------------------------
3. SYSTEM ARCHITECTURE
--------------------------------------------------------------------------------

[ Streamlit Dashboard & UI ]
            │
            ▼  (HTTP REST Calls)
   [ FastAPI Backend Engine ]
      ├── XGBoost Classifier (Churn Prediction)
      ├── SHAP Explainer (Root-Cause Driver Detection)
      ├── SQLAlchemy ORM ──▶ [ SQLite / MySQL Database ]
      └── SMTP Email Engine ──▶ [ Tailored HTML Retention Campaigns ]


--------------------------------------------------------------------------------
4. TECH STACK
--------------------------------------------------------------------------------
* Programming Language: Python 3.10+
* Machine Learning: XGBoost, Scikit-Learn, Imbalanced-Learn (SMOTE)
* Model Explainability: SHAP (SHapley Additive exPlanations)
* Backend API: FastAPI, Uvicorn, Pydantic v2
* Database & ORM: SQLAlchemy 2.0, SQLite (Default), PyMySQL
* Frontend & Visualization: Streamlit, Plotly Express
* Email Protocols: smtplib, email.message.EmailMessage


--------------------------------------------------------------------------------
5. RECOMMENDED PROJECT DIRECTORY TREE
--------------------------------------------------------------------------------

Telco-AI-Retention-Suite/
│
├── Dataset/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv   # Telco customer dataset
│
├── Project files/
│   ├── scaler.pkl                             # Fitted StandardScaler object
│   └── xgb_model.pkl                          # Trained XGBoost binary model
│
├── .env.example                               # Environment template
├── .gitignore                                 # Git ignore patterns
├── database.py                                # SQLAlchemy database setup
├── Main.py                                    # FastAPI application & ML logic
├── models.py                                  # SQLAlchemy customer schema
├── app.py                                     # Streamlit dashboard interface
├── The Churn prediction model.py             # Exploration & training script
├── requirements.txt                           # Frozen package dependencies
└── README.txt                                 # Documentation


--------------------------------------------------------------------------------
6. QUICKSTART & LOCAL SETUP
--------------------------------------------------------------------------------

Step 1: Clone the repository
------------------------------------
git clone https://github.com/MahmoudDahees/Telco-AI-Retention-Suite.git
cd Telco-AI-Retention-Suite


Step 2: Create and activate virtual environment
------------------------------------
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS / Linux:
python3 -m venv venv
source venv/bin/activate


Step 3: Install all required dependencies
------------------------------------
pip install --upgrade pip
pip install -r requirements.txt


Step 4: Configure environment variables
------------------------------------
# Windows:
copy .env.example .env

# macOS / Linux:
cp .env.example .env

* By default, .env uses: DB_URL=sqlite:///./customers.db
  This requires zero setup and works immediately.
* If you wish to use MySQL instead, uncomment and configure:
  DB_URL=mysql+pymysql://username:password@localhost:3306/customers


--------------------------------------------------------------------------------
7. RUNNING THE APPLICATION
--------------------------------------------------------------------------------

Launch two separate terminal windows inside the project directory:

Terminal 1: Start the FastAPI Backend
------------------------------------
uvicorn Main:app --reload --port 8000

* API Root: http://127.0.0.1:8000/
* Interactive Swagger Docs: http://127.0.0.1:8000/docs


Terminal 2: Start the Streamlit Interface
------------------------------------
streamlit run app.py

* Dashboard URL: http://localhost:8501


--------------------------------------------------------------------------------
8. API ENDPOINTS REFERENCE
--------------------------------------------------------------------------------

Method    Endpoint                 Description
--------------------------------------------------------------------------------
GET       /                        Retrieves all customer records from DB.
POST      /predict                 Runs XGBoost + SHAP, returns risk & saves user.
GET       /get_user/{customer_id}  Fetches a single customer record by ID.
PUT       /update_user?id={id}     Updates profile parameters and re-evaluates risk.
DELETE    /delete_user?id={id}     Deletes an individual customer by ID.
DELETE    /delete_all_users        Clears all customer entries from database.
POST      /send_one_email?id={id}  Sends targeted SHAP retention email to one client.
POST      /send_emails             Broadcasts tailored emails to all churn profiles.


--------------------------------------------------------------------------------
9. MEDIA & DEMO DISPLAY (FOR GITHUB)
--------------------------------------------------------------------------------
To display recordings or animated demos on GitHub:
1. Record a 15-second walkthrough using tools like ScreenToGif or OBS.
2. Save the output as demo.gif inside an assets/ folder in your repository.
3. You can reference it directly in Markdown or drag-and-drop an MP4 video 
   directly into GitHub's file editor.


--------------------------------------------------------------------------------
10. AUTHOR & CONTACT
--------------------------------------------------------------------------------
Mahmoud Dahees
GitHub: https://github.com/MahmoudDahees
LinkedIn: https://www.linkedin.com/in/mahmouddahees
================================================================================
