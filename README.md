# Expenses Tracker App (Flask)

A simple Flask-based application for managing expenses.  
Built as a practice project to explore backend development with Flask, including routing, templates, forms, and database integration.

---

## Getting Started

### 1. Install dependencies
```
poetry install
```
### 2. Run project
```
poetry run flask run
```
## Development
### Linting
We use flake8 and black for linting and formatting. Run:
```
poetry run python et-cli.py lint
```
### Test coverage
```
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html tests/
```
## License
This project is for learning purposes.
