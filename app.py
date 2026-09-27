from flask import Flask, request, jsonify
import joblib

# ------------------------------------------------------------------
# Create the Flask application instance
# ------------------------------------------------------------------
app = Flask(__name__)



@app.route("/predict", methods=["POST"])
def predict():
    # ------------------------------------------------------------------
    # STEP 1: Read the JSON body sent by the caller
    # Expected format: {"hours_studied": 7}
    # ------------------------------------------------------------------
    data  = request.json
    hours = data["hours_studied"]

    # ------------------------------------------------------------------
    # STEP 2: Pass the input to the model and get a prediction
    # model.predict() needs a 2D list: [[value]]
    # ------------------------------------------------------------------
    predicted_marks = float(model.predict([[hours]])[0])

    # ------------------------------------------------------------------
    # STEP 3: Derive a letter grade from the numeric score
    # ------------------------------------------------------------------
    if   predicted_marks >= 90: grade = "A+"
    elif predicted_marks >= 75: grade = "A"
    elif predicted_marks >= 60: grade = "B"
    elif predicted_marks >= 50: grade = "C"
    else:                        grade = "Fail"

    # ------------------------------------------------------------------
    # STEP 4: Return the result as JSON to the caller
    # ------------------------------------------------------------------
    return jsonify({
        "hours_studied":  hours,
        "predicted_marks": round(predicted_marks, 1),
        "grade":           grade
    })


if __name__ == "__main__":
    # debug=True auto-reloads when you edit the file (dev mode only)
    app.run(debug=True)