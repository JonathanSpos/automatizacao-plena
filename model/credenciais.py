from dataclasses import dataclass, field
from model.unidade_alvo import Unidade

@dataclass
class Credenciais:
    numeroMatricula: str
    cpf: str
    especialidade: str
    unidades: list[Unidade] = field(default_factory=list)

    def __post_init__(self):
        # matrícula
        if not self.numeroMatricula.isdigit() or len(self.numeroMatricula) != 15:
            raise ValueError("Matrícula inválida")

        # cpf
        cpf_numeros = ''.join(filter(str.isdigit, self.cpf))
        if len(cpf_numeros) != 11:
            raise ValueError("CPF inválido")
        self.cpf = cpf_numeros

        # especialidade
        if not self.especialidade.strip():
            raise ValueError("Especialidade inválida")

        # unidades
        if not self.unidades:
            raise ValueError("Informe ao menos uma unidade")

        for u in self.unidades:
            if not isinstance(u, Unidade):
                raise TypeError("Unidades devem ser do tipo Unidade (Enum)")

    @property
    def numeroMatricula(self) -> str:
        return self._numeroMatricula
    @property
    def cpf(self) -> str:
        return self._cpf
    @property
    def especialidade(self) -> str:
        return self._especialidade

    @numeroMatricula.setter
    def numeroMatricula(self, valor: str):
        self._numeroMatricula = valor
    @cpf.setter
    def cpf(self, valor: str):
        self._cpf = valor
    @especialidade.setter
    def especialidade(self, valor: str):
        self._especialidade = valor