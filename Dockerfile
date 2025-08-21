FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium + Chrome
ENV CHROMIUM_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port for Render
EXPOSE 8000

# Start backend (FastAPI with uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
