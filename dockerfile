FROM python:3.12-slim-bookworm

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary directories
COPY src ./src
COPY seed_data ./seed_data

# Set permissions & switch user
RUN chown -R appuser:appuser /app
USER appuser

# Create log directory
RUN mkdir -p /app/logs

CMD ["uvicorn", "travel_assistant.main:app", "--host", "0.0.0.0", "--port", "80"]