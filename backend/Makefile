
.PHONY: install test lint format run clean docker-build docker-run

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=html --cov-report=term

lint:
	flake8 . --exclude=.venv --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --exclude=.venv --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black . --line-length=100
	isort . --profile=black

run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-prod:
	uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

# docker-build:
# 	docker build -t rsa-backend .

# docker-run:
# 	docker run -p 8000:8000 rsa-backend