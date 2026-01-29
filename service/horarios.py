from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from service.navegacao import voltar
import re

HORA_RE = re.compile(r"^\d{2}:\d{2}$") # exemplo: 12:00
DATA_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}") # exemplo: 2026-02-05

def voltar_e_esperar_unidades(driver, timeout: int = 15):
    voltar(driver)
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, "//td[@role='gridcell']")))
    
def existe_horario(driver) -> bool:
    spans = driver.find_elements(By.CSS_SELECTOR, "span.ui-button-text.ui-c")
    for span in spans:
        texto = (span.text or "").strip()
        if HORA_RE.fullmatch(texto):
            return True
    return False

def obter_todos_horarios(driver, timeout: int = 20 ) -> list[str]:
    aguardar = WebDriverWait(driver, timeout)

    try:
        aguardar.until(existe_horario)
    except TimeoutException:
        return []

    # adiciona todos os horários dsponíveis em uma lista
    horarios = []
    spans = driver.find_elements(By.CSS_SELECTOR, "span.ui-button-text.ui-c")
    for span in spans:
        texto = (span.text or "").strip()
        if HORA_RE.fullmatch(texto):
            horarios.append(texto)
    
    # remove duplicados
    remover_duplicados = set()
    unicos = []
    for hora in horarios:
        if hora not in remover_duplicados:
            remover_duplicados.add(hora)
            unicos.append(hora)
    
    return unicos

def coletar_cliques_unidades(driver, unidades_marcadas: list[str]) -> list[dict]:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cliques: list[dict] = []

    for gridcell in soup.select("td[role='gridcell']"):
        span_dia = gridcell.select_one("span[style*='font-size:18px']")
        if not span_dia:
            continue
        
        dia_texto = span_dia.get_text(strip=True)

        # para cada link clicável (cada unidade desse dia)
        for link in gridcell.select("a[onclick*='wr(']"):
            ao_clicar = link.get("onclick", "")
            match_data = DATA_ISO_RE.search(ao_clicar)
            if not match_data:
                continue

            link_id = link.get("id")
            if not link_id:
                continue

            # pega o "card" da unidade correspondente a esse link
            card_unidade = link.find_parent("div", class_="ui-panelgrid")
            if not card_unidade:
                continue

            # dentro do card, pega o span azul com o nome da unidade
            span_nome = card_unidade.select_one("span[style*='font-size:16px'][style*='color:blue']")
            if not span_nome:
                continue

            nome_unidade = span_nome.get_text(strip=True)

            # filtra só unidades marcadas
            if nome_unidade not in unidades_marcadas:
                continue

            cliques.append({
                "dia_texto": dia_texto,
                "nome_unidade": nome_unidade,
                "link_id": link_id
            })

    # remove duplicados por (unidade, data)
    vistos = set()
    resultado = []
    for item in cliques:
        chave = (item["nome_unidade"], item["dia_texto"])
        if chave not in vistos:
            vistos.add(chave)
            resultado.append(item)

    return resultado


def obter_todos_horarios_unidades_marcadas(driver, unidades_marcadas: list[str], timeout_click = 15, timeout_horario = 15) -> dict:
    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.XPATH, "//td[@role='gridcell']"))
        )
    
    tasks = coletar_cliques_unidades(driver, unidades_marcadas)

    output: dict[str, list[dict]] = {unidade: [] for unidade in unidades_marcadas}

    for task in tasks:
        WebDriverWait(driver, timeout_click).until(
            EC.element_to_be_clickable((By.ID, task["link_id"]))
        ).click()

        horarios = obter_todos_horarios(driver, timeout=timeout_horario)

        chave_unidade = None
        for unidade_marcada in unidades_marcadas:
            if unidade_marcada in task["nome_unidade"]:
                chave_unidade = unidade_marcada
                break
        if chave_unidade is None:
            chave_unidade = task["nome_unidade"]

        output.setdefault(chave_unidade, []).append({
            "dia": task["dia_texto"],
            "horarios": horarios
        })

        voltar_e_esperar_unidades(driver, timeout=25)
    
    return {chave: valor for chave, valor in output.items() if valor}