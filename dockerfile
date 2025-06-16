FROM python:3.12-slim-bookworm

RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your application code AND seed data
COPY . .

# (OPTIONAL) verify it’s there during build
RUN ls -l /app/seed_data

RUN chown -R appuser:appuser /app
USER appuser
RUN mkdir -p /app/logs

CMD ["uvicorn", "travel_assistant.main:app", "--host", "0.0.0.0", "--port", "80"]
