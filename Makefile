SHELL := /bin/bash
.ONESHELL:

APP_PATH := ./app.py

# Docker commands
up:
	docker-compose up -d

down:
	docker-compose down

delete:
	docker-compose down --volumes --remove-orphans

# Build commands
start:
	streamlit run $(APP_PATH)