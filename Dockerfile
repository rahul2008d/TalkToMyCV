# Use an official Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.10

# Set environment variables for Python and prevent buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

# Create an app directory in the container
WORKDIR /var/task

# Copy pyproject.toml and README to install dependencies
COPY pyproject.toml README.md /var/task/

RUN curl -sSL https://install.python-poetry.org | python3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Copy the application code to the container
COPY app/ /var/task/app/
COPY vector_store/ /var/task/vector_store/

# Define the Lambda handler
CMD ["app.main.handler"]
