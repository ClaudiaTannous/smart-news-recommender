# Use a lightweight base image with Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Optional: Install system packages needed for some Python libs
RUN apt-get update && apt-get install -y build-essential

# Copy your entire project into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to distinguish cloud vs local
ENV GCP_DEPLOYMENT=1

# Expose the port FastAPI will use
EXPOSE 8080

# Run your FastAPI app via run_server.py
CMD ["python", "run_server.py"]
