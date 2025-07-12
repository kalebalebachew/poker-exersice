# Poker Game Application

A full-stack poker game application built with NextJS, FastAPI, and PostgreSQL.

## Requirements

- Docker
- Docker Compose

## Running the Application

To run the application, simply execute the following command from the root directory:

```bash
docker-compose up -d
```

Then open your browser and navigate to:

```
http://localhost:3000
```

## Architecture

- **Frontend**: NextJS with React and TypeScript, using shadcn/ui for styling
- **Backend**: FastAPI with Python, using Poetry for package management
- **Database**: PostgreSQL for data storage

## Features

- Play a full hand from start to finish in a 6-player Texas Holdem game
- Simulate a simple hand by pressing action buttons
- All actions are logged in the text field
- Completed hands are saved in a database and appear in the hand log

## Testing

### Frontend Tests

```bash
# Run unit tests
docker-compose exec frontend npm test

# Run end-to-end tests
docker-compose exec frontend npm run test:e2e
```

### Backend Tests

```bash
docker-compose exec backend poetry run pytest
```
