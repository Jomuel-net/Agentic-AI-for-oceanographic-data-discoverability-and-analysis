import json
import os

print("Working directory:", os.getcwd())

try:
    with open("DataDeployment.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        print("JSON loaded successfully!")
        print(data)
except Exception as e:
    print("Error:", e)
