import os
import time

from Automation import automatizacion


def safe_click(pagina, selector):
    element = pagina.wait_for_selector(selector, state="attached")
    #element.scroll_into_view_if_needed()
    element.wait_for_element_state("visible")
    element.wait_for_element_state("enabled")
    element.click()


def extraer_sd(playwright, navegador, pagina):
    # Crear una nueva pestaña en el navegador
    contexto = pagina.context
    pagina = contexto.new_page()
    pagina.goto("https://library.uniquindio.edu.co/databases")
    pagina.bring_to_front()
    pagina.wait_for_load_state("domcontentloaded")

    try:
        # Acceder al enlace de IEEE
        pagina.locator("div[data-content-listing-item='fac-ingenier-a']").click()
        link = pagina.locator(
            "//a[contains(@href, 'https://www.sciencedirect.com')]//span[contains(text(), 'SCIENCEDIRECT - (DESCUBRIDOR)')]")
        pagina.wait_for_load_state("domcontentloaded")
        link.last.click()

        # Iniciar sesión con correo institucional en caso de ser necesario
        if pagina.url != "https://www-sciencedirect-com.crai.referencistas.com/":
            automatizacion.iniciar_sesion(pagina)

        # Manejo de la búsqueda
        safe_click(pagina, '//span[contains(text(), "Advanced search")]')
        pagina.wait_for_load_state("domcontentloaded")
        pagina.wait_for_selector("//textarea[@id='qs']", timeout=60000)
        time.sleep(1)
        pagina.locator("//textarea[@id='qs']").fill('"computational thinking"')
        pagina.locator("//input[@id='date']").fill('2020-2025')
        time.sleep(1)
        pagina.locator('//button[@type="submit"]//span//span').click()
        time.sleep(5)
        pagina.wait_for_load_state("domcontentloaded")

        # Seleccion de n resultados por pagina
        safe_click(pagina, '//span[contains(text(), "100")]')
        pagina.wait_for_load_state("domcontentloaded")

        # Descarga de citas en formato bibtex
        i = 0
        while True:
            try:
                i += 1
                pagina.wait_for_selector("div.LoadingOverlay.show", state="hidden", timeout=60000)

                # Seleccionar todas las citas y presionar el botón de exportar
                pagina.locator("//input[@id='select-all-results']").click(force=True)
                pagina.wait_for_load_state("domcontentloaded")
                pagina.locator("button.button-link.export-all-link-button.button-link-primary.button-link-icon-left").click()
                pagina.wait_for_load_state("domcontentloaded")
                time.sleep(1)

                # Descargar archivo
                with pagina.expect_download() as download_info:
                    pagina.wait_for_selector('//span[contains(text(), "Export citation to BibTeX")]', timeout=10000).click()
                download = download_info.value
                download_path = os.path.join(os.getcwd(), "Data/DownloadedCitations", f"ScienceDirect_{i}.bib")
                download.save_as(download_path)
                print(f"Archivo descargado en: {download_path}")
                time.sleep(1)
                pagina.locator("//input[@id='select-all-results']").click(force=True)

                # Manejo de paginación
                next_button = pagina.get_by_role("link", name="next", exact=True)

                if not next_button.is_visible():
                    print("El botón 'Next' no es visible. Fin del proceso.")
                    break

                next_button.click()
                pagina.wait_for_load_state("domcontentloaded")
                time.sleep(2)

            except Exception as e:
                print(f"No hay más páginas.{e}")
                break

        navegador.close()
        playwright.stop()

    except Exception as e:
        print(f"Exception: {e}")
        navegador.close()
        playwright.stop()
        return