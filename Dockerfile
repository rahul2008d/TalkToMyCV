# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry lock files and pyproject.toml first (for caching purposes)
COPY pyproject.toml poetry.lock* /app/

# Install Poetry (Python package manager)
RUN pip install poetry

# Install dependencies in the container using Poetry
RUN poetry install --no-root --only main

# Copy the rest of the application into the container
COPY . /app

# Expose the port that FastAPI will run on
EXPOSE 8000

# Run the FastAPI app using Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
