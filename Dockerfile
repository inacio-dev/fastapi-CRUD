FROM python:3.13.2

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Instalar dependências e netcat para health check
RUN pip install --no-cache-dir -r /code/requirements.txt && \
    apt-get update && apt-get install -y netcat-openbsd postgresql-client

COPY . .

# Tornar os scripts executáveis
RUN chmod +x /code/entrypoint.sh

CMD ["/code/entrypoint.sh"]