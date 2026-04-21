# By, para capturar los elementos
from selenium.webdriver.common.by import By
# Driver para espera implicita
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Clase base
# Contiene codigo comun para el resto de clases de las paginas
class BasePage:

    # Constructor de la clase
    # Obtiene el driver, la URL de la web
    # Tambien el tiempo a esperar con el webdriverwait
    def __init__(self, driver, base_url, timeout=10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)
        self._timeout = timeout

    # Para poder movernos a una direccion concreta
    def goto(self, path):
        self.driver.get(f"{self.base_url}{path}")

    # By contiene el tipo de elemento a encontrar
    # Value el valor de ese elemento a encontrar
    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    # Devuelve todos los elementos del tipo indicado con by y con la etiqueta indicada en value
    def find_all(self, by, value):
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))

    # Realizar un click
    def click(self, by, value):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    # Fill sera el texto a introducir
    def fill(self, by, value, text):
        element = self.find(by, value)
        # Hay que hacer clear porque send_keys escribe sobre lo que hay, no borra de por si
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        element = self.find(by, value)
        return element.text

    def wait_for_text(self, by, value, text, custom_timeout=None):
        wait = self.wait if custom_timeout is None else WebDriverWait(self.driver, custom_timeout)
        wait.until(EC.text_to_be_present_in_element((by, value), text))