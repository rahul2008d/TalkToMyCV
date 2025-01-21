# Use the official AWS Lambda Python runtime as a base image
FROM public.ecr.aws/lambda/python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install Poetry (for dependency management)
RUN pip install --no-cache-dir poetry

# Copy the Poetry configuration and other necessary files into the container
COPY pyproject.toml poetry.lock* /app/

# Install dependencies with Poetry
RUN poetry install --no-dev --no-root

# Copy the application code into the container
COPY . /app/

# Set the environment variable for the Lambda handler (FastAPI app)
ENV AWS_LAMBDA_FUNCTION_HANDLER="app.lambda_handler"

# Expose port 8080 for local testing
EXPOSE 8080

# Use the Lambda runtime to run the FastAPI app when the container starts
CMD ["app.lambda_handler"]
