from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def abrir_janela(driver, url: str): 
    driver.get(url)
    driver.maximize_window()

def clicar_nome(driver):
    informacoes = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "frmInicial:nomepacIni")))
    informacoes.click()

def avancar(driver):
    informacoes = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='ui-button-text ui-c' and normalize-space(text())='Avançar']")))
    informacoes.click()

def clicar(driver):
    informacoes = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.TAG_NAME, "li")))
    informacoes.click()

def voltar(driver):
    informacoes = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='frmInicial:j_idt28']")))
    informacoes.click()