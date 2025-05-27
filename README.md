# Project Documentation

## Spis treści

- [Wymagania i uruchomienie](docs/requirements_and_run.md)
- [Makefile i komendy developerskie](docs/makefile_commands.md)
- [Architektura i zależności](docs/architecture.md)
- [Django Backend](docs/django_backend.md)
- [Chainlit](docs/chainlit.md)
- [Nginx](docs/nginx.md)
- [Prisma](docs/prisma.md)

## Opis projektu

Projekt składa się z kilku głównych komponentów: backendu Django (API i autoryzacja), Chainlit (interfejs AI/chat), Nginx (reverse proxy i serwowanie statycznych plików) oraz Prisma (ORM dla wybranych usług). Każdy komponent jest uruchamiany jako osobny kontener Docker i komunikuje się przez sieć docker-compose. Szczegóły znajdziesz w dokumentacji w katalogu docs/.

# Project Name - TODO: Update Project Name

[Krótki opis projektu - TODO: Dodać opis]

## Wymagania wstępne

- Docker
- Docker Compose

## Konfiguracja

Przed uruchomieniem projektu należy przygotować pliki konfiguracyjne dla poszczególnych usług.

### PostgreSQL (Wspólna Baza Danych)

W pliku `docker-compose.yml` zdefiniowana jest usługa `postgres`, która służy jako wspólna baza danych dla Django, Chainlit i LiteLLM. Konfiguracja domyślnej bazy danych i użytkownika odbywa się poprzez zmienne środowiskowe `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` ustawiane globalnie lub w głównym pliku `.env`. 

Dodatkowo, kontener PostgreSQL automatycznie tworzy dedykowane bazy danych i użytkowników dla poszczególnych usług przy pierwszym uruchomieniu, korzystając ze skryptu inicjalizacyjnego `postgres/docker-entrypoint-initdb.d/create-multiple-databases.sh`. Skrypt ten tworzy bazy danych i użytkowników na podstawie następujących zmiennych środowiskowych zdefiniowanych w pliku `.env`:

- Dla Django: `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`
- Dla Chainlit: `CHAINLIT_DB_NAME`, `CHAINLIT_DB_USER`, `CHAINLIT_DB_PASSWORD`
- Dla LiteLLM: `LITELLM_DB_NAME`, `LITELLM_DB_USER`, `LITELLM_DB_PASSWORD`

**Upewnij się, że odpowiednie zmienne `DATABASE_URL` w pliku `.env` wskazują na hosta `postgres` (np. `postgresql://user:pass@postgres:5432/db`).**

### Django Backend (`django-backend`)

1.  **Zmienne Środowiskowe dla Bazy Danych:** Aplikacja Django jest skonfigurowana do korzystania z dedykowanej bazy danych PostgreSQL. Upewnij się, że w głównym pliku `.env` zdefiniowane są następujące zmienne środowiskowe:
    *   `DJANGO_DB_NAME`: Nazwa bazy danych dla Django (np. `django_db`).
    *   `DJANGO_DB_USER`: Nazwa użytkownika bazy danych dla Django (np. `django_user`).
    *   `DJANGO_DB_PASSWORD`: Hasło dla użytkownika bazy danych Django.
    *   `DJANGO_DB_HOST`: Nazwa hosta bazy danych (powinna być `postgres`, czyli nazwa usługi Docker).
    *   `DJANGO_DB_PORT`: Port bazy danych (domyślnie `5432`).
    Aplikacja odczytuje te zmienne w pliku `django-backend/core/settings.py`.

2.  **Automatyczne Utworzenie Dedykowanej Bazy Danych i Użytkownika:** Dzięki skryptowi inicjalizacyjnemu `postgres/docker-entrypoint-initdb.d/create-multiple-databases.sh`, dedykowana baza danych i użytkownik dla aplikacji Django są tworzone automatycznie przy pierwszym uruchomieniu kontenera PostgreSQL. Wystarczy, że w pliku `.env` zdefiniowane są zmienne środowiskowe `DJANGO_DB_NAME`, `DJANGO_DB_USER` i `DJANGO_DB_PASSWORD`.

    Skrypt nadaje również wszystkie niezbędne uprawnienia, w tym właścicielstwo bazy danych i schematu. Jeśli potrzebujesz dodatkowych uprawnień dla użytkownika Django (np. do tworzenia baz danych dla testów), możesz je dodać ręcznie, łącząc się z bazą danych:

    ```bash
    docker compose exec postgres psql -U postgres
    ```

    Następnie, wewnątrz interfejsu `psql`, możesz wykonać dodatkowe polecenia SQL, np.:

    ```sql
    -- WAŻNE DLA TESTÓW DJANGO: Nadaj użytkownikowi uprawnienia do tworzenia baz danych
    -- Jest to wymagane przez mechanizm testowy Django do tworzenia tymczasowej bazy testowej.
    ALTER USER <DJANGO_DB_USER> CREATEDB;

    -- Wyjdź z psql
    \q
    ```

### Chainlit (`chainlit`)

Chainlit wymaga odpowiedniej konfiguracji zmiennych środowiskowych. Przykładowy plik konfiguracyjny znajduje się w `chainlit/.env-example`. Aby skonfigurować Chainlit:

