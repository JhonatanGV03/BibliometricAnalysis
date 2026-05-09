import os
import shutil

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Inicializador del driver de chrome
def initialize_driver():
    download_directory = os.path.join(os.path.dirname(os.getcwd()), "Datos")

    prefs = {
        "download.default_directory": download_directory,  # Cambiar carpeta de descargas
        "download.prompt_for_download": False,  # No preguntar dónde guardar
        "download.directory_upgrade": False,  # Permitir sobreescritura
        "safebrowsing.enabled": True  # Evitar bloqueos de descargas
    }

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.get("https://library.uniquindio.edu.co/databases")

    wait = WebDriverWait(driver, 10)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "onload-background")))
    safe_click(driver, By.XPATH, "//summary[contains(normalize-space(), 'Fac. Ingeniería')]")

    return driver


def safe_click(driver, by, selector, timeout=60):
    """Intenta hacer clic en un elemento, esperando que sea interactuable."""
    wait = WebDriverWait(driver, timeout)

    # Esperar a que el elemento esté presente en el DOM
    element = wait.until(EC.presence_of_element_located((by, selector)))

    # Hacer scroll hasta el elemento
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # Esperar a que el elemento sea clickeable
    element = wait.until(EC.element_to_be_clickable((by, selector)))

    # Intentar hacer clic normalmente, si falla usar JavaScript
    try:
        element.click()
    except:
        driver.execute_script("arguments[0].click();", element)


def extraer_sd():
    driver = initialize_driver()
    time.sleep(5)
    driver.get("https://www.sciencedirect.com/search?qs=%22computational%20thinking%22")


def extraer_sage():
    driver = initialize_driver() # Inicializar el driver de Chrome
    wait = WebDriverWait(driver, 20)

    # Hacer clic en el enlace de SAGE
    try:
        sage_element = wait.until(
            EC.element_to_be_clickable((By.XPATH,"//a[contains(@href, 'journals.sagepub.com')]//span[contains(text(), 'SAGE Revistas Consorcio Colombia - (DESCUBRIDOR) ')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", sage_element)
        sage_element.click()
    except Exception as e:
        print(f"Error: No se pudo interactuar con el elemento SAGE. Detalle: {e}")

    # Iniciar sesión en Google
    safe_click(driver, By.ID, "btn-google")
    wait.until(EC.presence_of_element_located((By.ID, "identifierId"))).send_keys("y@uqvirtual.edu.co")
    safe_click(driver, By.XPATH, "//span[contains(text(), 'Siguiente')]")
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys("1124")
    safe_click(driver, By.XPATH, "//span[contains(text(), 'Siguiente')]")
    #time.sleep(10)

    # Manejo de cookies y busqueda
    safe_click(driver, By.ID, "onetrust-accept-btn-handler")
    wait.until(EC.presence_of_element_located((By.ID, "AllField35ea26a9-ec16-4bde-9652-17b798d5b6750"))).send_keys('"computational thinking"')
    safe_click(driver, By.CSS_SELECTOR, "button.btn.quick-search__button")
    driver.get("https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=%22computational+thinking%22&startPage=0&pageSize=100")
    safe_click(driver, By.ID, "onetrust-accept-btn-handler")
    time.sleep(2)

    # Descargar las citas en formato bibtex
    while True:
        try:
            time.sleep(5)
            safe_click(driver, By.XPATH, "//input[@id='action-bar-select-all']")
            print("Se ejecuta")
            time.sleep(1)
            safe_click(driver, By.XPATH, "//span[contains(text(), 'Export selected citations')]")
            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.ID, "citation-format"))).send_keys("bibtex")
            time.sleep(1)
            safe_click(driver, By.ID, "citation-format")
            time.sleep(1)
            safe_click(driver, By.XPATH, "//a[contains(@download, 'sage.bib')]")

            time.sleep(1)
            safe_click(driver, By.XPATH, "//div[@class='modal__header']//button")
            time.sleep(1)
            safe_click(driver, By.XPATH, "//a[contains(@class, 'next hvr-forward pagination__link')]")
        except Exception as e:
            print(f"No hay más páginas: {e}")
            break
    time.sleep(100)
    #driver.quit()

def eliminar_archivos(download_directory):
    if os.path.exists(download_directory):
        for archivo in os.listdir(download_directory):
            archivo_path = os.path.join(download_directory, archivo)
            try:
                if os.path.isfile(archivo_path):
                    os.remove(archivo_path)  # Borra archivos
                elif os.path.isdir(archivo_path):
                    shutil.rmtree(archivo_path)  # Borra subcarpetas
            except Exception as e:
                print(f"No se pudo borrar {archivo_path}: {e}")
    else:
        os.makedirs(download_directory)  # Si la carpeta no existe, la crea

def main():

    eliminar_archivos(os.path.join(os.path.dirname(os.getcwd()), "Datos"))
    extraer_sage()


if __name__ == "__main__":
    main()


def extraer_acm(driver):
    driver.get("https://dl.acm.org/action/doSearch?AllField=%22computational+thinking%22")



