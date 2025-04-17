<highlight_summary>
Projekt polega na stworzeniu minimalistycznego szablonu dla aplikacji Django, który będzie stanowił punkt wyjścia dla przyszłych projektów. Celem jest dostarczenie kompletnego, ale uproszczonego boilerplate'u, który użytkownicy mogą łatwo rozszerzać i dostosowywać do swoich potrzeb. Szablon ma być wyposażony w podstawowe funkcjonalności, takie jak konfiguracja Nginx do obsługi statycznych plików, struktura projektu zgodna z najlepszymi praktykami Django oraz integracja z Dockerem i `uv` do zarządzania środowiskiem i zależnościami. Dodatkowo, szablon będzie zawierał podstawowe widoki logowania i wylogowania oraz skrypt umożliwiający łatwą zmianę nazw projektu, co zwiększy jego elastyczność i użyteczność.
</highlight_summary>

<decisions>
1. Użycie Django w wersji 5.2 z SQLite jako bazą danych na początek.
2. Dodanie aplikacji accounts z CustomUser na bazie AbstractUser, ale początkowo bez dodatkowych pól.
3. Użycie Nginx do serwowania statycznych plików, z odpowiednią konfiguracją w szablonie.
4. Brak obsługi plików mediów w szablonie.
5. Użycie Django Template Engine i ograniczenie się do podstawowego boilerplate.
6. Zawartość szablonu ma obejmować Dockerfile z multi-stage builds i zarządzanie pakietami przez `uv`.
7. Wykorzystanie YAML do konfiguracji środowiska zamiast `.env`.
8. Użycie jednego pliku `settings.py` z wartościami pobieranymi z konfiguracji.
9. Dodanie podstawowych testów dla widoków logowania i wylogowania, preferencja dla Django/Unit Test.
10. Stworzenie prostego skryptu do zmiany nazw projektu w szablonie.
11. Szablon może nie zawierać frontendu, a jesli zawiera to bardzo uproszczony, np z czystym htmlem. i tak będzie zmieniany użytkowników szablonu.
</decisions>

<matched_recommendations>
1. Stworzenie skryptu do automatycznej zmiany nazw w projekcie.
2. Dodanie konfiguracji Nginx dla statycznych plików w szablonie.
3. Uwzględnienie podstawowych testów w szablonie.
4. Użycie YAML do zarządzania konfiguracją środowiska.
5. Wdrożenie struktur projektowych zgodnych z konwencją Django.
6. Zastosowanie multi-stage Dockerfile dla efektywności budowy.
</matched_recommendations>

<prd_planning_summary>
a. **Główne wymagania funkcjonalne produktu:**
   - Minimalistyczny szablon Django z podstawowym boilerplate, gotowy do rozszerzenia przez użytkowników.
   - Konfiguracja Nginx dla obsługi statycznych plików.
   - Użycie Docker i `uv` do zarządzania środowiskiem i zależnościami.

b. **Kluczowe historie użytkownika i ścieżki korzystania:**
   - Użytkownik może łatwo rozpocząć nowy projekt Django, korzystając z gotowego szablonu.
   - Możliwość modyfikacji i rozbudowy szablonu poprzez dodanie własnych modeli i funkcjonalności.

c. **Ważne kryteria sukcesu i sposoby ich mierzenia:**
   - Szablon jest łatwy w użyciu i konfigurowalny przez użytkowników.
   - Konfiguracja Docker i Nginx działa poprawnie i wspiera rozwój aplikacji.
   - Testy dla funkcjonalności logowania i wylogowania przechodzą pomyślnie.

</prd_planning_summary>

</conversation_summary>