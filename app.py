from flask import Flask, render_template, request, jsonify, session
import time
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

DISEASES = ["cold", "flu", "migraine", "allergy", "covid-19", "sinusitis"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/update-python", methods=["POST"])
def update_python():
    data = request.get_json()
    symptoms = data.get("input", "").lower()
    
    diagnosis = random.choice(DISEASES)

    if "healthRecords" not in session:
        session["healthRecords"] = []
    session["healthRecords"].append(symptoms)
    
    return jsonify({"message": "Data received", "diagnosis": diagnosis})

@app.route("/output")
def output():
    time.sleep(7)  
    diagnosis = random.choice(DISEASES)
    return diagnosis

if __name__ == "__main__":
    app.run(debug=True)
