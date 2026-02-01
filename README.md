# Expenses Tracker App (Flask)

A simple Flask-based application for managing expenses.  
Built as a practice project to explore backend development with Flask, including routing, templates, forms, and database integration.

---

## Getting Started
## Copy Environment File:
```
cp .env.sample .env
```
Edit `.env` and fill in your actual values
### Build and run project
```
docker-compose up --build
```
### Run migration
```
docker-compose exec web flask db upgrade
```
## Development
### Run tests
```
docker-compose exec web pytest
# Run specific test file
docker-compose exec web pytest tests/test_auth.py 
```

### Run tests with coverage
```
docker-compose exec web pytest --cov=src --cov-report=html tests/
```

### Linting
We use flake8 and black for linting and formatting. Run:
```
docker-compose exec web python et-cli.py lint
```
### Test coverage
```
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html tests/
```
## License
This project is for learning purposes.
