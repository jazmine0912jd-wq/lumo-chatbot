# lumo-chatbot


Lumo ist ein anonymer Chatbot für Menschen mit Fragen zu Glücksspielverhalten. Er antwortet
empathisch (Mistral-API), bietet auf Wunsch einen anonymen Selbsttest (PGSI, 9 Fragen), informiert
über Spielerschutz-Tools (OASIS-Sperre, Einzahlungslimits, Reality-Checks, Spielpausen) und
vermittelt an Beratungsstellen. Gespräche werden **nirgends gespeichert** – nur in der
Browser-Sitzung (Streamlit `session_state`).

## Web-Oberfläche starten

```bash
cd lumo
pip install -r requirements.txt
cp .env.example .env   # eigenen MISTRAL_API_KEY eintragen
streamlit run app.py
```

Die Oberfläche ist dann im Browser unter **http://localhost:8501** erreichbar.

Ohne API-Key läuft die App automatisch im **Demo-Modus** (lokale Fallback-Antworten), damit die
Oberfläche trotzdem getestet werden kann.

## Struktur

- `app.py` – Streamlit-Web-App (Chat-UI, Schnellaktionen, Selbsttest-Ablauf)
- `lumo_core.py` – System-Prompt, Mistral-Client, Demo-Fallback, kuratierte Inhalte
  (Spielerschutz-Tools, Beratungsstellen, Soforthilfe)
- `selbsttest.py` – PGSI-Selbsttest (9 Fragen, Auswertung 0 / 1–2 / 3–7 / 8+)
- `.env.example` – Vorlage für `MISTRAL_API_KEY` und `LUMO_MODEL`

## Anonymität

- Keine Abfrage identifizierender Daten, kein Logging der Gespräche.
- Chat-Verlauf und Selbsttest-Antworten liegen nur in `st.session_state` (pro Browser-Sitzung).

## Wichtige Hilfsangebote (auch im Chat)

- BIÖG „Check dein Spiel": https://www.check-dein-spiel.de (kostenlos, anonym)
- Telefonberatung Glücksspielsucht: **0800 1 37 27 00** (kostenfrei, anonym; Mo–Do 10–22, Fr–So 10–18 Uhr)
- OASIS-Sperrsystem (Selbst-/Fremdsperre): Antrag beim Regierungspräsidium Darmstadt oder beim Anbieter
- Beratungsstellen vor Ort: https://www.bundesweit-gegen-gluecksspielsucht.de
- TelefonSeelsorge: **0800 111 0 111** / **0800 111 0 222** / **116 123** (rund um die Uhr, kostenfrei, anonym)

## Hinweis

Lumo ersetzt keine medizinische oder psychologische Beratung und stellt keine Diagnosen.
