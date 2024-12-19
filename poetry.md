
# Gedanken zu Poetry / Venv

## Warum überhaupt Virtual Environments?

Damit das Projekt unabängig von der Python-Installation auf deinem Rechner ist. 
Man will sich nicht jede Abhängigkeit eines einzelnen Projektes auf seiner globalen Installation holen, 
da man A) sich diese dabei gerne mal zerschießt und B) Dadurch Konflikte zwischen verschiedenen Projekten entstehen können.

Poetry hat die meiner Meinung nach sehr nützliche zusätzlich Fähigkeit, solche Abhängigkeiten mitzudokumentieren
und eine vereinfachte Installation anzubieten.

**Ohne Poetry**  Irgendwer entscheidet sich matplotlib zum plotten zu verwenden > Er installiert in seiner venv mit `pip install matplotlib` > Ich pull, Oh Mist!, das gibt mir einen Error, dependency resulution funktioniert nicht, ärgerlich, mal schauen ob jemand das Requirements.txt upgedatet hat. Wie? Das macht keiner? > Ich suche und installiere mir manuell die neue Dependency matplotlib und bete das es die richtige Version ist

**Mit Poetry** Irgendwer entscheidet sich matplotlib zum plotten zu verwenden > Er fügt mit dem Befehl `poetry add matplotlib` die Dependency in die Virtuelle Umgebung und ins toml hinzu > Ich pull, ich verwende `poetry install` > Poetry installiert automatisch alle benötigten Dependencies in die Poetry shell

Prinzipiell ist es auch möglich zweigleisig zu fahren, so dass jeder seine eigenen virtuelle Umgebung verwendet.
Für die Nutzer von Venv ändert das überhaupt nichts, außer das im Git Dateien liegen, die sie nicht brauchen. Für die Poetry Nutzer heißt das, dass sie eben trotzdem Dependencies manuell hinzufügen müssen, wenn ein Nicht-Poetry-Nutzer sie einführt.

---

## Tabellarischer Vergleich  

| **Aspekt**              | **Poetry**                                                                                                                                      | **venv**                                                                                           |  
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|  
| **Abhängigkeitsmanagement** | Poetry nutzt eine **Lock-Datei** (`poetry.lock`), um exakt festgelegte Versionen der Abhängigkeiten zu sichern. | venv selbst bietet kein Abhängigkeitsmanagement. Alles muss über `requirements.txt` gepflegt werden. |                                       |  
| **Bedienung**             | `poetry add django` fügt Abhängigkeiten hinzu, und `poetry remove django` entfernt sie.                                             | Manuell: `pip install django`, dann `pip freeze > requirements.txt`.                              |  
| **Reproduzierbarkeit**    | Dank `poetry.lock` identische Umgebungen für alle Teammitglieder.                                                                             | Abhängigkeiten können variieren, da `requirements.txt` nur die Hauptpakete listet. Und manuell gepflegt werden muss.               |  
| **Installation**          | Poetry muss separat installiert werden.                                                                                                      | venv ist Teil der Standardbibliothek und immer verfügbar.                                         |  
| **Projektstruktur**       | Poetry integriert alles in der Datei `pyproject.toml`, inklusive Skripten und Metadaten.                                                     | Mit venv braucht man zusätzlich `setup.py` oder `requirements.txt`, was oft unübersichtlich ist.  |  
 

### **Zusammenfassung der Vorteile von Poetry**  
- Automatisiertes und transparentes Abhängigkeitsmanagement.  
- Konsistenz durch die Lock-Datei (`poetry.lock`).  
- Modernes Tool mit klaren und gut strukturierten Befehlen.  

---

## Wichtige Commands: Poetry und venv zum Abgleich

| **Aufgabe**                                   | **Poetry**                                  | **venv**                                                                                             |  
|-----------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------------------------------|  
| **Virtuelle Umgebung erstellen**              | Automatisch bei `poetry install`.           | `python -m venv .venv`                                                                               |  
| **Virtuelle Umgebung aktivieren**             | `poetry shell`           | `source .venv/bin/activate` (Linux/Mac) oder `.venv\Scripts\activate` (Windows)                     |  
| **Abhängigkeit hinzufügen**                   | `poetry add <paket>`                        | `pip install <paket>` und danach `pip freeze > requirements.txt`                                     |  
| **Abhängigkeit entfernen**                    | `poetry remove <paket>`                     | `pip uninstall <paket>` und danach `pip freeze > requirements.txt`                                   |  
| **Abhängigkeiten installieren**               | `poetry install`                            | `pip install -r requirements.txt`                                                                   |  
| **Alle Abhängigkeiten auflisten**             | `poetry show`                               | `pip list`                                                                                          |  
| **Projektdetails ansehen**                    | `poetry show --tree`                        | Nicht direkt verfügbar; erfordert zusätzliche Tools wie `pipdeptree`.                               |  
| **Aktuelle Umgebung aktualisieren**           | `poetry update`                             | Manuelles Editieren der `requirements.txt` und `pip install -r requirements.txt`                    |  
 
  
---

## Installation

Sollte für alle funtionieren
`curl -sSL https://install.python-poetry.org | python3 -`
ansonsten konsultiert
https://python-poetry.org/docs