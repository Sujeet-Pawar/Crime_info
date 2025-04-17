# backend/app.py
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

try:
    df = pd.read_csv("karnataka_crime_merged_with_pd_districts.csv")
except Exception as e:
    print(f"Error loading data: {e}")
    df = None

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Karnataka Crime API"})
# Flask app with route aggregation