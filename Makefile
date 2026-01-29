.PHONY: install test train run benchmark load-test docker-build docker-up clean

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=src --cov-report=html

train:
	python train_model.py

run:
	python src/api.py

example:
	python example_usage.py

benchmark:
	python benchmark.py

load-test:
	python load_test.py

docker-build:
	docker build -t fraud-detection:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

redis-start:
	redis-server

redis-stop:
	redis-cli shutdown

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make train        - Train ML model"
	@echo "  make run          - Start API server"
	@echo "  make example      - Run example usage"
	@echo "  make benchmark    - Run performance benchmark"
	@echo "  make load-test    - Run load test"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start with Docker Compose"
	@echo "  make clean        - Clean cache files"
