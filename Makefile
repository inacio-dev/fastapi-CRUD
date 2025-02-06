# Variáveis
PYTHON = python3.12
PIP = pip
VENV = venv
VENV_BIN = $(VENV)/bin
DOCKER_COMPOSE = docker compose

# Comandos
.PHONY: install migrate run lint clean help

install:
	$(PYTHON) -m venv venv
	$(VENV_BIN)/pip install -r requirements.txt
	docker network create project-net || true

migrate:
	$(DOCKER_COMPOSE) up --build -d
	@read -p "Digite a mensagem para a migração: " message; \
	$(DOCKER_COMPOSE) exec web alembic revision --autogenerate -m "$$message"
	$(DOCKER_COMPOSE) down

run:
	$(DOCKER_COMPOSE) up --build

lint:
	black .
	ruff check .
	mypy .

clean:
	rm -rf ./**/*.pyc ./**/__pycache__ .mypy_cache venv .ruff_cache logs

help:
	@echo "Comandos disponíveis:"
	@echo "  install : Prepara o ambiente e instala as dependências do projeto"
	@echo "  migrate : Cria uma nova migração do Alembic"
	@echo "  run     : Executa o projeto"
	@echo "  lint    : Executa todos os linters do projeto"
	@echo "  clean   : Remove arquivos de cache e a rede Docker"
