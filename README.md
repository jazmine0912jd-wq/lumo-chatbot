# lumo-chatbot

**Lumo** ist ein anonymer Spielerschutz-Chatbot für Menschen mit Fragen zu Glücksspielverhalten. Er antwortet empathisch (basierend auf der Mistral-API), bietet auf Wunsch einen anonymen Selbsttest, informiert über Spielerschutz-Tools und vermittelt an Beratungsstellen. Gespräche bleiben vollständig anonym.

## Anonymität & Datenschutz

- Es werden **keine personenbezogenen Daten** erfragt (kein Name, keine Adresse, keine Kontodaten).
- Der Gesprächsverlauf wird **nur im Arbeitsspeicher** gehalten und beim Beenden gelöscht (`/clear` löscht ihn sofort). Es gibt keine Logs, keine Datenbank, keine Cookies.
- Das Selbsttest-Ergebnis wird **nicht gespeichert** und ist keine Diagnose.

## Voraussetzungen

- Python >= 3.10
- Ein Mistral-API-Key ([Mistral AI Console](https://console.mistral.ai/))

## Installation & Start

```bash
pip install -r requirements.txt
cp .env.example .env   # API-Key eintragen
python -m lumo
```

## Nutzung

Einfach frei schreiben. Befehle in der Konsole:

| Befehl | Funktion |
| --- | --- |
| `/selbsttest` | Anonymer Selbsttest (PGSI, 9 Fragen) |
| `/tools` | Spielerschutz-Tools (Limits, Spielpause, OASIS, Sperrsoftware …) |
| `/beratung` | Kostenlose, anonyme Beratungsstellen |
| `/clear` | Gesprächsverlauf im Arbeitsspeicher löschen |
| `/quit` | Chat beenden |

## Selbsttest

Der Selbsttest basiert auf dem **PGSI (Problem Gambling Severity Index)**: 9 Fragen zu den letzten 12 Monaten, Antworten `0 = nie` bis `3 = fast immer`, Gesamtscore 0–27.

- 0: kein erhöhtes Risiko
- 1–2: geringes Risiko
- 3–7: mittleres Risiko
- 8+: problematisches Spielverhalten

Das Ergebnis dient nur der Selbsteinschätzung und ersetzt keine professionelle Diagnose oder Beratung.

## Spielerschutz-Tools (Auszug)

- **LUGAS**: anbieterübergreifendes Einzahlungslimit (gesetzlich max. 1.000 €/Monat; Senken sofort, Erhöhen erst nach 7 Tagen)
- Einsatz-, Verlust- und Zeitlimits sowie Reality Checks beim Anbieter
- **Panik-Button / Spielpause**: sofortige 24-Stunden-Sperre bis zu längeren Pausen
- **OASIS**: bundesweite, anbieter- und spielformübergreifende Sperrdatei; freiwillige Selbstsperre ab 3 Monaten (Infos: [gluecksspiel-behoerde.de](https://www.gluecksspiel-behoerde.de))
- Sperrsoftware (z. B. BetBlocker, Gamban) und Banksperren für Glücksspielzahlungen

## Beratungsstellen (kostenlos & anonym)

- **BIÖG-Telefonberatung zur Glücksspielsucht**: 0800 1 37 27 00, Mo–Do 10–22 Uhr, Fr–So 10–18 Uhr, [check-dein-spiel.de](https://www.check-dein-spiel.de)
- **TelefonSeelsorge**: 0800 111 0 111 / 0800 111 0 222 / 116 123, rund um die Uhr, [telefonseelsorge.de](https://www.telefonseelsorge.de)
- **Krisenchat** für junge Menschen: [krisenchat.de](https://www.krisenchat.de)
- Suchtberatungsstellen vor Ort: [bundesweit-gegen-gluecksspielsucht.de](https://www.bundesweit-gegen-gluecksspielsucht.de), [dhs.de](https://www.dhs.de)
- Forum für Betroffene und Angehörige: [forum-gluecksspielsucht.de](https://www.forum-gluecksspielsucht.de)
- Bei akuter Gefahr: **Notruf 112**

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Hinweis

Lumo ist ein Informations- und Unterstützungsangebot. Er stellt keine medizinischen, psychologischen oder rechtlichen Diagnosen und ersetzt keine professionelle Beratung oder Therapie.
