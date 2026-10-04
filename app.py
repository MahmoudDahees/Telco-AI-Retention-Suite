import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -------------------------------------------------------------
# 1. Page Configuration & Custom Theme
# -------------------------------------------------------------
st.set_page_config(
    page_title="Telco Churn Analytics & Retention Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://127.0.0.1:8000"

# Custom Modern CSS (Navy / Royal Blue / Sky Blue Palette)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    /* Top Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        padding: 30px 35px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.25);
    }
    
    .hero-title {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 0;
        color: #ffffff;
    }
    
    .hero-subtitle {
        font-size: 14px;
        color: #bae6fd;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Stat Cards */
    .metric-card {
        background: white;
        padding: 20px 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #0284c7;
    }
    
    .metric-val {
        font-size: 26px;
        font-weight: 700;
        color: #0f172a;
        margin: 4px 0 0 0;
    }
    
    .metric-lbl {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.5px;
    }
    
    /* Result Badge Cards */
    .result-card-churn {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        border-left: 6px solid #e11d48;
        padding: 20px;
        border-radius: 12px;
        color: #9f1239;
    }
    
    .result-card-safe {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-left: 6px solid #16a34a;
        padding: 20px;
        border-radius: 12px;
        color: #166534;
    }
    
    /* Custom Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. Sidebar Navigation & Global Config
# -------------------------------------------------------------
with st.sidebar:
    # بدلاً من st.image(...)
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
            <span style="font-size: 42px;">📡</span>
            <div>
                <h3 style="margin: 0; color: #0284c7; font-weight: 700;">Telco AI</h3>
                <p style="margin: 0; font-size: 12px; color: #64748b;">Retention Suite</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Navigation Menu",
        [
            "📊 Dashboard & Database",
            "🔮 Predict & Add Customer",
            "✏️ Update Customer",
            "📧 Retention Campaigns",
            "🗑️ Database Management"
        ]
    )
    
    st.markdown("---")
    st.markdown("##### 🔌 API Connection")
    st.success(f"Connected: `{API_BASE_URL}`")

# -------------------------------------------------------------
# 3. Helpers & API Handlers
# -------------------------------------------------------------
def fetch_all_users():
    try:
        res = requests.get(f"{API_BASE_URL}/", timeout=5)
        if res.status_code == 200:
            return pd.DataFrame(res.json())
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error connecting to FastAPI backend: {e}")
        return pd.DataFrame()

# -------------------------------------------------------------
# PAGE 1: Dashboard & Database
# -------------------------------------------------------------
if page == "📊 Dashboard & Database":
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Customer Portfolio & Churn Overview</h1>
        <p class="hero-subtitle">Real-time telecommunication churn metrics, SHAP reason analytics, and database records.</p>
    </div>
    """, unsafe_allow_html=True)
    
    df = fetch_all_users()
    
    if not df.empty:
        total_cust = len(df)
        churn_cust = len(df[df["Churn"] == "Churn"]) if "Churn" in df.columns else 0
        churn_rate = (churn_cust / total_cust) * 100 if total_cust > 0 else 0
        avg_monthly = df["MonthlyCharges"].mean() if "MonthlyCharges" in df.columns else 0
        
        # Summary Metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-lbl">Total Profiles</div><div class="metric-val">{total_cust:,}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-lbl">At Risk (Churn)</div><div class="metric-val" style="color: #e11d48;">{churn_cust:,}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-lbl">Churn Rate</div><div class="metric-val">{churn_rate:.1f}%</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="metric-lbl">Avg Monthly Bill</div><div class="metric-val">${avg_monthly:.2f}</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualizations
        col_left, col_right = st.columns([1, 1])
        with col_left:
            if "Churn" in df.columns:
                fig_pie = px.pie(
                    df, names="Churn",
                    title="<b>Customer Retention vs Churn</b>",
                    color="Churn",
                    color_discrete_map={"Churn": "#f43f5e", "Not churn": "#0284c7"},
                    hole=0.45
                )
                fig_pie.update_layout(margin=dict(t=40, b=0, l=0, r=0))
                st.plotly_chart(fig_pie, use_container_width=True)
                
        with col_right:
            if "Churn_Reason" in df.columns and churn_cust > 0:
                reasons_df = df[df["Churn"] == "Churn"]["Churn_Reason"].value_counts().reset_index()
                reasons_df.columns = ["Factor", "Count"]
                fig_bar = px.bar(
                    reasons_df, x="Factor", y="Count",
                    title="<b>Primary Churn Drivers (SHAP Key Factors)</b>",
                    color="Count",
                    color_continuous_scale="Blues"
                )
                fig_bar.update_layout(margin=dict(t=40, b=0, l=0, r=0))
                st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("### 📋 Stored Customers Registry")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("No customers found in database. Start by predicting/adding profiles.")

# -------------------------------------------------------------
# PAGE 2: Predict & Add Customer
# -------------------------------------------------------------
elif page == "🔮 Predict & Add Customer":
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Real-Time Churn Scoring & Ingestion</h1>
        <p class="hero-subtitle">Input customer demographic & service details to predict churn risk and extract top SHAP drivers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("predict_form"):
        st.subheader("1. Customer Profile & Demographics")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            SeniorCitizen = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        with c2:
            Partner = st.selectbox("Partner", ["Yes", "No"])
            Dependents = st.selectbox("Dependents", ["Yes", "No"])
        with c3:
            tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
            Gmail = st.text_input("Customer Email", "customer@example.com")
        with c4:
            MonthlyCharges = st.number_input("Monthly Charges ($)", min_value=0.0, value=75.5)
            TotalCharges = st.number_input("Total Charges ($)", min_value=0.0, value=900.0)
            
        st.subheader("2. Subscribed Services")
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
            MultipleLines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
            InternetService = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        with s2:
            OnlineSecurity = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
            OnlineBackup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
            DeviceProtection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        with s3:
            TechSupport = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
            StreamingTV = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
            StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        with s4:
            Contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
            PaymentMethod = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
            ])
            
        submitted = st.form_submit_button("🚀 Run ML Model & Save Customer", use_container_width=True)
        
    if submitted:
        payload = {
            "gender": gender,
            "SeniorCitizen": SeniorCitizen,
            "Partner": Partner,
            "Dependents": Dependents,
            "tenure": tenure,
            "PhoneService": PhoneService,
            "MultipleLines": MultipleLines,
            "InternetService": InternetService,
            "OnlineSecurity": OnlineSecurity,
            "OnlineBackup": OnlineBackup,
            "DeviceProtection": DeviceProtection,
            "TechSupport": TechSupport,
            "StreamingTV": StreamingTV,
            "StreamingMovies": StreamingMovies,
            "Contract": Contract,
            "PaperlessBilling": PaperlessBilling,
            "PaymentMethod": PaymentMethod,
            "MonthlyCharges": float(MonthlyCharges),
            "TotalCharges": float(TotalCharges),
            "Gmail": Gmail
        }
        
        with st.spinner("Processing features through XGBoost & SHAP explainer..."):
            try:
                res = requests.post(f"{API_BASE_URL}/predict", json=payload)
                if res.status_code == 200:
                    st.success("Analysis Complete & Record Stored Successfully!")
                    st.markdown(f"""
                    <div class="result-card-churn" style="border-left-color: #0284c7; background: #f0f9ff; color: #0369a1;">
                        <h4 style="margin: 0 0 10px 0;">🎯 Pipeline Prediction Response</h4>
                        <p style="font-size: 16px; margin: 0; font-weight: 600;">{res.json()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Error from server ({res.status_code}): {res.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {e}")

# -------------------------------------------------------------
# PAGE 3: Update Customer
# -------------------------------------------------------------
elif page == "✏️ Update Customer":
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Modify Customer Data & Re-evaluate</h1>
        <p class="hero-subtitle">Retrieve existing records by ID, adjust their plan parameters, and re-compute churn metrics.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_search, _ = st.columns([1, 2])
    with col_search:
        cust_id = st.number_input("Enter Customer ID to Fetch", min_value=1, step=1)
        fetch_btn = st.button("🔍 Search Customer Record", use_container_width=True)
        
    if fetch_btn:
        res = requests.get(f"{API_BASE_URL}/get_user/{cust_id}")
        if res.status_code == 200 and res.json():
            st.session_state["fetched_user"] = res.json()
            st.success(f"Customer #{cust_id} record retrieved.")
        else:
            st.error(f"Customer with ID {cust_id} not found.")
            st.session_state.pop("fetched_user", None)
            
    if "fetched_user" in st.session_state:
        u = st.session_state["fetched_user"]
        with st.form("update_form"):
            st.markdown(f"#### Updating Details for Customer ID: `{u.get('customerID', cust_id)}`")
            u1, u2, u3, u4 = st.columns(4)
            with u1:
                u_gender = st.selectbox("Gender", ["Male", "Female"], index=0 if u.get("gender") == "Male" else 1)
                u_senior = st.selectbox("Senior Citizen", [0, 1], index=0 if u.get("SeniorCitizen") == 0 else 1)
                u_partner = st.selectbox("Partner", ["Yes", "No"], index=0 if u.get("Partner") == "Yes" else 1)
                u_dependents = st.selectbox("Dependents", ["Yes", "No"], index=0 if u.get("Dependents") == "Yes" else 1)
            with u2:
                u_tenure = st.number_input("Tenure", min_value=0, max_value=100, value=int(u.get("tenure", 1)))
                u_phone = st.selectbox("Phone Service", ["Yes", "No"], index=0 if u.get("PhoneService") == "Yes" else 1)
                u_mult = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"], index=["No", "Yes", "No phone service"].index(u.get("MultipleLines", "No")))
                u_net = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"], index=["Fiber optic", "DSL", "No"].index(u.get("InternetService", "Fiber optic")))
            with u3:
                u_sec = st.selectbox("Online Security", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(u.get("OnlineSecurity", "No")))
                u_bkp = st.selectbox("Online Backup", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(u.get("OnlineBackup", "No")))
                u_dev = st.selectbox("Device Protection", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(u.get("DeviceProtection", "No")))
                u_tech = st.selectbox("Tech Support", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(u.get("TechSupport", "No")))
            with u4:
                u_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(u.get("StreamingTV", "No")))
                u_mov = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(u.get("StreamingMovies", "No")))
                u_contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"], index=["Month-to-month", "One year", "Two year"].index(u.get("Contract", "Month-to-month")))
                u_paper = st.selectbox("Paperless Billing", ["Yes", "No"], index=0 if u.get("PaperlessBilling") == "Yes" else 1)
                
            u_pay = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
            ], index=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"].index(u.get("PaymentMethod", "Electronic check")))
            
            p1, p2 = st.columns(2)
            with p1:
                u_month = st.number_input("Monthly Charges ($)", value=float(u.get("MonthlyCharges", 50.0)))
            with p2:
                u_tot = st.number_input("Total Charges ($)", value=float(u.get("TotalCharges", 50.0)))
                
            update_submit = st.form_submit_button("💾 Save Updates & Re-Calculate Risk", use_container_width=True)
            
        if update_submit:
            update_payload = {
                "gender": u_gender,
                "SeniorCitizen": u_senior,
                "Partner": u_partner,
                "Dependents": u_dependents,
                "tenure": u_tenure,
                "PhoneService": u_phone,
                "MultipleLines": u_mult,
                "InternetService": u_net,
                "OnlineSecurity": u_sec,
                "OnlineBackup": u_bkp,
                "DeviceProtection": u_dev,
                "TechSupport": u_tech,
                "StreamingTV": u_tv,
                "StreamingMovies": u_mov,
                "Contract": u_contract,
                "PaperlessBilling": u_paper,
                "PaymentMethod": u_pay,
                "MonthlyCharges": u_month,
                "TotalCharges": u_tot
            }
            
            res_put = requests.put(f"{API_BASE_URL}/update_user?id={cust_id}", json=update_payload)
            if res_put.status_code == 200:
                st.success("Customer record updated successfully!")
                st.info(res_put.json())
            else:
                st.error(f"Failed to update: {res_put.text}")

# -------------------------------------------------------------
# PAGE 4: Retention Campaigns (Email Dispatcher)
# -------------------------------------------------------------
elif page == "📧 Retention Campaigns":
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Automated Retention Email Dispatcher</h1>
        <p class="hero-subtitle">Trigger customized, SHAP-tailored HTML retention offers to users marked as Churn risk.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🔐 SMTP Sender Credentials")
    e1, e2 = st.columns(2)
    with e1:
        sender_email = st.text_input("Sender Gmail Address", placeholder="your_email@gmail.com")
    with e2:
        sender_password = st.text_input("Gmail App Password (16 Characters)", type="password", help="Use Google Account App Password, not personal password.")
        
    st.markdown("---")
    
    tab_bulk, tab_single = st.tabs(["🚀 Broadcast to All Churn Customers", "🎯 Target Single Customer"])
    
    with tab_bulk:
        st.markdown("##### Bulk Dispatch")
        st.write("This will automatically query all customers with `Churn == 'Churn'`, compose their specific HTML retention template based on their `Churn_Reason`, and send it.")
        if st.button("📤 Send Retention Campaigns to ALL Churn Users", use_container_width=True):
            if not sender_email or not sender_password:
                st.warning("Please provide both sender Gmail and App Password above.")
            else:
                with st.spinner("Dispatching automated emails..."):
                    payload = {"sender_gmail": sender_email, "password": sender_password}
                    try:
                        res = requests.post(f"{API_BASE_URL}/send_emails", json=payload)
                        if res.status_code == 200:
                            st.success(f"Dispatch Complete: {res.json()}")
                        else:
                            st.error(f"Error sending emails: {res.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")
                        
    with tab_single:
        st.markdown("##### Targeted Single Dispatch")
        target_id = st.number_input("Target Customer ID", min_value=1, step=1)
        if st.button("📧 Send Targeted Retention Email", use_container_width=True):
            if not sender_email or not sender_password:
                st.warning("Please provide credentials above.")
            else:
                with st.spinner(f"Sending tailored offer to Customer #{target_id}..."):
                    payload = {"sender_gmail": sender_email, "password": sender_password}
                    try:
                        res = requests.post(f"{API_BASE_URL}/send_one_email?id={target_id}", json=payload)
                        if res.status_code == 200:
                            st.success(f"Email sent successfully: {res.json()}")
                        else:
                            st.error(f"Failed to dispatch: {res.text}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

# -------------------------------------------------------------
# PAGE 5: Database Management
# -------------------------------------------------------------
elif page == "🗑️ Database Management":
    st.markdown("""
    <div class="hero-container" style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%);">
        <h1 class="hero-title">Database Administration</h1>
        <p class="hero-subtitle">Delete individual user records or perform complete database purges.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_del_single, col_del_all = st.columns(2)
    
    with col_del_single:
        st.markdown("### 👤 Delete Specific Customer")
        del_id = st.number_input("Customer ID to Remove", min_value=1, step=1)
        if st.button("🗑️ Delete Customer", use_container_width=True):
            try:
                res = requests.delete(f"{API_BASE_URL}/delete_user?id={del_id}")
                if res.status_code == 200:
                    st.success(f"Customer #{del_id} deleted successfully.")
                else:
                    st.error(f"Failed to delete: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")
                
    with col_del_all:
        st.markdown("### ⚠️ Purge Entire Database")
        st.write("This action will permanently delete all records from the database.")
        confirm = st.checkbox("I understand that this action is irreversible.")
        if st.button("🚨 Wipe Entire Database", disabled=not confirm, use_container_width=True):
            try:
                res = requests.delete(f"{API_BASE_URL}/delete_all_users")
                if res.status_code == 200:
                    st.success("All customer records have been wiped.")
                else:
                    st.error(f"Failed to wipe records: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")