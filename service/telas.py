import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from service.navegacao import avancar

def identificar_tela(driver) -> str:
    avancar(driver)

    try:
        WebDriverWait(driver, 15).until(lambda d:
            d.find_elements(By.XPATH, "//td[@role='gridcell']") or
            d.find_elements(By.XPATH, "//span[contains(normalize-space(.), 'Agendamentos no período de:')]")
        )
    except TimeoutException:
        return "desconhecido"

    if driver.find_elements(By.XPATH, "//td[@role='gridcell']"):
        return "unidades"

    if driver.find_elements(By.XPATH, "//span[contains(normalize-space(.), 'Agendamentos no período de:')]"):
        return "preenchido"

    return "desconhecido"

def obter_periodo_agenda_preenchida(driver) -> tuple[str, str] | None:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(normalize-space(.), 'Agendamentos no período de:')]"))
        )
    except TimeoutException:
        return None

    spans = driver.find_elements(By.XPATH, "//span[contains(@style,'color:red')]")
    datas = [s.text.strip() for s in spans if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s.text.strip())]
    return (datas[0], datas[1]) if len(datas) >= 2 else None


    