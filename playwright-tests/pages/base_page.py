# Clase padre del resto de paginas
class BasePage:
    # page: pestaña del navegador 
    # base_url: para indicar el servidor que estamos ejecutando las pruebas
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    # Funcion para acceder a una pagina concreta de nuestra web
    def goto(self, path):
        self.page.goto(f"{self.base_url}{path}")