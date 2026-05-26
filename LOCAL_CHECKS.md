# Lokale CI/CD-Prüfschritte für das Audioexplorer Backend

Diese Datei beschreibt die lokalen Schritte, die vor einem Push oder Pull Request im Backend-Repository ausgeführt werden sollten.

Ziel ist, lokal möglichst dieselben Prüfungen auszuführen, die später auch in GitHub Actions laufen.

## Lokale Entwicklungsumgebung mit Conda einrichten

Für die lokale Entwicklung kann eine gemeinsame Conda-Umgebung verwendet werden. Dieser Schritt ist nur für Personen relevant, die lokal mit Anaconda oder Miniconda arbeiten.

Der Name der vorgesehenen Conda-Umgebung lautet:

```bash
backend-cicd
```

Die Umgebung wird aus der Datei `environment.yml` erstellt:

```bash
conda env create -f environment.yml
```

Anschließend wird die Umgebung aktiviert:

```bash
conda activate backend-cicd
```

Danach werden die Python-Projektabhängigkeiten aus `requirements.txt` installiert:

```bash
python -m pip install -r requirements.txt
```

Damit ist sichergestellt, dass lokal mit derselben Python-Basis und denselben Projektabhängigkeiten gearbeitet wird wie im restlichen Team.

Zur Kontrolle können folgende Befehle ausgeführt werden:

```bash
python --version
python -m pip --version
python -m pytest --version
```

Wenn die Conda-Umgebung bereits existiert und aktualisiert werden soll, kann sie mit folgendem Befehl aktualisiert werden:

```bash
conda env update -f environment.yml --prune
```

Danach sollten die Projektabhängigkeiten erneut installiert werden:

```bash
python -m pip install -r requirements.txt
```

## 1. Voraussetzungen

Das Backend verwendet aktuell:

- Python 3.12
- FastAPI
- Pydantic
- Ruff
- mypy
- pytest
- httpx
- pytest-cov
- Docker für Container-Builds

Prüfen, ob die richtige Umgebung aktiv ist:

```bash
python --version
python -m pip --version
```

Wenn in der Shell noch `(base)` steht, ist vermutlich noch nicht die richtige Umgebung aktiv.

## 2. Dependencies installieren oder aktualisieren

Im Repository-Root ausführen:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Der Repository-Root ist der Ordner, in dem unter anderem diese Dateien und Ordner liegen:

```text
app/
tests/
integration_tests/
contract_tests/
api_contract/
scripts/
requirements.txt
Dockerfile
.github/
```

## 3. Formatierung prüfen

Ruff Formatter prüft, ob alle Dateien korrekt formatiert sind.

```bash
python -m ruff format --check --diff .
```

Wenn dieser Check fehlschlägt, lokal automatisch formatieren:

```bash
python -m ruff format .
```

Danach den Check erneut ausführen:

```bash
python -m ruff format --check --diff .
```

## 4. Linting ausführen

Ruff prüft zusätzlich typische Codeprobleme, zum Beispiel ungenutzte Imports.

```bash
python -m ruff check .
```

Falls Ruff automatisch behebbare Probleme meldet, kann optional ausgeführt werden:

```bash
python -m ruff check . --fix
```

Danach erneut prüfen:

```bash
python -m ruff check .
```

## 5. Typecheck ausführen

mypy prüft die Typannotationen des Anwendungscodes.

```bash
python -m mypy app
```

Wenn dieser Schritt fehlschlägt, müssen die gemeldeten Typfehler im Code korrigiert werden.

Typische Ursachen:

- falscher Rückgabetyp einer Funktion
- fehlende Typannotationen
- falscher Importpfad
- Rückgabe eines `str`, obwohl ein Pydantic-Modell erwartet wird

## 6. Unit-nahe API-Tests ausführen

Die Tests im Ordner `tests/` verwenden FastAPIs `TestClient` und testen die App direkt im Python-Prozess.

```bash
python -m pytest tests -v
```

Diese Tests brauchen keinen laufenden Uvicorn-Server.

## 7. Coverage lokal erzeugen

Coverage misst, welche Teile des Anwendungscodes durch Tests abgedeckt werden.

```bash
python -m pytest tests -v --cov=app --cov-report=term-missing --cov-report=xml
```

Dabei wird zusätzlich diese Datei erzeugt:

```text
coverage.xml
```

Diese Datei wird später für SonarQube relevant sein, soll aber nicht ins Git-Repository committed werden.

`coverage.xml` sollte deshalb in `.gitignore` stehen:

```gitignore
.coverage
coverage.xml
htmlcov/
```

Aktuell ist noch kein Mindestwert aktiv. Das bedeutet: Die Pipeline bricht nicht wegen niedriger Coverage, sondern nur, wenn Tests fehlschlagen oder der Coverage-Lauf technisch nicht funktioniert.

