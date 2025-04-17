# Boilerplate Template Django

Minimalistyczny szablon Django 5.2 z podstawowymi funkcjonalnościami do szybkiego rozpoczęcia nowego projektu.

## Funkcjonalności

- Gotowa aplikacja `accounts` z niestandardowym modelem użytkownika
- Podstawowe widoki logowania i wylogowania
- Konfiguracja przez plik YAML
- Obsługa statycznych plików przez Nginx
- Docker i docker-compose
- Zarządzanie zależnościami przez `uv`
- Skrypt do łatwej zmiany nazwy projektu

## Wymagania

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) - Szybki instalator pakietów Python
- Docker i docker-compose (opcjonalnie)

## Instalacja

1. Sklonuj repozytorium:

```bash
git clone https://github.com/twoj-username/boilerplate_template.git
cd boilerplate_template
```

2. Stwórz i aktywuj wirtualne środowisko:

```bash
python -m venv .venv
source .venv/bin/activate  # Na Linux/macOS
# LUB
.venv\Scripts\activate  # Na Windows
```

3. Zainstaluj zależności:

```bash
uv pip install -e .
```

4. Uruchom migracje:

```bash
uv run python manage.py migrate
```

5. Utwórz superużytkownika:

```bash
uv run python manage.py createsuperuser
```

6. Uruchom serwer deweloperski:

```bash
uv run python manage.py runserver
```

## Zmiana nazwy projektu

Aby zmienić nazwę projektu z "boilerplate_template" na własną, użyj skryptu:

```bash
uv run python rename_project.py moj_projekt [moje_konto]
```

Gdzie:
- `moj_projekt` to nowa nazwa projektu
- `moje_konto` to opcjonalna nowa nazwa dla aplikacji accounts

## Konfiguracja

1. Skopiuj plik `config.sample.yml` do `config.yml`:

```bash
cp config.sample.yml config.yml
```

2. Edytuj `config.yml` i dostosuj ustawienia zgodnie z potrzebami.

## Docker

Aby uruchomić projekt w Dockerze:

```bash
docker-compose up -d
```

## Struktura projektu

```
boilerplate_template/
├── accounts/              # Aplikacja accounts
│   ├── admin.py           # Konfiguracja panelu administracyjnego
│   ├── apps.py            # Konfiguracja aplikacji
│   ├── forms.py           # Formularze uwierzytelniania
│   ├── models.py          # Model użytkownika
│   ├── tests.py           # Testy aplikacji
│   ├── urls.py            # Konfiguracja URL aplikacji
│   └── views.py           # Widoki logowania/wylogowania
├── boilerplate_template/  # Główny moduł projektu
│   ├── asgi.py
│   ├── settings.py        # Ustawienia projektu
│   ├── urls.py            # Główne URL projektu
│   └── wsgi.py
├── nginx/                 # Konfiguracja Nginx
│   └── nginx.conf
├── static/                # Statyczne pliki
│   └── css/
│       └── styles.css
├── templates/             # Szablony HTML
│   ├── accounts/
│   │   ├── dashboard.html
│   │   └── login.html
│   └── base.html
├── Dockerfile             # Konfiguracja Docker
├── docker-compose.yml     # Konfiguracja docker-compose
├── config.sample.yml      # Przykładowa konfiguracja
├── manage.py              # Skrypt zarządzania Django
├── pyproject.toml         # Konfiguracja projektu
└── rename_project.py      # Skrypt do zmiany nazwy projektu
```
