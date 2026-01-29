from service.preencher_matricula import preencher_credenciais
from service.navegacao import abrir_janela
from model.credenciais import Credenciais
from model.unidade_alvo import Unidade

def teste_preencher_matricula():
    abrir_janela("https://plenaconsultas.com.br/Agenda/")
    
    credenciais = Credenciais(
        numeroMatricula="015390329121000",
        cpf="50273008838",
        especialidade="cardiologia".upper(),
        unidades=[Unidade.MOGI]
    )

    preencher_credenciais(credenciais)

if __name__ == "__main__":
    teste_preencher_matricula()

