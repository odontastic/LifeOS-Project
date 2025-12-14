# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

ENV PYTHONPATH=/app

# Copy the dependency file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
# Copy the application source code to /app/src
COPY ./src ./src

# Command to run the application using the package structure
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
