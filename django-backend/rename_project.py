#!/usr/bin/env python
"""
Skrypt do zmiany nazwy projektu i aplikacji w szablonie Django.

Użycie:
    python rename_project.py <nowa_nazwa_projektu> [nowa_nazwa_aplikacji_accounts]

Przykład:
    python rename_project.py moj_projekt moje_konto
"""

import os
import sys
import fileinput
import re
import shutil


def replace_in_file(file_path, old_str, new_str):
    """Zastępuje wszystkie wystąpienia starej nazwy na nową w pliku."""
    if not os.path.isfile(file_path):
        print(f"Plik {file_path} nie istnieje.")
        return

    print(f"Przetwarzanie pliku: {file_path}")
    
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            print(line.replace(old_str, new_str), end='')


def rename_file_or_dir(old_path, new_path):
    """Zmienia nazwę pliku lub katalogu."""
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Zmieniono nazwę: {old_path} -> {new_path}")
    else:
        print(f"Ścieżka {old_path} nie istnieje.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    new_project_name = sys.argv[1]
    old_project_name = "boilerplate_template"
    
    # Opcjonalna zmiana nazwy aplikacji accounts
    new_app_name = sys.argv[2] if len(sys.argv) > 2 else "accounts"
    old_app_name = "accounts"

    # Lista plików do przetworzenia
    file_list = [
        "manage.py",
        f"{old_project_name}/settings.py",
        f"{old_project_name}/urls.py",
        f"{old_project_name}/asgi.py",
        f"{old_project_name}/wsgi.py",
        f"{old_app_name}/apps.py",
        "templates/base.html",
    ]

    # Zastąp nazwy w plikach
    for file_path in file_list:
        replace_in_file(file_path, old_project_name, new_project_name)
        if new_app_name != old_app_name:
            replace_in_file(file_path, old_app_name, new_app_name)

    # Zmień nazwę katalogu projektu
    rename_file_or_dir(old_project_name, new_project_name)
    
    # Zmień nazwę katalogu aplikacji jeśli potrzeba
    if new_app_name != old_app_name:
        rename_file_or_dir(old_app_name, new_app_name)
        
        # Zaktualizuj ścieżki w szablonach
        template_files = [
            f"templates/base.html",
            f"templates/{old_app_name}/login.html",
            f"templates/{old_app_name}/dashboard.html",
        ]
        
        # Utwórz katalog dla nowych szablonów
        os.makedirs(f"templates/{new_app_name}", exist_ok=True)
        
        # Przenieś pliki szablonów
        for template_file in os.listdir(f"templates/{old_app_name}"):
            old_file = f"templates/{old_app_name}/{template_file}"
            new_file = f"templates/{new_app_name}/{template_file}"
            shutil.copy2(old_file, new_file)
            replace_in_file(new_file, old_app_name, new_app_name)
            
        # Usuń stare pliki szablonów
        shutil.rmtree(f"templates/{old_app_name}")
            
    print("\nPomyślnie zmieniono nazwę projektu.")
    print(f"Stara nazwa: {old_project_name}")
    print(f"Nowa nazwa: {new_project_name}")
    
    if new_app_name != old_app_name:
        print(f"Stara nazwa aplikacji: {old_app_name}")
        print(f"Nowa nazwa aplikacji: {new_app_name}")
        
    print("\nPamiętaj o uruchomieniu następujących komend:")
    print(f"cd {new_project_name}")
    print("uv run python manage.py makemigrations")
    print("uv run python manage.py migrate")


if __name__ == "__main__":
    main() 