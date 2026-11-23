import os

DEFAULT_MODEL = os.environ.get("LUMO_MODEL", "mistral-medium-latest")

SYSTEM_PROMPT = """Du bist Lumo, ein anonymer, empathischer Chatbot zum Thema Spielerschutz und Glücksspielverhalten in Deutschland.

Deine Haltung:
- Sei warm, wertschätzend und niemals verurteilend. Sprich die Nutzer:in mit „du" an, in einfachen, klaren Sätzen.
- Stelle keine Diagnosen. Formuliere vorsichtig, z. B. „das könnte ein Hinweis sein".
- Sei ehrlich und konkret, aber halte Antworten kompakt (max. ca. 150 Wörter).

Deine Aufgaben:
1. Empathisch auf Fragen, Sorgen und Belastungen rund um das eigene Glücksspielverhalten (oder das von Angehörigen) antworten.
2. Auf Wunsch einen anonymen Selbsttest anbieten (9 Fragen, basiert auf dem PGSI). Der Selbsttest wird direkt im Chat geführt – die Antworten werden nirgendwo gespeichert.
3. Über Spielerschutz-Tools informieren:
   - OASIS-Sperrsystem: bundesweit und spielformübergreifend, geführt beim Regierungspräsidium Darmstadt. Selbstsperre mindestens 3 Monate (24-Stunden-Sofortsperre direkt beim Anbieter möglich), Fremdsperre mindestens 1 Jahr. Antrag beim Regierungspräsidium Darmstadt oder bei jedem teilnehmenden Glücksspielanbieter. Infos: rp-darmstadt.hessen.de und gluecksspiel-behoerde.de.
   - Einzahlungslimit: In Deutschland sind über alle lizenzierten Anbieter hinweg höchstens 1.000 € Einzahlung pro Monat möglich; das Limit kann direkt beim Anbieter gesenkt werden.
   - Reality-Checks (Anzeige von Spielzeit und Gewinn/Verlust) und Spielpausen aktivieren.
   - Selbstausschluss direkt beim Anbieter (Konto pausieren oder sperren).
   - Reize reduzieren: Newsletter abbestellen, Apps vom Startbildschirm entfernen, Benachrichtigungen aus.
   - Nur mit Geld spielen, das entbehrlich ist – nie mit geliehenem Geld.
4. Auf kostenlose, anonyme Hilfsangebote verweisen:
   - BIÖG „Check dein Spiel": https://www.check-dein-spiel.de – Selbsttests, Infos, Online-Beratung per Chat/E-Mail, kostenlos und anonym.
   - Telefonberatung Glücksspielsucht (BIÖG): 0800 1 37 27 00 – kostenfrei aus dem deutschen Fest- und Mobilnetz, anonym; Mo–Do 10–22 Uhr, Fr–So 10–18 Uhr.
   - Suchtberatungsstelle in der Nähe: https://www.bundesweit-gegen-gluecksspielsucht.de
   - TelefonSeelsorge: 0800 111 0 111 oder 0800 111 0 222 (auch 116 123) – rund um die Uhr, kostenfrei, anonym.

Wichtige Regeln:
- Frage niemals nach Namen, Adresse, Telefonnummer oder anderen identifizierenden Daten. Das Gespräch ist vollständig anonym und wird nicht gespeichert.
- Wenn jemand von Selbstharm, Suizid oder einer akuten Krise spricht: Nimm das ernst, antworte einfühlsam und nenne sofort die TelefonSeelsorge (0800 111 0 111 / 0800 111 0 222 / 116 123) sowie bei akuter Gefahr den Notruf 112. Empfehle dringend, professionelle Hilfe in Anspruch zu nehmen.
- Mache keine Versprechen („das wird schon wieder") und keine Schuldzuweisungen.
- Lumo ersetzt keine medizinische oder psychologische Beratung.
"""

TEXT_SPIIELERSCHUTZ = """🛡️ **Spielerschutz-Tools im Überblick**

- **OASIS-Sperrsystem** (bundesweit, spielformübergreifend): Selbstsperre mind. 3 Monate – Antrag beim Regierungspräsidium Darmstadt oder direkt bei einem teilnehmenden Anbieter; zusätzlich 24-Stunden-Sofortsperre beim Anbieter. Fremdsperre (z. B. durch Angehörige) mind. 1 Jahr. Infos: [rp-darmstadt.hessen.de](https://rp-darmstadt.hessen.de/sicherheit-und-kommunales/gluecksspiel/spielersperrsystem-oasis) und [gluecksspiel-behoerde.de](https://www.gluecksspiel-behoerde.de/de/fuer-gluecksspielanbieter/aufsichtssysteme/spielersperrdatei).
- **Einzahlungslimit**: Über alle lizenzierten deutschen Anbieter hinweg max. 1.000 € Einzahlung pro Monat – das Limit kannst du direkt beim Anbieter senken.
- **Reality-Check & Spielpause**: Im Spiel anzeigen lassen, wie lange und mit welchem Ergebnis du spielst; Pausen direkt aktivieren.
- **Selbstausschluss beim Anbieter**: Konto pausieren oder dauerhaft sperren lassen.
- **Reize reduzieren**: Werbe-Newsletter abbestellen, Glücksspiel-Apps vom Startbildschirm entfernen, Benachrichtigungen ausschalten.
- **Goldene Regel**: Nur mit Geld spielen, das du entbehren kannst – nie mit geliehenem Geld oder Geld für Miete/Rechnungen.

Soll ich dir auch die Beratungsangebote zeigen?"""

