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

1.  **Plik Konfiguracyjny:** Upewnij się, że plik `django-backend/config.yml` istnieje i zawiera poprawną konfigurację, w tym dane dostępowe do bazy danych PostgreSQL. Szczegóły dotyczące struktury tego pliku znajdują się [TODO: link do dokumentacji lub opisu struktury config.yml].
2.  **Zmienne Środowiskowe dla Bazy Danych:** Aplikacja Django wczytuje dane dostępowe do bazy danych (nazwa bazy, użytkownik, hasło, host, port) ze swojego pliku `config.yml`. Host bazy danych powinien być ustawiony na `postgres` (nazwa usługi Docker).
3.  **Utworzenie Bazy Danych i Użytkownika:** Po pierwszym uruchomieniu kontenera `postgres`, należy ręcznie utworzyć dedykowaną bazę danych i użytkownika dla Django. Połącz się z kontenerem `postgres` i wykonaj odpowiednie polecenia SQL (patrz sekcja `PostgreSQL` w dokumentacji konfiguracji - TODO: dodać link lub instrukcje).

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
