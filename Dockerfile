# Use official Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libffi-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and entrypoint
COPY . .

# Make sure the entrypoint script is executable
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8080

# Use entrypoint.sh to initialize etcd and start app
ENTRYPOINT ["./entrypoint.sh"]
