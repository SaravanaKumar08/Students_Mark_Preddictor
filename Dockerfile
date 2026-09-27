# Base image: official Python 3.11 (slim = smaller image size)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first — Docker caches this layer separately.
# If only app code changes, this pip install layer is reused (faster rebuilds).
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files needed by both the API and training services.
# student_model.pkl is NOT copied here — it does not exist on fresh clone.
# The real model is written here by the train service via bind mount in docker-compose.yml.
COPY app.py train_model.py ./

# Create an empty placeholder so the image always builds successfully
# even before the first training run has produced a real .pkl file.
RUN touch student_model.pkl

# Document which port this container listens on
EXPOSE 5000

# gunicorn = production WSGI server instead of Flask dev server
# app:app means: file "app.py", Flask object named "app" inside it
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]