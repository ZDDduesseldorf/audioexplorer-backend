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
- bandit
- pip-audit
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

## 11. Security Scan lokal ausführen

Der Security Scan besteht aktuell aus zwei Prüfungen:

- `bandit` prüft den eigenen Python-Code auf typische sicherheitsrelevante Muster.
- `pip-audit` prüft die installierten Python-Abhängigkeiten auf bekannte Schwachstellen.

Die benötigten Tools werden über `requirements.txt` installiert:

```bash
python -m pip install -r requirements.txt
```

Aktuell enthält `requirements.txt` dafür zusätzlich:

```txt
bandit
pip-audit
```

Außerdem ist FastAPI bewusst auf eine konkrete Version gepinnt. Wenn `pip-audit` für eine Version eine Schwachstelle meldet, wird die betroffene Version nicht ignoriert, sondern gezielt angepasst.

Beispiel:

```txt
fastapi[standard]==0.136.1
```

## Bandit ausführen

Im Repository-Root:

```bash
python -m bandit -r app scripts -ll -ii
```

Dabei werden aktuell der Anwendungscode unter `app/` und die Hilfsskripte unter `scripts/` geprüft.

Die Optionen bedeuten:

- `-r`: rekursiv prüfen
- `-ll`: nur Findings ab mittlerer Severity anzeigen
- `-ii`: nur Findings ab mittlerer Confidence anzeigen

Wenn Bandit keine sicherheitsrelevanten Probleme findet, erscheint sinngemäß:

```text
No issues identified.
```

## Dependency Scan mit pip-audit ausführen

Im Repository-Root:

```bash
pip-audit
```

Wenn keine bekannten Schwachstellen in den installierten Python-Paketen gefunden werden, erscheint:

```text
No known vulnerabilities found
```

Wenn `pip-audit` bekannte Schwachstellen findet, schlägt der Check fehl. Ein Security-Befund soll nicht dauerhaft mit Konstruktionen wie `pip-audit || true` ignoriert werden.

Stattdessen wird geprüft, ob eine sichere installierbare Version verfügbar ist. Danach werden die Dependencies neu installiert und die Checks erneut ausgeführt.

Beispiel:

```bash
python -m pip install -r requirements.txt
pip-audit
```

## Security Scan absichtlich fehlschlagen lassen

Um zu testen, ob Bandit funktioniert, kann temporär eine unsichere Testfunktion eingefügt werden.

Beispiel in einer Python-Datei unter `app/`:

```python
def temporary_security_test() -> object:
    return eval("1 + 1")
```

Danach Bandit ausführen:

```bash
python -m bandit -r app scripts -ll -ii
```

Bandit sollte diese Stelle melden.

Wichtig: Diese Testfunktion darf nicht committed werden. Danach die Änderung wieder entfernen oder die Datei zurücksetzen:

```bash
git restore app/api/sound_controller.py
```

## 12. Kompletter lokaler Prüfablauf vor einem Push

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
python -m bandit -r app scripts -ll -ii
pip-audit
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

Wenn alle Checks erfolgreich sind, ist der lokale Stand bereit für Push oder Pull Request.

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
doc
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

