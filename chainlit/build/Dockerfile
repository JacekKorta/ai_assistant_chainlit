###########
# BUILDER #
###########

FROM python:3.12-slim as builder

WORKDIR /app

# Ustawienie zmiennych środowiskowych
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Instalacja uv
RUN pip install uv

# Kopiowanie plików zależności
COPY chainlit/pyproject.toml /app/

# Instalacja zależności
RUN uv pip install --system -e .

# Kopiowanie pozostałych plików projektu
COPY chainlit /app/


# #########
# # FINAL #
# #########

FROM python:3.12-slim

WORKDIR /app

# Ustawienie zmiennych środowiskowych
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalacja zależności
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Kopiowanie plików projektu
COPY --from=builder /app/ /app/

# Uruchomienie serwera Gunicorn
CMD ["uv", "run", "chainlit", "run", "main.py", "--host", "0.0.0.0", "--port", "8000", "-h"]