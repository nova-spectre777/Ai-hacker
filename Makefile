.PHONY: install test lint compile env

install:
	python -m pip install -e ".[dev,web]"

test:
	python -m pytest -q

lint:
	ruff check src tests scripts

compile:
	python -m compileall -q src scripts cyber-lab

env:
	python scripts/check_environment.py
