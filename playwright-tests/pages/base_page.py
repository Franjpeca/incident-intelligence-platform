# Clase padre, el resto de paginas toman informacion de esta
# En vez de en cada pagina indicar cosas como url etc, se hace en esta clase y se hereda
class BasePage:
    # Self: este mismo objeto
    # page: pestaña del navegador 
    # base_url: para indicar el servidor que estamos ejecutando las pruebas
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    # Funcion que accede al path especificado
    # Toma la pagina indicada al crear el objeto y se mueve a esa pagina
    # Es para navegar por las diferentes paginas
    def goto(self, path):
        self.page.goto(f"{self.base_url}{path}")