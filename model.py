import os
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import joblib

file_path = "dataset.csv"
df = pd.read_csv(file_path)

df['Login Time'] = pd.to_datetime(df['Login Time'])
df['Logout Time'] = pd.to_datetime(df['Logout Time'])

df['login_hour'] = df['Login Time'].dt.hour
df['logout_hour'] = df['Logout Time'].dt.hour

#print(df[['Login Time', 'Logout Time', 'login_hour', 'logout_hour']].head())

features = df[['login_hour', 'logout_hour', 'Usage Time (mins)', 'Count of Survey Attempts']]
# print(features.head())

wcss = []
K_range = range(2, 11)  # Testing k from 2 to 10

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(features)
    wcss.append(kmeans.inertia_)  # Store the WCSS (inertia)

# Plot Elbow Method graph
plt.figure(figsize=(8, 5))
plt.plot(K_range, wcss, marker='o', linestyle='--')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('(WCSS)')
plt.title('Elbow Method to Determine Optimal k')
plt.show()

optimalK=5
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

df['cluster'] = kmeans.fit_predict(features)

#print(df[['NPI', 'cluster']].head())

# Save the trained model
model_path = "kmeans_model.joblib"
joblib.dump(kmeans, model_path)
print(f"Model saved as {model_path}")

# Load the saved model
if os.path.exists(model_path):
    loaded_model = joblib.load(model_path)
    print("Model loaded successfully.")
else:
    print("Model file not found!")

input_time = input("Enter the time (HH:MM) to find the best doctors: ")
input_hour = int(input_time.split(":")[0])

centers = kmeans.cluster_centers_[:, 0]  # Extract cluster centers for login_hour
closest_cluster = np.argmin(np.abs(centers - input_hour))  # Find closest cluster

target_doctors = df[df['cluster'] == closest_cluster]['NPI']

target_doctors.to_csv("target_doctors.csv", index=False)

print(f"Exported {len(target_doctors)} target doctors to 'target_doctors.csv'")