Ein späterer Mindestwert könnte so ergänzt werden:

```bash
python -m pytest tests -v --cov=app --cov-report=term-missing --cov-report=xml --cov-fail-under=80
```

## 8. Integration Tests ausführen

Die Integration Tests im Ordner `integration_tests/` sprechen die laufende FastAPI-App über echtes HTTP an.

Dafür werden zwei Terminals benötigt.

### Terminal 1: App starten

Im Repository-Root:

```bash
conda activate backend-cicd
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Die App sollte danach erreichbar sein unter:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2: Integration Tests ausführen

Im Repository-Root:

```bash
conda activate backend-cicd
python -m pytest integration_tests -v
```

Wenn die App nicht läuft, dürfen die Integration Tests fehlschlagen. Das ist korrekt, weil sie bewusst gegen eine laufende HTTP-Instanz testen.

## 9. API Contract prüfen

Der API Contract wird aus dem von FastAPI generierten OpenAPI-Schema abgeleitet.

Die gespeicherte Referenzdatei liegt hier:

```text
api_contract/openapi.json
```

Der Contract-Test vergleicht den aktuell von FastAPI generierten Contract mit dieser gespeicherten Datei.

Contract-Test ausführen:

```bash
python -m pytest contract_tests -v
```

Wenn dieser Test fehlschlägt, gibt es zwei mögliche Ursachen:

1. Die API wurde absichtlich geändert.
2. Die gespeicherte Datei `api_contract/openapi.json` ist nicht mehr synchron mit dem aktuellen Code oder den aktuellen Dependencies.

## 10. API Contract bei API-Änderungen neu generieren

Wenn sich die API absichtlich geändert hat, zum Beispiel durch:

- neuen Endpoint
- entfernten Endpoint
- geänderten Pfad
- geändertes Response-Modell
- geändertes Schema
- geänderte API-Metadaten wie Titel, Version oder Beschreibung

muss der OpenAPI-Contract bewusst neu generiert werden.

Dafür im Repository-Root ausführen:

```bash
python -m scripts.export_openapi
```

Danach prüfen:

```bash
python -m pytest contract_tests -v
```

Anschließend den Contract-Diff bewusst ansehen:

```bash
git diff api_contract/openapi.json
```

Wenn der Diff fachlich gewollt ist, wird die Datei mitcommitted:

```bash
git add api_contract/openapi.json
```

Wichtig: In der CI-Pipeline soll `python -m scripts.export_openapi` nicht automatisch direkt vor dem Contract-Test ausgeführt werden. Sonst würde der Test jede Änderung automatisch akzeptieren und könnte unbeabsichtigte API-Änderungen nicht mehr erkennen.

## 11. Kompletter lokaler Prüfablauf vor einem Push

Wenn keine Integration Tests benötigt werden oder die App nicht separat gestartet ist:

```bash
conda activate backend-cicd
python -m pip install -r requirements.txt
python -m ruff format --check --diff .
python -m ruff check .
python -m mypy app
python -m pytest tests -v
python -m pytest tests -v --cov=app --cov-report=term-missing --cov-report=xml
python -m pytest contract_tests -v
```

Mit Integration Tests zusätzlich:

Terminal 1:

```bash
conda activate backend-cicd
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
conda activate backend-cicd
python -m pytest integration_tests -v
```

## 12. Typische Commit-Messages

Das aktuelle Commit-Schema lautet:

```text
<type>(backend): <short description>
```

Erlaubte Types:

```text
feat
fix
test
ci
```

Beispiele:

```text
feat(backend): add FastAPI setup
fix(backend): correct labeled sample naming
test(backend): add API endpoint tests
test(backend): add coverage reporting
test(backend): add API integration tests
test(backend): add OpenAPI contract test
```

Für Änderungen am API Contract nach bewusster API-Änderung kann zum Beispiel verwendet werden:

```text
test(backend): update OpenAPI contract
```

## 13. Empfohlener Ablauf bei API-Änderungen

Wenn ein Endpoint oder Schema geändert wird:

```bash
conda activate backend-cicd
python -m pip install -r requirements.txt
python -m ruff format .
python -m ruff check .
python -m mypy app
python -m pytest tests -v
python -m pytest tests -v --cov=app --cov-report=term-missing --cov-report=xml
python -m scripts.export_openapi
python -m pytest contract_tests -v
git diff api_contract/openapi.json
```

Wenn Integration Tests betroffen sind, zusätzlich:

Terminal 1:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
python -m pytest integration_tests -v
```

Wenn alles grün ist:

```bash
git status
git add .
git status
git commit -m "test(backend): update OpenAPI contract"
git push
```