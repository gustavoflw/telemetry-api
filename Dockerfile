FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false

# Copy pyproject.toml
COPY pyproject.toml /app/

# Generate lock file
RUN poetry lock

# Copy application code
COPY src /app/src

# Install dependencies
RUN poetry install --no-dev

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
