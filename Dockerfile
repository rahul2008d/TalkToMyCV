# Step 1: Start from the AWS Lambda Python runtime base image
FROM public.ecr.aws/lambda/python:3.9 AS base

# Step 2: Install system dependencies required for building and running the app
RUN yum install -y gcc libffi-devel

# Step 3: Install Poetry to handle dependencies
RUN pip install --no-cache-dir poetry==2.0.0

# Set environment variables for Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Step 4: Set the working directory in the container
WORKDIR /app

# Step 5: Copy only the dependency-related files first to leverage Docker caching
COPY pyproject.toml poetry.lock README.md ./ 

# Step 6: Install dependencies (without dev dependencies) and ensure virtual environment is created
RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# Step 7: Copy application code into the container
COPY app ./app

# Step 8: Copy vector-store directory to the container (it will be used by the app)
COPY vector_store ./vector_store

# Step 9: Ensure the virtual environment is activated
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app

# Step 10: Set the environment variable for AWS Lambda integration
ENV LAMBDA_TASK_ROOT=/app

# Step 12: CMD directive will instruct Lambda to run this entry point.
# Since FastAPI is already handled inside `main.py`, we just invoke Mangum for Lambda.
CMD ["app/main.handler"]
