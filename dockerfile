FROM python:3.12-slim-bookworm

# 1) create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app

# 2) install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) copy your code
COPY src/ ./src/

# 4) copy the seed_data into the package path your code expects
COPY seed_data/ ./src/travel_assistant/seed_data/

# (optional) verify at build-time
RUN ls -R /app/src/travel_assistant/seed_data

# 5) set permissions & user
RUN chown -R appuser:appuser /app
USER appuser
RUN mkdir -p /app/logs

# 6) start the app
CMD ["uvicorn", "travel_assistant.main:app", "--host", "0.0.0.0", "--port", "80"]
