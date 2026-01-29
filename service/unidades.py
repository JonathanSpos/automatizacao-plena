from bs4 import BeautifulSoup


def dias_por_unidade_na_tela_unidades(driver, unidades: list[str]) -> dict:
    soup = BeautifulSoup(driver.page_source, "html.parser")
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