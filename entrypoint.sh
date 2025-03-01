#!/bin/sh

# Aguarda o banco de dados estar pronto
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Database started"

# Define a senha do banco de dados
export PGPASSWORD=$POSTGRES_PASSWORD

# Conecta ao banco de dados e cria o schema se ele não existir
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "CREATE SCHEMA IF NOT EXISTS $POSTGRES_SCHEMA;"

# Executa as migrations
alembic upgrade head

# Inicia a aplicação
exec uvicorn app.main:app --host ${API_HOST} --port ${API_PORT} --reload