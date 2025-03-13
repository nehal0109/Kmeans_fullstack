from fastapi import FastAPI
import pandas as pd
import numpy as np
import joblib

app = FastAPI()

# Load trained model
model = joblib.load("kmeans_model.joblib")

# Load dataset (assumed to be preprocessed)
file_path = "dataset.csv"
df = pd.read_csv(file_path)

df['Login Time'] = pd.to_datetime(df['Login Time'])
df['Logout Time'] = pd.to_datetime(df['Logout Time'])

df['login_hour'] = df['Login Time'].dt.hour
df['logout_hour'] = df['Logout Time'].dt.hour

df['cluster'] = model.predict(df[['login_hour', 'logout_hour', 'Usage Time (mins)', 'Count of Survey Attempts']])

@app.get("/")
def home():
    return {"message": "Doctor Recommendation API is Running"}

@app.get("/recommend/")
def recommend_doctors(time: str):
    try:
        input_hour = int(time.split(":")[0])
        centers = model.cluster_centers_[:, 0]
        closest_cluster = np.argmin(np.abs(centers - input_hour))
        target_doctors = df[df['cluster'] == closest_cluster]['NPI'].tolist()
        return {"Recommended Doctors": target_doctors}
    except Exception as e:
        return {"error": str(e)}

