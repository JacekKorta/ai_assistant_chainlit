# Nginx

## Opis

Nginx pełni rolę reverse proxy w projekcie oraz serwuje pliki statyczne generowane przez Django.

## Konfiguracja

- Plik konfiguracyjny znajduje się w `nginx/nginx.conf`.
- Nginx nasłuchuje na porcie 80 i przekazuje żądania do backendu Django (usługa `web` na porcie 8000).
- Pliki statyczne są serwowane z katalogu `/app/staticfiles/`.

## Schemat działania

- Żądania do `/static/` są obsługiwane bezpośrednio przez Nginx.
- Pozostałe żądania są przekazywane do backendu Django.
- Nginx umożliwia komunikację między Chainlit a Django przez sieć docker-compose (adres `nginx`).

## Uruchamianie

- Nginx jest uruchamiany jako osobny kontener przez `docker compose up`.
- Wejście do powłoki kontenera: `make nginx-exec` 