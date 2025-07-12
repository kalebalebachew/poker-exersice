# Poker Hand Evaluator API

Production-ready backend API for the Poker Hand Evaluator application, built with FastAPI and PostgreSQL.

## Features

- Evaluate poker hands using the pokerkit library
- Track and store poker game history in PostgreSQL
- Calculate winnings for poker games with accurate poker rules
- RESTful API design with proper status codes and error handling
- Comprehensive test suite with unit and integration tests
- Production-ready Docker configuration with multi-stage builds

## Technology Stack

- **Python 3.11**: Modern Python version with improved performance
- **FastAPI**: High-performance web framework for building APIs
- **PostgreSQL**: Robust relational database for data persistence
- **pokerkit**: Advanced poker hand evaluation library
- **pytest**: Testing framework for unit and integration tests
- **Docker**: Containerization for consistent deployment

## Architecture

The application follows a clean architecture pattern with the following components:

- **Models**: Data models using Python dataclasses and Pydantic schemas
- **Repositories**: Data access layer with raw SQL (no ORM)
- **Services**: Business logic layer for poker game evaluation
- **API Endpoints**: RESTful API endpoints for client interaction

## API Endpoints

### Hand Endpoints

- `POST /api/v1/poker/hands/`: Create and evaluate a new poker hand
- `GET /api/v1/poker/hands/`: Get all poker hands
- `GET /api/v1/poker/hands/{hand_id}`: Get a specific poker hand

### Game Endpoints

- `POST /api/v1/poker/games/`: Create a new poker game
- `POST /api/v1/poker/games/evaluate/`: Evaluate a complete poker game
- `GET /api/v1/poker/games/`: Get all poker games
- `GET /api/v1/poker/games/{game_id}`: Get a specific poker game
- `POST /api/v1/poker/games/{game_id}/actions/`: Add an action to a poker game

## Development Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:

   ```bash
   # Make sure PostgreSQL is running
   # Create a database named 'poker'
   ```

5. Set environment variables:

   ```bash
   export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/poker
   ```

6. Run the application:

   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Production Deployment

### Using Docker Compose

1. Make sure Docker and Docker Compose are installed on your system.

2. Build and start the containers:

   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - API: http://localhost:8000
   - Frontend: http://localhost:3000

### Manual Deployment

1. Build the Docker image:

   ```bash
   docker build -t poker-api ./backend
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 \
     -e DATABASE_URL=postgresql://postgres:postgres@db:5432/poker \
     -e ENVIRONMENT=production \
     poker-api
   ```

## Testing

Run tests with pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

## Performance Considerations

- The application uses connection pooling for database connections
- The Docker configuration includes proper resource limits
- The application uses multiple workers in production for better concurrency

## Security Considerations

- The application runs as a non-root user in Docker
- Environment variables are used for sensitive configuration
- Input validation is performed on all API endpoints

## Monitoring and Logging

- Health check endpoints are provided for monitoring
- Structured logging is used for better observability
- Docker health checks are configured for all services

## License

This project is licensed under the MIT License - see the LICENSE file for details.

