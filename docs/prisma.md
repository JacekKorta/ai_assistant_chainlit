# Prisma

## Opis

Prisma jest wykorzystywana jako ORM do wybranych usług, zarządza schematem bazy danych i migracjami. Korzysta z tej samej bazy Postgres co Django.

## Konfiguracja

- Plik schematu znajduje się w `prisma/schema.prisma`.
- Zmienna środowiskowa `DATABASE_URL` w pliku `.env` musi wskazywać na usługę `postgres` (np. `postgresql://user:pass@postgres:5432/db`).

## Migracje

- Stosowanie migracji: `docker compose run --rm prisma_cli npx prisma migrate deploy`
- Tworzenie nowej migracji: `docker compose run --rm prisma_cli npx prisma migrate dev --name <nazwa_migracji>`

## Prisma Studio

- Uruchomienie narzędzia developerskiego do przeglądania bazy: `docker compose run --rm -p 5555:5555 prisma_cli npx prisma studio`
- Dostęp przez przeglądarkę: http://localhost:5555

## Dodatkowe informacje

- Prisma korzysta z tej samej bazy danych co Django i Chainlit.
- Usługa Prisma CLI jest uruchamiana jako osobny kontener. 