1. Skopiuj plik `chainlit/.env-example` do `chainlit/.env` i dostosuj wartości zmiennych według potrzeb.

2. Upewnij się, że w głównym pliku `.env` projektu zdefiniowane są zmienne środowiskowe dla bazy danych Chainlit:
   * `CHAINLIT_DB_NAME`: Nazwa bazy danych dla Chainlit
   * `CHAINLIT_DB_USER`: Nazwa użytkownika bazy danych dla Chainlit
   * `CHAINLIT_DB_PASSWORD`: Hasło dla użytkownika bazy danych Chainlit

3. Skonfiguruj dostęp do API OpenAI poprzez zmienne:
   * `OPENAI_URL`: URL API OpenAI (domyślnie: `https://api.openai.com/v1/`)
   * `OPENAI_API_KEY`: Klucz API OpenAI

4. Ustaw klucze dla autentykacji Chainlit:
   * `CHAINLIT_AUTH_SECRET`: Sekretny klucz używany do autentykacji w Chainlit

Chainlit komunikuje się z backendem Django poprzez zmienną środowiskową `DJANGO_BACKEND_URL` (domyślnie ustawioną na `http://nginx` w `docker-compose.yml`) oraz z LiteLLM Proxy poprzez `LITELLM_PROXY_URL` (domyślnie `http://litellm-proxy:8080`).

### Nginx (`nginx`)

Konfiguracja Nginx znajduje się w pliku `nginx/nginx.conf`. Domyślnie jest skonfigurowany do serwowania plików statycznych Django oraz jako reverse proxy dla aplikacji Django.

[TODO: Dodać ewentualne dodatkowe kroki konfiguracyjne dla Nginx.]

### Prisma

Schemat Prisma znajduje się w `prisma/schema.prisma`. Do interakcji z bazą danych za pomocą Prisma (migracje, studio) służy dedykowana usługa `prisma_cli` zdefiniowana w `docker-compose.yml`. Usługa ta wymaga pliku `.env` w głównym katalogu projektu z poprawnie ustawioną zmienną `DATABASE_URL` wskazującą na kontener `postgres`.

## Uruchomienie

Aby uruchomić wszystkie niezbędne usługi (bez narzędzi deweloperskich jak Prisma Studio):

```bash
docker compose up -d --build
```

## Zarządzanie Bazą Danych (Prisma)

Po uruchomieniu usług (`docker compose up -d`), możesz zarządzać schematem bazy danych za pomocą narzędzi Prisma uruchamianych w kontenerze `prisma_cli`.

### Migracje Prisma

Aby zastosować oczekujące migracje zdefiniowane w katalogu `prisma/migrations` do bazy danych:

```bash
docker compose run --rm prisma_cli npx prisma migrate deploy
```
To polecenie należy wykonać po każdej zmianie w `prisma/schema.prisma` i wygenerowaniu nowej migracji (np. za pomocą `docker compose run --rm prisma_cli npx prisma migrate dev --name nazwa_migracji`).

### Prisma Studio (Narzędzie Deweloperskie)

Aby uruchomić Prisma Studio (graficzny interfejs do przeglądania i edycji danych w bazie):

```bash
docker compose run --rm -p 5555:5555 prisma_cli npx prisma studio
```
Następnie otwórz w przeglądarce adres: [http://localhost:5555](http://localhost:5555).

Prisma Studio jest narzędziem deweloperskim i powinno być uruchamiane tylko na żądanie.

## Dostęp do Aplikacji

-   Aplikacja Django: [http://localhost](http://localhost) (przez Nginx)
-   Chainlit UI: [http://localhost:8000](http://localhost:8000)
-   LiteLLM Proxy: [http://localhost:8080](http://localhost:8080)

## Dodatkowe Informacje

### LiteLLM Proxy

Projekt wykorzystuje LiteLLM Proxy jako pośrednika do komunikacji z modelami językowymi. Konfiguracja LiteLLM znajduje się w pliku `litellm-proxy/config.yaml`. Proxy wymaga następujących zmiennych środowiskowych w głównym pliku `.env`:

- `LITELLM_DB_NAME`, `LITELLM_DB_USER`, `LITELLM_DB_PASSWORD`: Dane dostępowe do dedykowanej bazy danych
- `LITELLM_DB_URL`: Pełny URL połączenia do bazy danych (np. `postgresql://litellm_user:password@postgres:5432/litellm_db`)
- `LITELLM_MASTER_KEY`: Główny klucz API dla LiteLLM
- `LITELLM_SALT_KEY`: Klucz używany do szyfrowania danych

LiteLLM Proxy jest dostępny pod adresem [http://localhost:8080](http://localhost:8080).

### Struktura Projektu

Projekt składa się z następujących głównych komponentów:

- `django-backend/`: Backend Django z API i autoryzacją
- `chainlit/`: Interfejs użytkownika AI/chat oparty na Chainlit
- `nginx/`: Konfiguracja serwera Nginx (reverse proxy)
- `postgres/`: Skrypty inicjalizacyjne dla bazy danych PostgreSQL
- `prisma/`: Schemat bazy danych i narzędzia ORM
- `litellm-proxy/`: Konfiguracja proxy dla modeli językowych

Szczegółowa dokumentacja poszczególnych komponentów znajduje się w katalogu `docs/`.
