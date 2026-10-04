#%%
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve, f1_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import StratifiedKFold, cross_val_score
# %%
data = pd.read_csv(r'G:\ML projects\Projects\Teleco customer churn prediction project, A HUGE ONE\Dataset\WA_Fn-UseC_-Telco-Customer-Churn.csv')
data.head()
# %%
data.info()
# %%
data.describe()
# %%
data.isnull().sum()
# %%
data = data.drop(['customerID'], axis=1)
# %%
data['TotalCharges'] = pd.to_numeric(data['TotalCharges'], errors='coerce')
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
data["Churn"] = data["Churn"].map({"Yes": 1, "No": 0})
data
# %%
data.info()
# %%
corr = data.corr().sort_values(by='Churn', ascending=False)
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=False, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
# %%
corr
# %%
data = data.drop(['gender', 'PhoneService', 'MultipleLines'],axis=1)
# %%
data["YearlyCharges"] = data["MonthlyCharges"] * 12
data["SubscriptionSegment"]  = pd.cut(data["MonthlyCharges"], bins=[0, 30,60,119], labels=[0, 1, 2])
#%%
monthly_trend = data["MonthlyCharges"].groupby(data["Churn"]).mean()
fig, ax = plt.subplots(3,1,figsize=(12, 8))
sns.lineplot(data=data, x='tenure', y='MonthlyCharges', hue='Churn', palette="coolwarm", ax=ax[0])
sns.barplot(y=monthly_trend, x=monthly_trend.index, color="red", ax=ax[1])
sns.countplot(data=data, x='SubscriptionSegment', hue='Churn', palette="coolwarm", ax=ax[2])
#%%
data['Churn']
# %%
data
# %%
corr = data.corr().sort_values(by='Churn', ascending=False)
plt.figure(figsize=(12, 8))
sns.heatmap(corr, annot=False, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
# %%
data["Churn"].value_counts()
data.isnull().sum()
#%%
data["TotalCharges"] = data["TotalCharges"].fillna(0)
#%%
data.isnull().sum()
# %%
X = data.drop('Churn', axis=1)
y = data['Churn']
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#%%
Scaler = StandardScaler()
x_scaled = Scaler.fit_transform(x_train)
smote = SMOTE(random_state=42)
x_resampled, y_resampled = smote.fit_resample(x_scaled, y_train)
x_test_scaled = Scaler.transform(x_test)
# %%
x_resampled.shape, y_resampled.shape
y_resampled.value_counts()
#%%
model = LogisticRegression(class_weight='balanced', random_state=42)
model.fit(x_resampled, y_resampled)
# %%
predictions = model.predict(x_test_scaled)
report = classification_report(y_test, predictions)
print(report)
# %%
Xgb_model = XGBClassifier(eval_metric='logloss', n_estimators=1000, scale_pos_weight=1, random_state=42, depth=15, learning_rate=0.01)
Xgb_model.fit(x_resampled, y_resampled)
# %%
predictions_xgb = Xgb_model.predict(x_test_scaled)
report_xgb = classification_report(y_test, predictions_xgb)
# %%
print(report_xgb)
# %%
RandomForest_model = RandomForestClassifier(class_weight='balanced', random_state=42)
RandomForest_model.fit(x_resampled, y_resampled)
# %%
predictions_rf = RandomForest_model.predict(x_test_scaled)
report_rf = classification_report(y_test, predictions_rf)
print(report_rf)
# %%
predictions_xgb = Xgb_model.predict_proba(x_test_scaled)[:, 1]
roc_auc = roc_auc_score(y_test, predictions_xgb)
# %%
roc_auc
# %%
predictions_xgb
# %%
thresholds = []
for i in np.arange(0.1, 1, 0.05):
    threshold = i
    predictions_xgb_threshold = (predictions_xgb >= threshold).astype(int)
    report_xgb_threshold = classification_report(y_test, predictions_xgb_threshold)
    f1 = f1_score(y_test, predictions_xgb_threshold)
    print(f"Threshold: {threshold}")
    print(report_xgb_threshold)
    print(f"F1 Score: {f1}")
    print("-" * 50)
    thresholds.append((threshold, f1))
    time.sleep(1)
best_threshold = max(thresholds, key=lambda x: x[1])[0]
print(f"Best Threshold: {best_threshold}")
# %%
predictions_xgb_threshold = (predictions_xgb >= best_threshold).astype(int)
# %%
report_xgb_threshold = classification_report(y_test, predictions_xgb_threshold)
print(report_xgb_threshold)
# %%
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# %%
from imblearn.pipeline import Pipeline
pipeline = Pipeline([("scaler", StandardScaler()),
                     ("smote", SMOTE(random_state=42)),
                     ("model", XGBClassifier(eval_metric='logloss', n_estimators=1000, scale_pos_weight=1, random_state=42, depth=15, learning_rate=0.01))
                                          ])

f1_scores = []
for fold, (train_index, test_index) in enumerate(cv.split(X, y), 1):
    X_train_cv, X_val_cv = X.iloc[train_index], X.iloc[test_index]
    y_train_cv, y_val_cv = y.iloc[train_index], y.iloc[test_index]
    
    pipeline.fit(X_train_cv, y_train_cv)
    predictions_cv = pipeline.predict(X_val_cv)
    f1 = f1_score(y_val_cv, predictions_cv)
    f1_scores.append(f1)
    print(f"Fold {fold}: F1 Score = {f1}")
# %%
print(f"Cross-Validation F1 Scores: {f1_scores}")
# %%
import pickle

with open("xgb_model.pkl", "wb") as f:
    pickle.dump(Xgb_model, f)
    
with open("scaler.pkl", "wb") as f:
    pickle.dump(Scaler,f)
# %%
