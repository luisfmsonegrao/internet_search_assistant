# Makefile (Windows only)

.PHONY: setup format run clean

VENV = .venv

setup:
	@if not exist $(VENV) (
		python -m venv $(VENV)
	)
	@$(VENV)\Scripts\pip install --upgrade pip
	@$(VENV)\Scripts\pip install -r requirements.txt

# Format all code using Ruff
format:
	@$(VENV)\Scripts\ruff format .
	@$(VENV)\Scripts\ruff check .

run:
	python src\assistant_core\gradio_ui.py

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

install