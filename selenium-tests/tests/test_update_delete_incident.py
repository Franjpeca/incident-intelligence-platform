import pytest
from utils.assertions import assert_incident_exists, assert_incident_not_exists

from pages.update_delete_incident_page import UpdateDeleteIncidentPage

# Funcion test que prueba la actualizacion general de una incidencia
def test_update_incident(driver, base_url, fixture_create_incident):

    incident_id = fixture_create_incident["id"]


    update_page = UpdateDeleteIncidentPage(driver, base_url)

    update_page.goto()

    # Actualizamos la incidencia
    update_page.update_incident(
        incident_id,
        title="Actualizando titulo usando selenium",
        description="Actualizacion de la descripcion",
        status="in_progress"
    )

    try:
        update_page.wait_for_update_success_feedback()
    except Exception:
        error_visible = update_page.get_update_feedback_text()

        pytest.fail(
            f"No se pudo actualizar la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = update_page.get_update_feedback_text().lower()
    response = update_page.get_update_response_text().lower()

    assert "incidencia actualizada correctamente" in feedback
    assert f'"id": {incident_id}' in response
    assert '"title": "actualizando titulo usando selenium"' in response
    assert '"description": "actualizacion de la descripcion"' in response
    assert '"status": "in_progress"' in response

    # Comprobamos ademas que la incidencia se ve actualizada desde la pagina de consulta
    assert_incident_exists(driver, base_url, incident_id, "actualizando titulo usando selenium")


def test_update_incident_status(driver, base_url, fixture_create_incident):

    incident_id = fixture_create_incident["id"]

    update_page = UpdateDeleteIncidentPage(driver, base_url)

    update_page.goto()

    update_page.update_status_only(incident_id, "closed")

    try:
        update_page.wait_for_status_success_feedback()
    except Exception:
        error_visible = update_page.get_status_feedback_text()

        pytest.fail(
            f"No se pudo actualizar el estado de la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = update_page.get_status_feedback_text().lower()
    response = update_page.get_status_response_text().lower()

    assert "estado actualizado correctamente" in feedback
    assert f'"id": {incident_id}' in response
    assert '"status": "closed"' in response


def test_delete_incident(driver, base_url, fixture_create_incident):

    incident_id = fixture_create_incident["id"]

    update_page = UpdateDeleteIncidentPage(driver, base_url)

    update_page.goto()

    update_page.update_status_only(incident_id, "closed")

    # Borramos la incidencia
    update_page.delete_incident(incident_id)

    try:
        update_page.wait_for_delete_success_feedback()
    except Exception:
        error_visible = update_page.get_delete_feedback_text()

        pytest.fail(
            f"No se pudo borrar la incidencia con id {incident_id}.\n"
            f"Mensaje devuelto por la web: '{error_visible}'"
        )

    feedback = update_page.get_delete_feedback_text().lower()

    assert "incidencia borrada correctamente" in feedback

    assert_incident_not_exists(driver, base_url, incident_id)