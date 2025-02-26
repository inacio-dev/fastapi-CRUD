# CRUD em FastAPI

Este é um projeto de exemplo que implementa um CRUD (Create, Read, Update, Delete) utilizando **FastAPI**, uma framework web moderna, rápida e eficiente para Python. A aplicação foi projetada para ser simples, extensível e eficiente, com suporte para documentação automática de APIs.

## O que é FastAPI?

**FastAPI** é uma framework web moderna para construção de APIs em Python. Ela é baseada no padrão OpenAPI e no JSON Schema, oferecendo suporte a validações automáticas, documentação interativa, e performance comparável a frameworks como Node.js e Go. Alguns dos principais recursos do FastAPI incluem:

- **Rápido e de alto desempenho**: construído sobre o ASGI e o Starlette.
- **Validações automáticas de dados**: utiliza o Pydantic para validação e tipagem.
- **Documentação automática**: gera documentação interativa com Swagger e Redoc.
- **Intuitivo**: reduz a quantidade de código repetitivo, tornando-o fácil de entender e usar.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
app/
├── api/
│   ├── endpoints/      # Endpoints organizados em módulos
│   │   └── v1/         # Primeira versão de endpoints
│   ├── __init__.py     # Arquivo de inicialização
│   └── router.py       # Rotas principais
├── core/
│   ├── controllers/    # Lógica de controle (camada intermediária)
│   ├── database/       # Configuração de conexão com o banco de dados
│   ├── models/         # Definição dos modelos do banco de dados
│   ├── schemas/        # Schemas para validação de dados
│   └── tasks/          # Tarefas assíncronas e utilitários
├── utils/              # Scripts auxiliares
├── migrations/         # Controle de migrações de banco de dados (Alembic)
├── logs/               # Logs de execução
└── venv/               # Ambiente virtual Python
```

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

- **Pyenv** e **Python 3.13.2**
- **Docker** e **Docker Compose**

## Instalação e Configuração

### 1. Clone este repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Configure o ambiente virtual

```bash
make check
make install
```

### 3. Configure as variáveis de ambiente

Antes de iniciar o projeto, configure as variáveis de ambiente. Um arquivo `.env` é necessário para armazenar essas variáveis, garantindo uma configuração consistente e segura.

Aqui está um exemplo do arquivo `.env`:

```env
# Database
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_SCHEMA=

# Database Pool
DB_POOL_SIZE=
DB_MAX_OVERFLOW=
DB_POOL_TIMEOUT=
DB_POOL_RECYCLE=

# FastAPI
API_HOST=
API_PORT=

# Cache
REDIS_URL=
CACHE_TIMEOUT=
```

### Instruções para configuração:

1. **Banco de Dados**:

   - Configure as informações do banco de dados, como nome do banco, usuário, senha, host e porta.
   - O esquema do banco está configurado como `public`, mas pode ser alterado conforme sua necessidade.

2. **Pool de Conexões do Banco de Dados**:

   - Ajuste os parâmetros do pool conforme o volume de conexões esperado na aplicação.

3. **FastAPI**:

   - Configure o host e a porta em que a API será executada. Por padrão, está configurado para `0.0.0.0:8000`.

4. **Cache**:
   - Configure o Redis para armazenar dados em cache e defina o tempo de expiração (`CACHE_TIMEOUT`).

Certifique-se de salvar este arquivo na raiz do projeto antes de iniciar a aplicação. Isso garantirá que todas as variáveis de ambiente sejam carregadas corretamente.

### 4. Execute novas migrações do banco de dados

```bash
make migrate
```

### 5. Execute a aplicação

```bash
make run
```

A API estará disponível em: [http://localhost:8000](http://localhost:8000).

## Rotas disponíveis

Para explorar todas as rotas, acesse a documentação interativa:

- **Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Lint

Para executar os linters, utilize:

```bash
make lint
```
