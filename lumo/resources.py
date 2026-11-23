from dataclasses import dataclass


@dataclass(frozen=True)
class CounselingService:
    name: str
    description: str
    phone: str | None = None
    website: str | None = None
    hours: str | None = None


@dataclass(frozen=True)
class ProtectionTool:
    name: str
    description: str


CRISIS_MESSAGE = (
    "Es tut mir leid, dass du dich gerade so fühlst. Du musst da nicht allein durch. "
    "Bitte wende dich jetzt an Menschen, die dir helfen können:\n"
    "- TelefonSeelsorge: 0800 111 0 111 oder 0800 111 0 222 (auch 116 123) - "
    "rund um die Uhr, kostenlos und anonym, auch per Chat und Mail auf telefonseelsorge.de\n"
    "- Krisenchat fur junge Menschen: krisenchat.de\n"
    "- Bei akuter Gefahr: Notruf 112\n"
    "- BIÖG-Telefonberatung zur Glücksspielsucht: 0800 1 37 27 00 (kostenlos, anonym)\n"
    "Wenn du magst, reden wir danach uber alles, was dich beschaftigt."
)

COUNSELING_SERVICES = (
    CounselingService(
        name="BIÖG-Telefonberatung zur Glücksspielsucht",
        description=(
            "Kostenfreie, anonyme Telefonberatung fur Betroffene und Angehorige, "
            "auch mit Online-Beratung per Chat/Mail und anonymem Selbsttest."
        ),
        phone="0800 1 37 27 00",
        website="https://www.check-dein-spiel.de",
        hours="Mo-Do 10-22 Uhr, Fr-So 10-18 Uhr",
    ),
    CounselingService(
        name="TelefonSeelsorge",
        description="Kostenlose, anonyme Krisenberatung bei allen Sorgen - rund um die Uhr.",
        phone="0800 111 0 111 / 0800 111 0 222 / 116 123",
        website="https://www.telefonseelsorge.de (Chat/Mail: online.telefonseelsorge.de)",
        hours="rund um die Uhr",
    ),
    CounselingService(
        name="Krisenchat",
        description="Chat-Beratung von jungen Menschen fur Jugendliche und junge Erwachsene.",
        website="https://www.krisenchat.de",
    ),
    CounselingService(
        name="Suchtberatungsstellen vor Ort",
        description=(
            "Personliche Beratung bei Suchtberatungsstellen (z. B. Caritas, Diakonie). "
            "Die BIÖG-Hotline nennt auf Wunsch Stellen in deiner Nahe."
        ),
        website=(
            "https://www.bundesweit-gegen-gluecksspielsucht.de und https://www.dhs.de"
        ),
    ),
    CounselingService(
        name="Forum fur Betroffene und Angehorige",
        description="Anonymer Austausch mit anderen Betroffenen und Angehorigen.",
        website="https://www.forum-gluecksspielsucht.de",
    ),
)

PROTECTION_TOOLS = (
    ProtectionTool(
        name="Einzahlungslimit (LUGAS)",
        description=(
            "Anbieterubergreifendes Einzahlungslimit, gesetzlich auf 1.000 EUR pro Monat "
            "begrenzt. Senken geht sofort, Erhohen erst nach 7 Tagen Wartezeit."
        ),
    ),
    ProtectionTool(
        name="Einsatz-, Verlust- und Zeitlimits",
        description=(
            "Beim Anbieter lassen sich personliche Limits fur Einsatze, Verluste und "
            "Spielzeit festlegen."
        ),
    ),
    ProtectionTool(
        name="Reality Check",
        description="Regelmassige Hinweise wahrend des Spiels zu Spieldauer, Einsatzen und Verlusten.",
    ),
    ProtectionTool(
        name="Spielpause / Panik-Button",
        description=(
            "Sofortige 24-Stunden-Sperre (Panik-Button) bis zu langeren freiwilligen Pausen - "
            "niedrigschwellig beim Anbieter aktivierbar."
        ),
    ),
    ProtectionTool(
        name="Selbstsperre uber OASIS",
        description=(
            "Bundesweite, anbieter- und spielformubergreifende Sperrdatei. Freiwillige "
            "Selbstsperre ab 3 Monaten (kurzere 24h-Sperre moglich), Antrag beim Anbieter "
            "oder beim Regierungsprasidium Darmstadt. Infos: gluecksspiel-behoerde.de"
        ),
    ),
    ProtectionTool(
        name="Sperrsoftware",
        description=(
            "Programme wie BetBlocker oder Gamban blockieren den Zugang zu "
            "Glucksspiel-Websites und -Apps - auch bei Anbietern ohne deutsche Lizenz."
        ),
    ),
    ProtectionTool(
        name="Banksperre fur Glucksspielzahlungen",
        description="Viele Banken bieten einen Block fur Glucksspiel-Transaktionen auf dem Konto an.",
    ),
    ProtectionTool(
        name="Eigenes Budget",
        description=(
            "Nur mit festem Budget spielen, das man entbehren kann - und nie Geld leihen, "
            "um weiterzuspielen oder Verluste zuruckzugewinnen."
        ),
    ),
)


def format_counseling_services() -> str:
    lines = []
    for service in COUNSELING_SERVICES:
        line = f"- {service.name}"
        details = []
        if service.phone:
            details.append(f"Tel: {service.phone}")
        if service.hours:
            details.append(service.hours)
        if service.website:
            details.append(service.website)
        if details:
            line += " (" + ", ".join(details) + ")"
        line += f": {service.description}"
        lines.append(line)
    return "\n".join(lines)


def format_protection_tools() -> str:
    return "\n".join(
        f"- {tool.name}: {tool.description}" for tool in PROTECTION_TOOLS
    )
