from model.credenciais import Credenciais
from service.utils import pausa
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from service.navegacao import clicar_nome, avancar, clicar


def preencher_credenciais(driver, credenciais: Credenciais):
    
    pausa(1)
    campo_matricula = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "frmInicial:MatrIni")))
    pausa(2)
    campo_matricula.send_keys(credenciais.numeroMatricula)
    
    pausa(2)
    clicar_nome(driver)

    pausa(1)
    campo_cpf = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "frmInicial:cpfIni")))
    pausa(2)
    campo_cpf.send_keys(credenciais.cpf)

    avancar(driver)

    pausa(1)
    campo_especialidade = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "frmInicial:group_input")))
    pausa(2)
    campo_especialidade.send_keys(credenciais.especialidade.upper())
   
    clicar(driver)

    