# Variáveis
PYTHON = python
PY_VERSION = 3.13.2
PIP = pip
VENV = venv
VENV_BIN = $(VENV)/bin
DOCKER_COMPOSE = docker compose

# Comandos
.PHONY: check install migrate run lint clean help

check:
	@if ! pyenv versions | grep -q $(PY_VERSION); then \
		pyenv install $(PY_VERSION); \
	else \
		echo "Python $(PY_VERSION) já está instalado."; \
	fi
	@pyenv local $(PY_VERSION)

install:
	$(PYTHON) --version
	$(PYTHON) -m venv venv
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	docker network create project-net || true

migrate:
	$(DOCKER_COMPOSE) up --build -d
	@read -p "Digite a mensagem para a migração: " message; \
	$(DOCKER_COMPOSE) exec drive-web alembic revision --autogenerate -m "$$message"
	$(DOCKER_COMPOSE) stop

run:
	$(DOCKER_COMPOSE) up --build

lint:
	$(VENV_BIN)/black .
	$(VENV_BIN)/ruff check --fix .
	$(VENV_BIN)/mypy .

clean:
	rm -rf ./**/*.pyc ./**/__pycache__ .mypy_cache venv .ruff_cache logs

help:
	@echo "Comandos disponíveis:"
	@echo "  check   : Verifica se a versão correta do Python está instalada"
	@echo "  install : Prepara o ambiente e instala as dependências do projeto"
	@echo "  migrate : Cria uma nova migração do Alembic"
	@echo "  run     : Executa o projeto"
	@echo "  lint    : Executa todos os linters do projeto"
	@echo "  clean   : Remove arquivos de cache e a rede Docker"
