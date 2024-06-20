from engine import Calculator
from tkinter import Tk
from tkinter import ttk


class Window(Tk):
    def __init__(self):
        # Creating calculator
        self.engine = Calculator()

        # Main Window
        super().__init__()
        self.title("Calculadora salário líquido CLT")

        # Label and Entry 01 - salary [R$]
        self.lbl_01 = ttk.Label(self, text="Salário bruto R$")
        self.lbl_01.grid(column=0, row=0, sticky="e", padx=5, pady=5)
        self.entry_01 = ttk.Entry(self, width=10)
        self.entry_01.grid(column=1, row=0)

        # Label and Entry 02 - dependents [qty]
        self.lbl_02 = ttk.Label(self, text="Dependentes")
        self.lbl_02.grid(column=0, row=1, sticky="e", padx=5, pady=5)
        self.entry_02 = ttk.Entry(
            self, width=10, validate="focusout", validatecommand=lambda: self.check_int(self.entry_02.get())
        )
        self.entry_02.grid(column=1, row=1)

        # Label and Entry 03 - pension percentage [%]
        self.lbl_03 = ttk.Label(self, text="Pensão [%]")
        self.lbl_03.grid(column=0, row=2, sticky="e", padx=5, pady=5)
        self.entry_03 = ttk.Entry(self, width=10)
        self.entry_03.grid(column=1, row=2)

        # Label and Entry 04 - other discounts [R$]
        self.lbl_04 = ttk.Label(self, text="Outros descontos R$")
        self.lbl_04.grid(column=0, row=3, sticky="e", padx=5, pady=5)
        self.entry_04 = ttk.Entry(
            self, width=10, validate="focusout", validatecommand=lambda: self.check_float(self.entry_04.get())
        )
        self.entry_04.grid(column=1, row=3)

        # Button 01 - Clear
        self.btn_clear = ttk.Button(self, text="Limpar", width=15, command=self.clear)
        self.btn_clear.grid(column=3, row=0, padx=5, pady=5, rowspan=2)

        # Button 02 - Calculate
        self.btn_calculate = ttk.Button(self, text="Calcular", width=15, command=self.calculate)
        self.btn_calculate.grid(column=3, row=2, padx=5, pady=5, rowspan=2)

        # Loop window
        self.mainloop()

    def check_int(self, value: str) -> bool:
        if value.strip().isnumeric():
            print("SIM")
            return True
        else:
            print("NÃO")
            return False
        # return True if value.strip().isnumeric() else False

    def check_float(self, value: str) -> bool:
        if value.strip().replace(",", "").replace(".", "").isnumeric():
            print("SIM")
            return True
        else:
            print("NÃO")
            return False

    def clear(self):
        pass

    def calculate(self):
        # self.engine.salary = self.verify(self.entry_01.get(), float)
        # self.engine.dependents = self.verify(self.entry_02.get(), int)
        # self.engine.pension_percentage = self.verify(self.entry_03.get(), float)
        # self.engine.other_discounts = self.verify(self.entry_04.get(), float)
        self.engine.calculate()
        self.report()

    """
    def verify(self, value: str, object_type: type):
        if value == "":
            return object_type(0)
        else:
            v = value.replace(",", "")
            v = v.replace(".", "")
            if v.isnumeric():
                return object_type(value.replace(",", "."))
            else:
                return object_type(0)
    """

    def report(self):
        print("=" * 50)
        print(f"\nSalário bruto: R${self.engine.salary:.2f}")
        print(f"INSS: R${self.engine.inss_value:.2f}")
        print(f"IRPF: R${self.engine.irpf_value:.2f}")
        print(f"Pensão alimentícia: R${self.engine.pension_value:.2f}")
        print(f"Outros descontos: R${self.engine.other_discounts:.2f}")
        print(f"Total de descontos: R${self.engine.total_discounts:.2f}")
        print(f"Salário Líquido: R${self.engine.net_salary:.2f}\n")
        print("=" * 50)


if __name__ == "__main__":
    app = Window()
