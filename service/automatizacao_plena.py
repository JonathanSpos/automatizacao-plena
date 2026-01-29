from service.preencher_matricula import preencher_credenciais
from service.navegacao import abrir_janela
from service.telas import identificar_tela, obter_periodo_agenda_preenchida
from service.horarios import obter_todos_horarios_unidades_marcadas
from model.credenciais import Credenciais

def automatizar_agendamento(driver, credenciais: Credenciais) -> dict:
    try:  
        abrir_janela(driver, "https://plenaconsultas.com.br/Agenda/")

        preencher_credenciais(driver, credenciais)  
        tela = identificar_tela(driver)

        if tela == "unidades":
            unidades_texto = [unidade.value for unidade in credenciais.unidades]
            horario_agendamento = obter_todos_horarios_unidades_marcadas(driver, unidades_texto)
            return {"status": "unidades", "horarios": horario_agendamento}

        if tela == "preenchido":
            periodo = obter_periodo_agenda_preenchida(driver)
            return {
                "status": "preenchido",
                "periodo": {"de": periodo[0] if periodo else None, "ate": periodo[1] if periodo else None},
                "mensagem": "Agendamentos preenchidos em todas as unidades"
            }

        return {"status": "erro", "mensagem": "Não consegui identificar a tela após avançar"}

    except Exception:
        return {"status": "erro", "mensagem": "Erro na automação, especialidade/doutor não encontrado, verifique se as credenciais estão corretas"}