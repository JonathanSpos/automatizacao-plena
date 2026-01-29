def formatar_resultado(resultado: dict) -> str:
    status = resultado.get("status")

    if status == "unidades":
        dados = resultado.get("horarios", {})
        if not dados:
            return "Nenhum horário disponível nas unidades selecionadas."

        blocos = []
        for unidade, itens in dados.items():
            linhas = [unidade]
            for item in itens:
                dia = item.get("dia", "Dia não informado")
                horarios = item.get("horarios", [])
                if horarios:
                    linhas.append(f"  - {dia}: {', '.join(horarios)}")
                else:
                    linhas.append(f"  - {dia}: sem horários disponíveis")
            blocos.append("\n".join(linhas))

        return "Horários disponíveis:\n\n" + "\n\n".join(blocos)

    if status == "preenchido":
        periodo = resultado.get("periodo", {})
        de = periodo.get("de")
        ate = periodo.get("ate")
        if de and ate:
            return f"Agendamentos preenchidos no período de {de} até {ate}."
        return "Agendamentos preenchidos em todas as unidades."

    return resultado.get("mensagem", "Erro desconhecido")
