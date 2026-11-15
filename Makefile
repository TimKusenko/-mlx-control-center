.PHONY: help install dev test lint format type-check clean build

help:
	@echo "MLX Control Center — Development Commands"
	@echo ""
	@echo "  make install       Install package"
	@echo "  make dev           Install in development mode"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters (black, isort)"
	@echo "  make type-check    Run type checker (mypy)"
	@echo "  make format        Format code with black & isort"
	@echo "  make clean         Remove build artifacts and cache"
	@echo "  make build         Build distribution package"

install:
	pip install .

dev:
	pip install -e .
	pip install pytest pytest-cov black isort mypy

test:
	pytest tests/ -v --tb=short

lint:
	black --check mlx_control tests
	isort --check-only mlx_control tests

type-check:
	mypy mlx_control --ignore-missing-imports

format:
	black mlx_control tests
	isort mlx_control tests

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .coverage htmlcov/

build: clean
	python -m build

all: format type-check test
