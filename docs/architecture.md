# Architektura i zależności

Projekt składa się z kilku głównych komponentów, uruchamianych jako osobne kontenery Docker:

- **Django Backend** (`web`): Odpowiada za logikę biznesową, API oraz autoryzację użytkowników. Udostępnia endpointy REST, m.in. do weryfikacji danych logowania.
- **Nginx** (`nginx`): Pełni rolę reverse proxy. Przekazuje ruch HTTP na port 80 do backendu Django (na port 8000 w kontenerze `web`) oraz serwuje pliki statyczne z katalogu `/app/staticfiles/`.
- **Chainlit** (`chainlit`): Interfejs AI/chat, który korzysta z OpenAI oraz komunikuje się z backendem Django przez HTTP (np. do autoryzacji użytkowników). Łączy się z backendem przez adres http://nginx, korzystając z sieci docker-compose.
- **Postgres** (`postgres`): Wspólna baza danych dla Django i Prismy.
- **Prisma** (`prisma_cli`): ORM do wybranych usług, zarządza migracjami i schematem bazy danych.

## Schemat komunikacji

```
Użytkownik <-> Nginx <-> Django Backend
           <-> Chainlit <-> (Nginx <-> Django Backend)
```

- Użytkownik łączy się z aplikacją przez Nginx (http://localhost) lub Chainlit (http://localhost:8000).
- Chainlit, aby zweryfikować użytkownika, wysyła żądanie HTTP POST do endpointu Django `/api/accounts/verify-credentials/` przez Nginx (http://nginx/api/accounts/verify-credentials/).
- Nginx przekazuje żądania do backendu Django na porcie 8000.
- Wszystkie usługi korzystają z tej samej sieci Docker (`app_network`), co umożliwia komunikację po nazwach usług.

## Zależności

- Wszystkie kontenery są zarządzane przez `docker-compose.yml`.
- Pliki konfiguracyjne i zmienne środowiskowe są współdzielone przez `.env`.
- Prisma i Django korzystają z tej samej bazy danych Postgres.

Szczegóły konfiguracji znajdziesz w dokumentacji poszczególnych komponentów. 