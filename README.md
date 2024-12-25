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

- **Python 3.12+**
- **Docker** e **Docker Compose** (opcional, mas recomendado)
- **PostgreSQL** (ou outro banco configurado no projeto)

## Instalação e Configuração

### 1. Clone este repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2. Configure o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate # No Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Antes de iniciar o projeto, configure as variáveis de ambiente. Um arquivo `.env` é necessário para armazenar essas variáveis, garantindo uma configuração consistente e segura.

Aqui está um exemplo do arquivo `.env`:

```env
# Database
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_SCHEMA=protheus

# Database Pool
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000

# Cache
REDIS_URL=redis://redis:6379
CACHE_TIMEOUT=1800
```

### Instruções para configuração:

1. **Banco de Dados**:

   - Configure as informações do banco de dados, como nome do banco, usuário, senha, host e porta.
   - O esquema do banco está configurado como `protheus`, mas pode ser alterado conforme sua necessidade.

2. **Pool de Conexões do Banco de Dados**:

   - Ajuste os parâmetros do pool conforme o volume de conexões esperado na aplicação.

3. **FastAPI**:

   - Configure o host e a porta em que a API será executada. Por padrão, está configurado para `0.0.0.0:8000`.

4. **Cache**:
   - Configure o Redis para armazenar dados em cache e defina o tempo de expiração (`CACHE_TIMEOUT`).

Certifique-se de salvar este arquivo na raiz do projeto antes de iniciar a aplicação. Isso garantirá que todas as variáveis de ambiente sejam carregadas corretamente.

### 4. Execute as migrações do banco de dados

```bash
alembic upgrade head
```

### 5. Execute a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Usando o Docker (opcional)

Para rodar toda a aplicação com Docker, utilize os seguintes comandos:

1. **Build e inicialização dos serviços**:

   ```bash
   docker-compose up --build
   ```

2. **Acesse a aplicação**:
   Acesse a aplicação no endereço [http://localhost:8000](http://localhost:8000).

## Rotas disponíveis

A API inclui as seguintes rotas (CRUD básico):

- **GET** `/items/`: Listar todos os itens.
- **GET** `/items/{id}`: Obter um item pelo ID.

Para explorar todas as rotas, acesse a documentação interativa:

- **Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testes

Para executar os testes, utilize:

```bash
pytest
```

Certifique-se de configurar um banco de dados de teste no arquivo `.env`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
