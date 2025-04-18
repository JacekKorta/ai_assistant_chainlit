# Project Name - TODO: Update Project Name

[Krótki opis projektu - TODO: Dodać opis]

## Wymagania wstępne

- Docker
- Docker Compose

## Konfiguracja

Przed uruchomieniem projektu należy przygotować pliki konfiguracyjne dla poszczególnych usług.

### PostgreSQL (Wspólna Baza Danych)

W pliku `docker-compose.yml` zdefiniowana jest usługa `postgres`, która służy jako wspólna baza danych dla Django i Prismy. Konfiguracja domyślnej bazy danych i użytkownika (np. dla Prismy) odbywa się poprzez zmienne środowiskowe `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` ustawiane globalnie lub w głównym pliku `.env`.

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

[TODO: Opisać kroki konfiguracji dla Prismy. Wiadomo, że korzysta z bazy `postgres` i domyślnych danych uwierzytelniających z `docker-compose.yml` lub zmiennych środowiskowych.]

## Uruchomienie

Aby uruchomić wszystkie usługi zdefiniowane w `docker-compose.yml`:

```bash
docker compose up -d --build
```

## Dostęp do Aplikacji

-   Aplikacja Django: [http://localhost](http://localhost) (przez Nginx)
-   Chainlit UI: [http://localhost:8000](http://localhost:8000)

## Dodatkowe Informacje

[TODO: Dodać linki do dalszej dokumentacji, opis struktury projektu itp.]
