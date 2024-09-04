# Start with a base image that has Python installed
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install build-essential and venv for compiling native extensions and creating virtual environments
RUN apt-get update && apt-get install -y build-essential python3-venv

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate the virtual environment and install dependencies
RUN /opt/venv/bin/pip install --upgrade pip
COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN /opt/venv/bin/pip install gunicorn

# Copy the rest of the application code
COPY . .

# Remove any .pyc files and __pycache__ directories
RUN find . -name "*.pyc" -exec rm -f {} + && find . -name "__pycache__" -exec rm -rf {} +

RUN chmod -R 777 /app/core/docs
RUN chmod -R 777 /app/logs

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Set the environment variables for using the virtual environment
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app

# Expose port 5000
EXPOSE 5000

# Specify the command to run the application using Gunicorn
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:5000", "app:app"]
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
