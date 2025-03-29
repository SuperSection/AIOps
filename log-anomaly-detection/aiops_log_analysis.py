import re
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


# Read log file
log_file_path = "app.log"

with open(log_file_path, "r") as file:
  logs = file.readlines()


# Parse logs into a structured DataFrame
data = []

for log in logs:
  match = re.match(r"\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\] (\w+) (\S+) - (.+)", log.strip())
  if match:
    timestamp, level, service, message = match.groups()
    data.append([timestamp, level, service, message])

df = pd.DataFrame(data, columns=["timestamp", "level", "service", "message"])

# Convert timestamp to datetime format for sorting
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Assign numeric scores to log levels
level_mapping = {"INFO": 1, "WARN": 2, "ERROR": 3, "CRITICAL": 4}
df["level_score"] = df["level"].map(level_mapping)

# Add message length as a new feature
df["message_length"] = df["message"].apply(len)


# AI Model for Anomaly Detection (Isolation Forest)
model = IsolationForest(contamination=0.1, random_state=42)   # Lower contamincation for best accuracy
df["anomaly"] = model.fit_predict(df[["level_score", "message_length"]])

# Mark anomalies in a readable format
df["is_anomaly"] = df["anomaly"].apply(lambda x: "❌ Anomaly" if x == -1 else "✅ Normal")

# Print only detected anomalies
anomalies = df[df["is_anomaly"] == "❌ Anomaly"]
print("\n==== 🔍 Detected Anomalies ====\n", anomalies)
