# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ .

# Expose the app port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
