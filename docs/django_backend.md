# Django Backend

## Opis

Backend Django odpowiada za logikę biznesową, API oraz autoryzację użytkowników. W projekcie wykorzystywany jest Django REST Framework do budowy API.

## Konfiguracja

- Zmienne środowiskowe bazy danych muszą być ustawione w pliku `.env`:
  - `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST` (powinno być `postgres`), `DJANGO_DB_PORT`.
- Po pierwszym uruchomieniu należy ręcznie utworzyć bazę danych i użytkownika (patrz: requirements_and_run.md).

## Endpointy API

- `/api/accounts/verify-credentials/` – POST, weryfikacja danych logowania użytkownika (używane przez Chainlit).

## Integracja

- Backend jest wystawiony na porcie 8000 w kontenerze `web`.
- Nginx przekazuje ruch HTTP z portu 80 do backendu Django.
- Chainlit korzysta z endpointów Django do autoryzacji użytkowników.

## Testowanie

- Testy uruchamiasz komendą `make web-test` (wykorzystuje bazę testową, użytkownik Django musi mieć uprawnienia CREATEDB).

## Migracje

- Tworzenie migracji: `make web-makemigrations`
- Stosowanie migracji: `make web-migrate` 