FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full application code and pre-warmed .cache
COPY . .

# Cloud Run injects PORT environment variable (default 8080)
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "streamlit run app/main.py --server.port=${PORT} --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false"]