# prisma/build/Dockerfile
# Użyj oficjalnego obrazu Node.js (wersja LTS Alpine jest zwykle mniejsza)
FROM node:lts-alpine as builder

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki package.json i package-lock.json (jeśli istnieje)
# Kopiujemy je najpierw, aby wykorzystać cache warstw Docker
COPY ./prisma/package.json ./package.json
# Jeśli używasz package-lock.json, odkomentuj poniższą linię
# COPY ./prisma/package-lock.json ./package-lock.json

# Zainstaluj zależności zdefiniowane w package.json, w tym Prisma CLI
RUN npm install

# Skopiuj resztę plików z katalogu prisma (głównie schema.prisma)
COPY ./prisma ./prisma

# Ustaw domyślny punkt wejścia, aby ułatwić uruchamianie poleceń Prisma
# ENTRYPOINT ["npx", "prisma"]
# Zamiast ENTRYPOINT, użyjemy command w docker-compose, aby kontener działał

# Możesz dodać domyślne polecenie, jeśli chcesz, np. do wyświetlenia pomocy
# CMD ["--help"]
