# Makefile - EduPaie

.PHONY: help install run test clean build

help:
	@echo "Commandes disponibles :"
	@echo "  make install  - Installer les dependances"
	@echo "  make run      - Lancer l'application"
	@echo "  make test     - Lancer les tests"
	@echo "  make clean    - Nettoyer"
	@echo "  make build    - Generer l'executable"

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	python -m pytest tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build/ dist/ *.spec

build:
	pyinstaller --onefile --windowed --name EduPaie main.py
