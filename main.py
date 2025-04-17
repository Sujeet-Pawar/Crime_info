from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the dataset
try:
    df = pd.read_csv("karnataka_crime_merged_with_pdf_districts.csv")
    df.fillna(0, inplace=True)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]  # sanitize column names
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()

# Home route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Karnataka Crime API"})

# All data
@app.route("/api/all", methods=["GET"])
def get_all_data():
    return df.to_json(orient="records")

# Filter by district
@app.route("/api/district/<district>", methods=["GET"])
def get_by_district(district):
    filtered = df[df["district"].str.lower() == district.lower()]
    if filtered.empty:
        return jsonify({"error": "District not found"}), 404
    return filtered.to_json(orient="records")

# Filter by year
@app.route("/api/year/<int:year>", methods=["GET"])
def get_by_year(year):
    filtered = df[df["year"] == year]
    if filtered.empty:
        return jsonify({"error": "Year not found"}), 404
    return filtered.to_json(orient="records")

# Top 5 crime-prone districts
@app.route("/api/top-crime-districts", methods=["GET"])
def top_crime_districts():
    year = request.args.get("year", type=int)
    if year:
        data = df[df["year"] == year]
    else:
        data = df
    if data.empty:
        return jsonify({"error": "No data available"}), 404
    top = data.groupby("district")["total_crimes"].sum().sort_values(ascending=False).head(5)
    return top.reset_index().to_json(orient="records")

# Summary stats
@app.route("/api/stats", methods=["GET"])
def stats():
    total_crimes = int(df["total_crimes"].sum())
    unique_years = sorted(df["year"].unique().tolist())
    total_districts = df["district"].nunique()
    return jsonify({
        "total_crimes": total_crimes,
        "available_years": unique_years,
        "districts_covered": total_districts
    })

# Get available filters
@app.route("/api/filters", methods=["GET"])
def filters():
    return jsonify({
        "districts": sorted(df["district"].unique().tolist()),
        "years": sorted(df["year"].unique().tolist())
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
