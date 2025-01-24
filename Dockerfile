# Use an official Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.10

# Set environment variables for Python and prevent buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

# Create an app directory
WORKDIR /var/task

# Copy pyproject.toml to install dependencies
COPY pyproject.toml /var/task/

# Install Poetry for dependency management
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy the application code to the container
COPY app/ /var/task/app/
COPY vector_store/ /var/task/vector_store/

# Add Lambda handler
CMD ["app.main.handler"]
