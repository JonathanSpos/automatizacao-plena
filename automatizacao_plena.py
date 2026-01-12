from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from config import separar
import time
import re

options = webdriver.EdgeOptions()
options.add_argument("--headless=new")

navegador = webdriver.Edge(options=options)

def pausa(tempo: int):
    time.sleep(tempo)

def abrir_janela(url: str): 
    navegador.get(url)
    navegador.maximize_window()
        
def preencher_matricula(matricula: str):    
    if len(matricula) != 15:
        raise ValueError("Digite uma matrícula válida")
    if not matricula.isdigit():
        raise TypeError("Somente números são aceitos")
    else:
        informacoes = navegador.find_element(By.ID, "frmInicial:MatrIni")
        informacoes.click()
        informacoes.send_keys(matricula)
        pausa(1)

def clicar_nome():
    informacoes = navegador.find_element(By.ID, "frmInicial:nomepacIni")
    informacoes.click()
    pausa(1)

def preencher_cpf(cpf: str):  
    if len(cpf) != 11:
        raise ValueError("Coloque um cpf válido.")
    if not cpf.isdigit():
        raise TypeError("Somente números são aceitos.")
    else:
        informacoes = navegador.find_element(By.ID, "frmInicial:cpfIni")
        informacoes.click()
        informacoes.send_keys(cpf)
        pausa(1)
  
def preencher_email(email: str):
    informacoes = navegador.find_element(By.ID, "frmInicial:emailIni")
    informacoes.send_keys(email)
    pausa(1)

def preencher_telefone(telefone: str):
    if len(telefone) != 11:
        raise ValueError("Digite um telefone válido")
    if not telefone.isdigit():
        raise TypeError("Somente números são aceitos")
    else:
        informacoes = navegador.find_element(By.ID, "frmInicial:celularIni")
        informacoes.send_keys(telefone)
        pausa(1)

def avancar():
    informacoes = navegador.find_element(By.XPATH, "//span[@class='ui-button-text ui-c' and normalize-space(text())='Avançar']")
    informacoes.click()
    pausa(1)


def procurar_por_doutor_especialidade(nome: str):
    informacoes = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.ID, "frmInicial:group_input")))
    informacoes.send_keys(nome.upper())
    pausa(1)


def clicar():
    informacoes = WebDriverWait(navegador, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "li")))
    informacoes.click()
    pausa(1)

def obter_periodo_agenda_preenchida() -> tuple[str, str] | None:
    try:
        WebDriverWait(navegador, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[contains(normalize-space(.), 'Agendamentos no período de:')]")
            )
        )
    except TimeoutException:
        return None

    
    spans = navegador.find_elements(By.XPATH, "//span[contains(@style,'color:red')]")
    datas = [s.text.strip() for s in spans if re.fullmatch(r"\d{2}/\d{2}/\d{4}", s.text.strip())]

    if len(datas) >= 2:
        return datas[0], datas[1]

    return None

def avancar_e_identificar_tela() -> str:
    avancar()

    try:
        WebDriverWait(navegador, 15).until(lambda d:
            d.find_elements(By.XPATH, "//td[@role='gridcell']") or
            d.find_elements(By.XPATH, "//span[contains(normalize-space(.), 'Agendamentos no período de:')]")
        )
    except TimeoutException:
        return "desconhecido"

    if navegador.find_elements(By.XPATH, "//td[@role='gridcell']"):
        return "unidades"

    if navegador.find_elements(By.XPATH, "//span[contains(normalize-space(.), 'Agendamentos no período de:')]"):
        return "preenchido"

    return "desconhecido"

def dias_por_unidade_na_tela_unidades(unidades: list[str]) -> dict:
    soup = BeautifulSoup(navegador.page_source, "html.parser")

    resultado = {u: [] for u in unidades}

    for td in soup.select("td[role='gridcell']"):
        span_dia = td.select_one("span[style*='font-size:18px']")
        if not span_dia:
            continue

        dia_txt = span_dia.get_text(strip=True)

        for unidade in unidades:
            if td.find("span", string=lambda t, u=unidade: t and u in t):
                if dia_txt not in resultado[unidade]:
                    resultado[unidade].append(dia_txt)

    return {u: dias for u, dias in resultado.items() if dias}

def automatizar_agendamento(matricula: str, cpf: str, medico: str, unidades_alvo: list):
    abrir_janela("https://plenaconsultas.com.br/Agenda/")
    
    preencher_matricula(matricula)
    clicar_nome()
    
    preencher_cpf(cpf)
    avancar()
    
    procurar_por_doutor_especialidade(medico)
    clicar()
    
    tela = avancar_e_identificar_tela()

    if tela == "unidades":
        dias_por_unidade = dias_por_unidade_na_tela_unidades(unidades_alvo)
        separar()
        return {
            "status": "unidades",
            "unidades": dias_por_unidade
        }

    if tela == "preenchido":
        periodo = obter_periodo_agenda_preenchida()
        separar()
        return {
            "status": "preenchido",
            "periodo": {
                "de": periodo[0] if periodo else None,
                "ate": periodo[1] if periodo else None
            },
            "mensagem": "Agendamentos preenchidos em todas as unidades"
        }

    return {
        "status": "erro",
        "mensagem": "Não consegui identificar a tela após avançar"
    }

def formatar_resultado(resultado: dict) -> str:
    if resultado["status"] == "unidades":
        unidades = resultado.get("unidades", {})
        if not unidades:
            return "Nenhuma unidade encontrada com dias disponíveis."

        blocos = []
        for unidade, dias in unidades.items():
            bloco = [f"{unidade}"]
            for d in dias:
                bloco.append(f"  - {d}")
            blocos.append("\n".join(bloco))

        return "Dias disponíveis:\n\n" + "\n\n".join(blocos)

    if resultado["status"] == "preenchido":
        de = resultado["periodo"].get("de")
        ate = resultado["periodo"].get("ate")
        return f"Agendamentos preenchidos no período de {de} até {ate}."

    return f"{resultado.get('mensagem', 'Erro desconhecido')}"
