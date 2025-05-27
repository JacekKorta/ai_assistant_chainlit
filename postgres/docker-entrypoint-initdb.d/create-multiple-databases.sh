#!/bin/bash
set -e

# Funkcja do tworzenia bazy danych i użytkownika
create_db_and_user() {
    local db_name=$1
    local user=$2
    local password=$3

    echo "Creating database $db_name and user $user..."
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE DATABASE $db_name;
        CREATE USER $user WITH PASSWORD '$password';
        GRANT ALL PRIVILEGES ON DATABASE $db_name TO $user;
        ALTER DATABASE $db_name OWNER TO $user;
        \c $db_name
        ALTER SCHEMA public OWNER TO $user;
        GRANT ALL ON SCHEMA public TO $user;
EOSQL
    echo "Created database $db_name and user $user."
}

# Tworzenie bazy dla Django
if [ -n "$DJANGO_DB_NAME" ] && [ -n "$DJANGO_DB_USER" ] && [ -n "$DJANGO_DB_PASSWORD" ]; then
    create_db_and_user "$DJANGO_DB_NAME" "$DJANGO_DB_USER" "$DJANGO_DB_PASSWORD"
fi

# Tworzenie bazy dla Chainlit
if [ -n "$CHAINLIT_DB_NAME" ] && [ -n "$CHAINLIT_DB_USER" ] && [ -n "$CHAINLIT_DB_PASSWORD" ]; then
    create_db_and_user "$CHAINLIT_DB_NAME" "$CHAINLIT_DB_USER" "$CHAINLIT_DB_PASSWORD"
fi

# Tworzenie bazy dla LiteLLM
if [ -n "$LITELLM_DB_NAME" ] && [ -n "$LITELLM_DB_USER" ] && [ -n "$LITELLM_DB_PASSWORD" ]; then
    create_db_and_user "$LITELLM_DB_NAME" "$LITELLM_DB_USER" "$LITELLM_DB_PASSWORD"
fi