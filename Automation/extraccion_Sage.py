import os
import time

from Automation import automatizacion


def safe_click(pagina, selector):
    element = pagina.wait_for_selector(selector, state="attached")
    #element.scroll_into_view_if_needed()
    element.wait_for_element_state("visible")
    element.wait_for_element_state("enabled")
    element.click()

def extraer_sage(playwright, navegador, pagina):
    try:
        # Acceder al enlace de sage
        pagina.locator("div[data-content-listing-item='fac-ingenier-a']").click()
        link = pagina.locator("//a[contains(@href, 'journals.sagepub.com')]//span[contains(text(), 'SAGE Revistas - (DESCUBRIDOR) ')]")
        pagina.wait_for_load_state("domcontentloaded")
        link.click()

        #Iniciar sesión con correo institucional
        automatizacion.iniciar_sesion(pagina)

        # Manejo de cookies y busqueda
        safe_click(pagina, "#onetrust-accept-btn-handler")
        pagina.wait_for_load_state("domcontentloaded")
        pagina.fill("#AllField35ea26a9-ec16-4bde-9652-17b798d5b6750", '"computational thinking"')
        safe_click(pagina, "button.btn.quick-search__button")
        pagina.wait_for_load_state("domcontentloaded")
        pagina.goto("https://journals-sagepub-com.crai.referencistas.com/action/doSearch?AllField=%22computational+thinking%22&startPage=0&pageSize=100&AfterYear=2020&BeforeYear=2025")
        #safe_click(pagina, "#onetrust-accept-btn-handler")
        #pagina.fill('#range-slider-start', '2020')
        #pagina.locator('#range-slider-start').press('Enter')
        time.sleep(2)
        pagina.wait_for_selector(".loader-wrapper", state="detached")
        pagina.wait_for_load_state("domcontentloaded")

        # Descarga de citas en formato bibtex
        i = 0
        while True:
            try:
                i+=1
                # Seleccionar todas las citas y presionar el botón de exportar
                pagina.wait_for_selector(".loader-wrapper", state="detached")
                safe_click(pagina,"//input[@id='action-bar-select-all']")
                time.sleep(1)
                safe_click(pagina,"xpath=//span[contains(text(), 'Export selected citations')]")
                pagina.wait_for_load_state("domcontentloaded")
                time.sleep(5)

                #Seleccionar el formato de exportación y esperar que se habilite la descarga
                pagina.wait_for_selector("//div[@class='csl-entry']", state="visible")
                pagina.select_option("#citation-format", "bibtex")
                pagina.wait_for_load_state("domcontentloaded")
                time.sleep(1)
                pagina.wait_for_selector("//a[contains(@download, 'sage.bib')]", state="visible")

                # Descargar archivo
                with pagina.expect_download() as download_info:
                    pagina.locator("//a[contains(@download, 'sage.bib')]").click()
                download = download_info.value
                download_path = os.path.join(os.getcwd(), "Data/DownloadedCitations", f"sage_{i}.bib")
                download.save_as(download_path)
                print(f"Archivo descargado en: {download_path}")

                #Manejo de la paginación
                safe_click(pagina, "xpath=//div[@class='modal__header']//button")
                next_button = pagina.locator("xpath=//a[contains(@class, 'next hvr-forward pagination__link')]")

                if next_button.get_attribute("disabled") == "true":
                    print("El botón 'Next' está deshabilitado. Fin del proceso.")
                    break

                # Pasar a la siguiente página
                safe_click(pagina, "xpath=//a[contains(@class, 'next hvr-forward pagination__link')]")
                pagina.wait_for_load_state("domcontentloaded")
                time.sleep(2)

            except Exception as e:
                print(f"No hay más páginas.{e}")
                break


    except Exception as e:
        print(f"Exception: {e}")
        navegador.close()
        playwright.stop()
        return