TEXT_BERATUNG = """📞 **Kostenlose & anonyme Beratung**

- **BIÖG „Check dein Spiel"**: [check-dein-spiel.de](https://www.check-dein-spiel.de) – Selbsttests, Informationen und Online-Beratung per Chat/E-Mail, kostenlos und anonym.
- **Telefonberatung Glücksspielsucht (BIÖG)**: **0800 1 37 27 00** – kostenfrei aus dem deutschen Fest- und Mobilnetz, anonym. Zeiten: Mo–Do 10–22 Uhr, Fr–So 10–18 Uhr.
- **Suchtberatungsstelle in deiner Nähe**: [bundesweit-gegen-gluecksspielsucht.de](https://www.bundesweit-gegen-gluecksspielsucht.de) (Verzeichnis nach Postleitzahl).
- Auch Angehörige können sich dort kostenlos und anonym beraten lassen.

Möchtest du vorher den anonymen Selbsttest machen, um dein Spielverhalten einzuschätzen?"""

TEXT_SOFORTHILFE = """🆘 **Wenn es dir gerade sehr schlecht geht**

- **TelefonSeelsorge**: **0800 111 0 111** oder **0800 111 0 222** (auch **116 123**) – rund um die Uhr, kostenfrei, anonym.
- Bei akuter Gefahr für Leib oder Leben: **Notruf 112**.
- **Glücksspielsucht-Beratung (BIÖG)**: **0800 1 37 27 00** (kostenfrei, anonym; Mo–Do 10–22 Uhr, Fr–So 10–18 Uhr) oder [check-dein-spiel.de](https://www.check-dein-spiel.de).

Du bist nicht allein, und es ist ein starker Schritt, Hilfe anzunehmen. Bitte wende dich jetzt an eine dieser Nummern."""

TEXT_SELBSTTEST_INTRO = (
    "Gerne! Der Selbsttest besteht aus **9 kurzen Fragen** (basierend auf dem wissenschaftlich geprüften PGSI) "
    "und dauert etwa 2 Minuten. Er ist **vollständig anonym** – deine Antworten werden nur in dieser "
    "Browser-Sitzung angezeigt und nirgendwo gespeichert. Denk bei den Antworten an die **letzten 12 Monate**.\n\n"
    "Antworte auf jede Frage mit **0 = nie**, **1 = manchmal**, **2 = die meiste Zeit** oder **3 = fast immer**. "
    "Zum Abbrechen jederzeit „abbrechen“ schreiben.\n\n"
)

KRISE_KEYWORDS = [
    "suizid", "selbstmord", "nicht mehr leben", "leben beenden", "umbringen",
    "selbstharm", "ritzen", "alles vorbei", "keinen sinn mehr", "töt",
]


class LumoBot:
    def __init__(self, api_key: str | None, model: str = DEFAULT_MODEL, demo_mode: bool = False):
        self.api_key = api_key
        self.model = model
        self.demo_mode = demo_mode or not api_key
        self._client = None
        if not self.demo_mode:
            from mistralai import Mistral
            self._client = Mistral(api_key=api_key)

    @property
    def uses_api(self) -> bool:
        return self._client is not None

    def chat(self, messages: list[dict]) -> str:
        if self.demo_mode:
            return self._demo_response(messages[-1]["content"])
        response = self._client.chat.complete(
            model=self.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages,
            temperature=0.7,
            max_tokens=600,
        )
        return response.choices[0].message.content.strip()

    def _demo_response(self, user_text: str) -> str:
        t = user_text.lower()
        if any(k in t for k in KRISE_KEYWORDS):
            return TEXT_SOFORTHILFE
        if "selbsttest" in t or "test" in t:
            return "Im Demo-Modus ist der Selbsttest als Schaltfläche oben im Chat verfügbar. Starte ihn mit „🧪 Selbsttest starten“."
        if any(k in t for k in ["sperre", "oasis", "limit", "schutz", "tool", "pause"]):
            return TEXT_SPIIELERSCHUTZ
        if any(k in t for k in ["beratung", "hilfe", "telefon", "hotline", "stelle", "anlauf"]):
            return TEXT_BERATUNG
        return (
            "Danke, dass du das mit mir teilst. (Demo-Modus – für echte Antworten per Mistral-API "
            "bitte MISTRAL_API_KEY in der .env setzen.) Ich höre dir zu: Was beschäftigt dich gerade "
            "am meisten am Spielen? Du kannst auch oben „🧪 Selbsttest starten“ wählen."
        )
