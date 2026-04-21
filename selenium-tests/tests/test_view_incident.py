import pytest

from pages.view_incident_page import ViewIncidentPage


def test_view_incident_by_id(driver, base_url, fixture_create_incident):
    incident_id = fixture_create_incident["id"]

    view_page = ViewIncidentPage(driver, base_url)

    view_page.goto()

    view_page.search_incident_by_id(incident_id)

    try:
        view_page.wait_for_search_success_feedback()
    except Exception:
        error_visible = view_page.get_search_feedback_text()

        pytest.fail(
            f"No se pudo encontrar la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = view_page.get_search_feedback_text().lower()
    response = view_page.get_search_response_text().lower()

    assert "incidencia encontrada" in feedback
    assert f'"id": {incident_id}' in response
    # Debemos comprobarlo con lo devuelto en la incidencia
    assert f'"title": "{fixture_create_incident["title"].lower()}"' in response



def test_view_all_incidents(driver, base_url, fixture_create_incident):
    created_incident = fixture_create_incident

    view_page = ViewIncidentPage(driver, base_url)

    view_page.goto()

    view_page.load_all_incidents()

    try:
        view_page.wait_for_list_success_feedback()
    except Exception:
        error_visible = view_page.get_list_feedback_text()

        pytest.fail(
            f"No se pudieron cargar las incidencias.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = view_page.get_list_feedback_text().lower()
    incidents_list = view_page.get_incidents_list_text().lower()

    assert created_incident["id"] is not None
    assert "incidencias cargadas" in feedback
    assert fixture_create_incident["title"].lower() in incidents_list