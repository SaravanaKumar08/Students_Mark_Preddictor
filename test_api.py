import requests

# The local URL where Flask is running — must match app.py's port
BASE_URL = "http://127.0.0.1:5000"


def test_health():
    # Confirm the API root endpoint responds before running predictions
    response = requests.get(BASE_URL)
    print(f"Health check: {response.status_code} — {response.text}")


def test_predict(name, hours):
    # Send a POST request with the student's hours as JSON body
    payload  = {"hours_studied": hours}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    result   = response.json()

    print(
        f"{name:<10}  "
        f"{hours} hrs  →  "
        f"{result['predicted_marks']} marks  →  Grade: {result['grade']}"
    )


if __name__ == "__main__":
    test_health()
    print("-" * 50)

    # Test with different students and study hours
    students = [
        ("Ravi",   3),
        ("Priya",  7),
        ("Kumar",  10),
        ("Meena",  1),
        ("Arjun",  9),
    ]
    for name, hours in students:
        test_predict(name, hours)