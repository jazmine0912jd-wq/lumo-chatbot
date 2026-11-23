PGSI_SKALA = ["0 – nie", "1 – manchmal", "2 – die meiste Zeit", "3 – fast immer"]

PGSI_FRAGEN = [
    "Haben Sie jemals mehr Geld eingesetzt, als Sie sich leisten konnten?",
    "Mussten Sie jemals mit höheren Einsätzen spielen, um das gleiche Gefühl der Aufregung zu bekommen?",
    "Haben Sie jemals wieder gespielt, um verlorenes Geld zurückzugewinnen?",
    "Haben Sie jemals Geld geliehen oder etwas verkauft, um Geld für das Glücksspiel zu bekommen?",
    "Haben Sie jemals das Gefühl gehabt, dass das Glücksspiel Ihnen Probleme bereiten könnte?",
    "Hat Ihnen das Glücksspiel jemals gesundheitliche Probleme bereitet, einschließlich Stress oder Angstzustände?",
    "Hat Ihnen das Glücksspiel jemals finanzielle Probleme bereitet?",
    "Haben Ihnen andere jemals Bedenken hinsichtlich Ihres Glücksspiels geäußert oder Ihnen gesagt, dass Sie ein Problem mit dem Glücksspiel haben könnten?",
    "Hat Ihr Glücksspiel jemals zu Problemen in Ihrer Beziehung, mit Familie oder Freunden geführt?",
]

ANTWORT_WERTE = {
    "0": 0, "nie": 0,
    "1": 1, "manchmal": 1,
    "2": 2, "die meiste zeit": 2, "meiste zeit": 2, "meistens": 2,
    "3": 3, "fast immer": 3, "immer": 3,
}

ABBRUCH_WORTE = {"abbrechen", "stopp", "stop", "ende", "quit", "exit", "abbruch"}


def antwort_parsen(text: str):
    t = text.strip().lower()
    if t in ABBRUCH_WORTE:
        return "abbruch"
    if t in ANTWORT_WERTE:
        return ANTWORT_WERTE[t]
    return None


def auswertung(score: int) -> str:
    if score == 0:
        return (
            "Dein Ergebnis: **0 Punkte** – kein auffälliges Spielverhalten erkennbar.\n\n"
            "Das ist ein gutes Zeichen. Trotzdem gilt: Spiel nur mit Geld, das du entbehren kannst. "
            "Wenn du Fragen hast, bin ich gerne für dich da."
        )
    if score <= 2:
        return (
            f"Dein Ergebnis: **{score} Punkt(e)** – geringes Risiko.\n\n"
            "Es gibt erste Anzeichen, dass das Spielen für dich belastend werden könnte. "
            "Ein paar Schutzmaßnahmen können helfen: Einzahlungslimit setzen, Spielpausen einlegen, "
            "Reality-Checks aktivieren. Wenn du möchtest, zeige ich dir die Spielerschutz-Tools."
        )
    if score <= 7:
        return (
            f"Dein Ergebnis: **{score} Punkte** – mittleres Risiko (problematisches Spielverhalten möglich).\n\n"
            "Mehrere Antworten deuten darauf hin, dass das Glücksspiel bereits negative Folgen für dich hat. "
            "Das ist kein Grund für Scham – es passiert vielen Menschen. Sinnvolle nächste Schritte: "
            "eine Spielpause oder Selbstsperre (OASIS) in Betracht ziehen und professionelle, kostenlose "
            "Beratung nutzen, z. B. das BIÖG-Beratungstelefon **0800 1 37 27 00** (anonym, kostenfrei) "
            "oder [check-dein-spiel.de](https://www.check-dein-spiel.de)."
        )
    return (
        f"Dein Ergebnis: **{score} Punkte** – hohes Risiko (wahrscheinliches problematisches bzw. pathologisches Spielverhalten).\n\n"
        "Deine Antworten zeigen deutliche Anzeichen einer Glücksspielproblematik. Bitte nimm das ernst – "
        "du musst das nicht allein tragen. Wichtige nächste Schritte:\n"
        "- **Sofort**: Spielpause oder Selbstsperre über OASIS beantragen (bundesweit, spielformübergreifend).\n"
        "- **Beratung (kostenlos & anonym)**: BIÖG-Telefonberatung Glücksspielsucht **0800 1 37 27 00** "
        "(Mo–Do 10–22 Uhr, Fr–So 10–18 Uhr) oder [check-dein-spiel.de](https://www.check-dein-spiel.de).\n"
        "- Beratungsstelle in deiner Nähe: [bundesweit-gegen-gluecksspielsucht.de](https://www.bundesweit-gegen-gluecksspielsucht.de).\n\n"
        "Dieser Test ersetzt keine Diagnose, aber er ist ein wichtiges Warnsignal. "
        "Sprich mit einer Fachkraft – das kann wirklich helfen."
    )
