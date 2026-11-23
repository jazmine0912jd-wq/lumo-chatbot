from lumo.resources import (
    COUNSELING_SERVICES,
    CRISIS_MESSAGE,
    PROTECTION_TOOLS,
    format_counseling_services,
    format_protection_tools,
)


def test_crisis_message_contains_emergency_numbers():
    assert "0800 111 0 111" in CRISIS_MESSAGE
    assert "0800 111 0 222" in CRISIS_MESSAGE
    assert "116 123" in CRISIS_MESSAGE
    assert "112" in CRISIS_MESSAGE


def test_every_service_has_name_description_and_contact():
    for service in COUNSELING_SERVICES:
        assert service.name.strip()
        assert service.description.strip()
        assert service.phone or service.website


def test_bzga_hotline_is_listed():
    text = format_counseling_services()
    assert "0800 1 37 27 00" in text
    assert "check-dein-spiel.de" in text


def test_protection_tools_cover_oasis_and_lugas():
    text = format_protection_tools()
    assert "OASIS" in text
    assert "LUGAS" in text
    assert "Panik-Button" in text
    assert len(PROTECTION_TOOLS) >= 5
