# Wymagania i uruchomienie

## Wymagania wstępne

- Docker
- Docker Compose

## Konfiguracja środowiska

1. Skonfiguruj plik `.env` w katalogu głównym na podstawie `.env-example`.
2. Upewnij się, że porty 80 (Nginx), 8000 (Chainlit) i 5432 (Postgres) są wolne.

## Uruchomienie projektu

Aby uruchomić wszystkie usługi:

```bash
docker compose up -d --build
```

Aby zatrzymać i usunąć kontenery:

```bash
make down
```

## Dostęp do aplikacji

- Django (przez Nginx): http://localhost
- Chainlit: http://localhost:8000

Więcej szczegółów znajdziesz w pozostałych plikach dokumentacji. 