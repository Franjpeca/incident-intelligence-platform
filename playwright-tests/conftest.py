# import pytest
#import pytest
#from playwright.sync_api import sync_playwright
#
## Lanza el motor de navegacion, el navegador
## Decorador que indica que esta funcion no es un test, si no una funcion de carga
## "session" indica que hasta que no se terminen los test no se cierra el navegador
## Si no abria que abrir y cerrar el navegador por cada test
#@pytest.fixture(scope="session")
#def browser():
#    # Context manager, para manejar memoria y evitar que se detenga el flujo aunque haya errores
#    with sync_playwright() as p:
#        # Se lanza el proceso del navegador, en modo no headless en este caso (se ve la ventana)
#        browser = p.chromium.launch(headless=False)
#        yield browser # Manda el navegador al test que se vaya a ejecutar y se queda esperando
#        browser.close() # Finalmente se cierra correctamente
#
#@pytest.fixture
#def page(browser):
#    # Se crea una sesion aislada, con cookies y otros elementos solo para esa sesion
#    context = browser.new_context()
#    # Se devuelve la pagina, es la pestaña del navegador y con la que interactuamos
#    page = context.new_page()
#    yield page  # Se envia la pagina y se queda en espera
#    context.close()
#
#
#