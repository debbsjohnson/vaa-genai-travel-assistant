FROM python:3.12

WORKDIR /app

# Update package manager and install security updates
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y && apt-get autoremove -y && apt-get clean

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "travel_assistant.main:app", "--host", "0.0.0.0", "--port", "80"]