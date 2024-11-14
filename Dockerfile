# Use a base image with Python
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Set working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . .

# Expose port for the web server (adjust according to your needs)
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]