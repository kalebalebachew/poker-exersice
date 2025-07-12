FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry==1.7.1

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Copy poetry configuration files
COPY pyproject.toml ./

# Generate lock file and install dependencies
RUN poetry lock --no-update
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Install the application
RUN poetry install --no-interaction --no-ansi

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 