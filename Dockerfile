# Used tensorflow base image
FROM tensorflow/tensorflow:2.7.0

# Seting a working directory /app
WORKDIR /app

# Copy the requirements file into working directory
COPY requirements.txt .

# Install dependencies in Container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
