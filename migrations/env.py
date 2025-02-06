import importlib
import os
import pkgutil
from collections.abc import MutableMapping
from logging.config import fileConfig
from typing import Literal

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from app.core.database.sync_db import Base


# Função para carregar modelos dinamicamente
def load_models() -> None:
    """Dinamicamente importa todos os modelos no diretório 'models'."""
    models_path = os.path.join(os.path.dirname(__file__), "../app/core/models")
    for module_info in pkgutil.iter_modules([models_path]):
        importlib.import_module(f"app.core.models.{module_info.name}")


# Carregar modelos antes de definir o metadata
load_models()

print("Tabelas carregadas no Base.metadata:")
for table_name, table in Base.metadata.tables.items():
    print(f"  Tabela: {table_name}, Schema: {table.schema}")

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a configuração do Alembic
config = context.config
section = config.config_ini_section

# Definir variáveis de ambiente no arquivo de configuração
config.set_section_option(section, "POSTGRES_DB", os.getenv("POSTGRES_DB", "default_db"))
config.set_section_option(section, "POSTGRES_USER", os.getenv("POSTGRES_USER", "default_user"))
config.set_section_option(section, "POSTGRES_PASSWORD", os.getenv("POSTGRES_PASSWORD", "default_password"))
config.set_section_option(section, "POSTGRES_HOST", os.getenv("POSTGRES_HOST", "localhost"))
config.set_section_option(section, "POSTGRES_PORT", os.getenv("POSTGRES_PORT", "5432"))

# Obter schema do PostgreSQL
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA", "public")


# Configurar loggers se o arquivo de configuração existir
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Assegurar que todas as tabelas têm o schema correto
for table in Base.metadata.tables.values():
    if not table.schema:
        table.schema = POSTGRES_SCHEMA

# MetaData para autogenerate
# Assegure-se de que Base.metadata contém todos os modelos relevantes
# para as migrações automáticas.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    def include_name(
        name: str | None,
        type_: Literal["schema", "table", "column", "index", "unique_constraint", "foreign_key_constraint"],
        parent_names: MutableMapping[Literal["schema_name", "table_name", "schema_qualified_table_name"], str | None],
    ) -> bool:
        if type_ == "schema":
            return name in [POSTGRES_SCHEMA]
        else:
            return True

    """Executar migrações no modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        include_name=include_name,
        version_table_schema=POSTGRES_SCHEMA,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executar migrações no modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    def include_name(
        name: str | None,
        type_: Literal["schema", "table", "column", "index", "unique_constraint", "foreign_key_constraint"],
        parent_names: MutableMapping[Literal["schema_name", "table_name", "schema_qualified_table_name"], str | None],
    ) -> bool:
        if type_ == "schema":
            return name in [POSTGRES_SCHEMA]
        else:
            return True

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            version_table_schema=POSTGRES_SCHEMA,
        )

        with context.begin_transaction():
            context.run_migrations()


# Escolher entre modo offline ou online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
