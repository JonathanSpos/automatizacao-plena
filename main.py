from automatizacao_plena import automatizar_agendamento,formatar_resultado
from time import sleep
from config import UNIDADES_ALVO, separar

def main():
    sleep(2)
    separar()
    matricula = input("Matrícula (15 dígitos): ").strip()
    cpf = input("CPF (11 dígitos): ").strip()
    medico = input("Doutor/Especialidade: ").strip()

    unidades_alvo = UNIDADES_ALVO
    try:
        resultado = automatizar_agendamento(matricula, cpf, medico, unidades_alvo)
        mensagem = formatar_resultado(resultado)
        print(mensagem)
    finally:
        pass

if __name__ == "__main__":
    main()