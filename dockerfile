FROM python:3.12-slim-bookworm

# create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app files
COPY . .

# set ownership and switch user
RUN chown -R appuser:appuser /app
USER appuser

# create log directory
RUN mkdir -p /app/logs

CMD ["uvicorn", "travel_assistant.main:app", "--host", "0.0.0.0", "--port", "80"]