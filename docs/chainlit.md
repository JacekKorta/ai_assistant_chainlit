# Chainlit

## Opis

Chainlit to interfejs AI/chat, który korzysta z OpenAI oraz integruje się z backendem Django w celu autoryzacji użytkowników.

## Konfiguracja

- W pliku `.env` należy ustawić klucz API OpenAI oraz adres backendu Django:
  - `OPENAI_API_KEY` – klucz API do OpenAI
  - `DJANGO_BACKEND_URL` – adres backendu Django (w docker-compose powinien być ustawiony na `http://nginx`)
- Chainlit uruchamiany jest jako osobny kontener na porcie 8000.

## Integracja z Django

- Chainlit weryfikuje użytkowników przez endpoint `/api/accounts/verify-credentials/` w Django, wysyłając żądania HTTP do backendu przez Nginx.
- Komunikacja między kontenerami odbywa się po nazwach usług (np. `nginx`).

## Uruchamianie

- Uruchomienie wszystkich usług: `docker compose up -d --build`
- Wejście do powłoki kontenera: `make chainlit-exec`

## Dodatkowe informacje

- Plik konfiguracyjny i kod główny znajduje się w `chainlit/main.py`.
- Chainlit korzysta z bazy danych Postgres (wspólnej z Django i Prismą). 