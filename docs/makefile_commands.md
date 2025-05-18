# Makefile i komendy developerskie

W projekcie dostępny jest plik `Makefile`, który upraszcza zarządzanie kontenerami i usługami.

## Najważniejsze komendy

- `make up` – uruchomienie wszystkich kontenerów w trybie foreground
- `make upd` – uruchomienie wszystkich kontenerów w tle (detached)
- `make down` – zatrzymanie i usunięcie wszystkich kontenerów, sieci i wolumenów
- `make web-exec` – wejście do powłoki kontenera Django
- `make chainlit-exec` – wejście do powłoki kontenera Chainlit
- `make nginx-exec` – wejście do powłoki kontenera Nginx
- `make postgres-exec` – wejście do powłoki kontenera Postgres
- `make prisma-cli-exec` – wejście do powłoki kontenera Prisma CLI
- `make web-makemigrations` – tworzenie migracji Django
- `make web-migrate` – stosowanie migracji Django
- `make web-test` – uruchamianie testów Django

Każda z tych komend korzysta z `docker-compose` i pozwala na szybkie zarządzanie środowiskiem developerskim. 