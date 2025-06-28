# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit-specific config to run in Docker
EXPOSE 8501

# Entrypoint
CMD ["streamlit", "run", "automated.py", "--server.port=8501", "--server.address=0.0.0.0"]
