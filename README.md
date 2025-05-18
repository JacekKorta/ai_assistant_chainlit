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

W pliku `docker-compose.yml` zdefiniowana jest usługa `postgres`, która służy jako wspólna baza danych dla Django i Prismy. Konfiguracja domyślnej bazy danych i użytkownika (np. dla Prismy) odbywa się poprzez zmienne środowiskowe `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` ustawiane globalnie lub w głównym pliku `.env`. **Upewnij się, że `DATABASE_URL` w pliku `.env` wskazuje na hosta `postgres` (np. `postgresql://user:pass@postgres:5432/db`).**

### Django Backend (`django-backend`)

1.  **Zmienne Środowiskowe dla Bazy Danych:** Aplikacja Django jest skonfigurowana do korzystania z dedykowanej bazy danych PostgreSQL. Upewnij się, że w głównym pliku `.env` zdefiniowane są następujące zmienne środowiskowe:
    *   `DJANGO_DB_NAME`: Nazwa bazy danych dla Django (np. `django_db`).
    *   `DJANGO_DB_USER`: Nazwa użytkownika bazy danych dla Django (np. `django_user`).
    *   `DJANGO_DB_PASSWORD`: Hasło dla użytkownika bazy danych Django.
    *   `DJANGO_DB_HOST`: Nazwa hosta bazy danych (powinna być `postgres`, czyli nazwa usługi Docker).
    *   `DJANGO_DB_PORT`: Port bazy danych (domyślnie `5432`).
    Aplikacja odczytuje te zmienne w pliku `django-backend/core/settings.py`.

2.  **Utworzenie Dedykowanej Bazy Danych i Użytkownika:** Po pierwszym uruchomieniu kontenera `postgres` (`docker compose up -d postgres`), należy **ręcznie utworzyć dedykowaną bazę danych i użytkownika** dla aplikacji Django. Połącz się z działającym kontenerem PostgreSQL używając użytkownika zdefiniowanego w `DATABASE_USER` (dla Prismy/Chainlit), który ma uprawnienia do tworzenia baz i użytkowników (lub użyj domyślnego superużytkownika `postgres`, jeśli to konieczne):
    ```bash
    docker compose exec postgres psql -U ${DATABASE_USER} -d ${DATABASE_NAME}
    # Lub: docker compose exec postgres psql -U postgres
    ```
    Następnie, wewnątrz interfejsu `psql`, wykonaj następujące polecenia SQL, zastępując wartości w nawiasach `< >` tymi zdefiniowanymi w zmiennych `DJANGO_DB_*` w pliku `.env`:
    ```sql
    -- Utwórz bazę danych
    CREATE DATABASE <DJANGO_DB_NAME>;

    -- Utwórz użytkownika z hasłem
    CREATE USER <DJANGO_DB_USER> WITH PASSWORD '<DJANGO_DB_PASSWORD>';

    -- Nadaj wszystkie uprawnienia do nowej bazy danych temu użytkownikowi
    GRANT ALL PRIVILEGES ON DATABASE <DJANGO_DB_NAME> TO <DJANGO_DB_USER>;

    -- Ustaw użytkownika jako właściciela bazy (opcjonalne, ale często przydatne)
    ALTER DATABASE <DJANGO_DB_NAME> OWNER TO <DJANGO_DB_USER>;

    -- WAŻNE DLA TESTÓW DJANGO: Nadaj użytkownikowi uprawnienia do tworzenia baz danych
    -- Jest to wymagane przez mechanizm testowy Django do tworzenia tymczasowej bazy testowej.
    ALTER USER <DJANGO_DB_USER> CREATEDB;

    -- Wyjdź z psql
    \q
    ```
    Na przykład, jeśli używasz wartości `django_db`, `django_user` i `django_secret_password`:
    ```sql
    CREATE DATABASE django_db;
    CREATE USER django_user WITH PASSWORD 'django_secret_password';
    GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;
    ALTER DATABASE django_db OWNER TO django_user;
    ALTER USER django_user CREATEDB;
    \q
    ```
    Ten krok jest niezbędny, aby Django mogło połączyć się ze swoją bazą danych oraz aby można było uruchamiać testy (`python manage.py test`).

### Chainlit (`chainlit`)

[TODO: Opisać kroki konfiguracji dla Chainlit, jeśli są wymagane. Na razie wiadomo, że korzysta z bazy `postgres`.]

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

## Dodatkowe Informacje

[TODO: Dodać linki do dalszej dokumentacji, opis struktury projektu itp.]
