import threading
import tkinter as tk
from tkinter import ttk, messagebox

from model.credenciais import Credenciais
from model.unidade_alvo import Unidade
from config.driver import criar_driver

from service.automatizacao_plena import automatizar_agendamento
from service.formatador import formatar_resultado


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plena Saúde - Busca de Agendamento")
        self.geometry("720x520")

        # estilo para contornar entries
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Outlined.TEntry", padding=6, relief="solid", borderwidth=1)

        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Matrícula (15 dígitos):").grid(row=0, column=0, sticky="w")
        self.matricula = ttk.Entry(frm, style="Outlined.TEntry")
        self.matricula.grid(row=0, column=1, sticky="we", padx=8, pady=4)

        ttk.Label(frm, text="CPF:").grid(row=1, column=0, sticky="w")
        self.cpf = ttk.Entry(frm, style="Outlined.TEntry")
        self.cpf.grid(row=1, column=1, sticky="we", padx=8, pady=4)

        ttk.Label(frm, text="Especialidade / Médico:").grid(row=2, column=0, sticky="w")
        self.especialidade = ttk.Entry(frm, style="Outlined.TEntry")
        self.especialidade.grid(row=2, column=1, sticky="we", padx=8, pady=4)

        # headless
        self.headless_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frm,
            text="Executar em segundo plano (Headless)",
            variable=self.headless_var
        ).grid(row=3, column=1, sticky="w", padx=8, pady=4)

        # unidades
        ttk.Label(frm, text="Unidades:").grid(row=4, column=0, sticky="nw")
        self.un_mogi = tk.BooleanVar(value=True)
        self.un_aruja = tk.BooleanVar(value=True)

        un_frame = ttk.Frame(frm)
        un_frame.grid(row=4, column=1, sticky="w", padx=8, pady=4)

        ttk.Checkbutton(un_frame, text="Hospital Previna - Mogi das Cruzes", variable=self.un_mogi).pack(anchor="w")
        ttk.Checkbutton(un_frame, text="Plena Saúde - Arujá", variable=self.un_aruja).pack(anchor="w")

        self.btn = ttk.Button(frm, text="Buscar horários", command=self.on_buscar)
        self.btn.grid(row=5, column=1, sticky="w", padx=8, pady=10)

        ttk.Label(frm, text="Resultado:").grid(row=6, column=0, sticky="nw")
        self.saida = tk.Text(frm, height=16, wrap="word")
        self.saida.grid(row=6, column=1, sticky="nsew", padx=8, pady=4)

        frm.columnconfigure(1, weight=1)
        frm.rowconfigure(6, weight=1)

    def escrever_saida(self, texto: str):
        self.saida.delete("1.0", "end")
        self.saida.insert("end", texto)

    def on_buscar(self):
        self.btn.config(state="disabled")
        self.escrever_saida("Executando...")
        threading.Thread(target=self._executar_busca, daemon=True).start()

    def _executar_busca(self):
        try:
            unidades = []
            if self.un_mogi.get():
                unidades.append(Unidade.MOGI)
            if self.un_aruja.get():
                unidades.append(Unidade.ARUJA)

            credenciais = Credenciais(
                numeroMatricula=self.matricula.get().strip(),
                cpf=self.cpf.get().strip(),
                especialidade=self.especialidade.get().strip(),
                unidades=unidades
            )

            driver = criar_driver(headless=self.headless_var.get())
            try:
                resultado = automatizar_agendamento(driver, credenciais)
            finally:
                driver.quit()

            texto = formatar_resultado(resultado)
            self.after(0, lambda: self.escrever_saida(texto))

        except Exception:
            self.after(0, lambda: messagebox.showerror("Erro", "insira credenciais válidas"))
        finally:
            self.after(0, lambda: self.btn.config(state="normal"))