## 13. Typische Commit-Messages

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
doc
```

Die Types werden wie folgt verwendet:

- `feat`: neue fachliche Funktionalität
- `fix`: Fehlerbehebung oder Korrektur einer problematischen Dependency-Version
- `test`: Tests, Coverage, API Contract oder Security-Checks
- `ci`: Änderungen an der CI/CD-Pipeline oder GitHub-Actions-Konfiguration
- `doc`: Änderungen an Dokumentation oder Anleitung

Beispiele:

```text
feat(backend): add FastAPI setup
fix(backend): correct labeled sample naming
fix(backend): downgrade vulnerable FastAPI version
test(backend): add API endpoint tests
test(backend): add coverage reporting
test(backend): add API integration tests
test(backend): add OpenAPI contract test
test(backend): add security scan
ci(backend): add security scan to pipeline
doc(backend): document security scan workflow
```

Für Änderungen am API Contract nach bewusster API-Änderung kann zum Beispiel verwendet werden:

```text
test(backend): update OpenAPI contract
```

Für die Einführung des Security Scans in der Pipeline passt:

```text
ci(backend): add security scan to pipeline
```

Für die Dokumentation des Security Scans in dieser Anleitung passt:

```text
doc(backend): document security scan workflow
```

Für das Beheben einer verwundbaren Dependency-Version passt:

```text
fix(backend): downgrade vulnerable FastAPI version
```

Wenn Pipeline, Anleitung und Dependency-Korrektur gemeinsam committed werden, kann pragmatisch auch eine zusammenfassende Commit-Message verwendet werden:

```text
ci(backend): add security scan
```

## 14. Empfohlener Ablauf bei API-Änderungen

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
python -m bandit -r app scripts -ll -ii
pip-audit
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

Wenn der Diff in `api_contract/openapi.json` fachlich gewollt ist, wird die Datei mitcommitted.

Wenn alles grün ist:

```bash
git status
git add .
git status
git commit -m "test(backend): update OpenAPI contract"
git push
```

Wenn zusätzlich eine verwundbare Dependency-Version angepasst wurde, kann stattdessen eine passende Commit-Message verwendet werden:

```bash
git commit -m "fix(backend): downgrade vulnerable FastAPI version"
```

Wenn nur die Anleitung geändert wurde, passt:

```bash
git commit -m "doc(backend): document security scan workflow"
```

Wenn nur die GitHub-Actions-Pipeline geändert wurde, passt:

```bash
git commit -m "ci(backend): add security scan to pipeline"
```

## 15. Docker Build und lokaler Start

Das Backend enthält bereits ein `Dockerfile` im Repository-Root.

Der Docker-Build prüft, ob aus dem aktuellen Backend-Code ein lauffähiges Docker Image gebaut werden kann.

Für die lokale Ausführung wird **Docker Desktop** als Runtime-Umgebung empfohlen. Docker Desktop sollte gestartet sein, bevor die folgenden Befehle ausgeführt werden.

Im Repository-Root ausführen:

```bash
docker build -t audioexplorer-api:local .
```

Danach prüfen, ob das Image lokal vorhanden ist:

```bash
docker images audioexplorer-api
```

Das Image kann anschließend lokal gestartet werden:

```bash
docker run --rm -p 8000:8000 audioexplorer-api:local
```

Die API sollte danach erreichbar sein unter:

```text
http://localhost:8000/docs
```

Alternativ kann die Erreichbarkeit per `curl` geprüft werden:

```bash
curl -fsS http://127.0.0.1:8000/docs
```

Wenn der Container läuft, kann er im Terminal mit `CTRL+C` beendet werden.

## Docker Image aus GitHub Actions herunterladen

In der GitHub-Actions-Pipeline wird das Docker Image gebaut und zusätzlich als komprimiertes Artifact gespeichert.

Dafür wird das Image in der Pipeline mit `docker save` exportiert:

```bash
docker save audioexplorer-api:<commit-sha> | gzip > audioexplorer-api-image.tar.gz
```

Das Artifact kann nach einem erfolgreichen Workflow Run in GitHub heruntergeladen werden:

```text
Repository → Actions → Workflow Run öffnen → Artifacts → audioexplorer-api-image-...
```

Nach dem Download kann das Image lokal geladen werden.

Unter Git Bash, Linux oder macOS:

```bash
gunzip audioexplorer-api-image.tar.gz
docker load -i audioexplorer-api-image.tar
docker images audioexplorer-api
```

Danach kann das geladene Image gestartet werden:

```bash
docker run --rm -p 8000:8000 audioexplorer-api:<commit-sha>
```

Wenn der konkrete Commit-SHA-Tag unhandlich ist, kann lokal zusätzlich ein einfacher Tag vergeben werden:

```bash
docker tag audioexplorer-api:<commit-sha> audioexplorer-api:downloaded
docker run --rm -p 8000:8000 audioexplorer-api:downloaded
```

Hinweis:

Aktuell installiert das Dockerfile die Dependencies aus `requirements.txt`. Dadurch landen vorerst auch Entwicklungs- und CI-Tools wie `ruff`, `mypy`, `pytest`, `bandit` und `pip-audit` im Image. Für den aktuellen CI/CD-Aufbau ist das akzeptabel. Vor Staging oder Production sollte später geprüft werden, ob Runtime- und Development-Dependencies getrennt werden.