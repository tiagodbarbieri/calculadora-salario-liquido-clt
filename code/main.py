from engine import Calculator
from tkinter import Tk
from tkinter import ttk


class MyEntry(ttk.Frame):
    def __init__(self, master, text, type: int | float):
        super().__init__(master=master)
        self.type = type
        self.value: int | float = 0
        self.msg = ""
        self.status = True

        # Label - text
        self.label_text = ttk.Label(master=self, text=text)
        self.label_text.grid(column=0, row=0, sticky="e", padx=5, pady=5)
        # Entry
        self.entry = ttk.Entry(
            master=self, width=10, justify="right", validate="focusout", validatecommand=self.function_select
        )
        self.entry.grid(column=1, row=0)
        # Label - message
        self.label_msg = ttk.Label(master=self, text=self.msg, width=18, foreground="red")
        self.label_msg.grid(column=3, row=0, sticky="w", padx=5, pady=5)

    def function_select(self) -> bool:
        if self.type == int:
            return self.check_int(self.entry.get())
        elif self.type == float:
            return self.check_float(self.entry.get())

    def check_int(self, value: str) -> bool:
        if value == "":
            return self.fill_variables()
        elif value.strip().isnumeric():
            return self.fill_variables(int(value.strip()))
        else:
            return self.fill_variables(msg="<- deve ser inteiro!", status=False)

    def check_float(self, value) -> bool:
        if value == "":
            return self.fill_variables()
        elif value.strip().replace(",", "").replace(".", "").isnumeric():
            return self.fill_variables(float(value.strip().replace(",", ".")))
        else:
            return self.fill_variables(msg="<- número inválido!", status=False)

    def fill_variables(self, value=0, msg="", status=True) -> bool:
        self.value = value
        self.msg = msg
        self.label_msg.configure(text=self.msg)
        self.status = status
        return self.status

    def clear(self):
        self.value = 0
        self.msg = ""
        self.label_msg.configure(text=self.msg)
        self.entry.delete(0, "end")


class Window(Tk):
    def __init__(self):
        # Creating calculator
        self.engine = Calculator()

        # Main Window
        super().__init__()
        self.title("Calculadora salário líquido CLT")

        # Label and Entry 01 - salary [R$]
        self.entry_01 = MyEntry(self, "Salário bruto R$", float)
        self.entry_01.grid(column=0, row=0, sticky="e", columnspan=3)

        # Label and Entry 02 - dependents [qty]
        self.entry_02 = MyEntry(self, "Dependentes", int)
        self.entry_02.grid(column=0, row=1, sticky="e", columnspan=3)

        # Label and Entry 03 - pension percentage [%]
        self.entry_03 = MyEntry(self, "Pensão [%]", float)
        self.entry_03.grid(column=0, row=2, sticky="e", columnspan=3)

        # Label and Entry 04 - other discounts [R$]
        self.entry_04 = MyEntry(self, "Outros descontos R$", float)
        self.entry_04.grid(column=0, row=3, sticky="e", columnspan=3)

        # Button 01 - Save
        self.btn_save = ttk.Button(self, text="Salvar", width=15, command=self.save)
        self.btn_save.grid(column=0, row=4, padx=5, pady=5)

        # Button 02 - Clear
        self.btn_clear = ttk.Button(self, text="Limpar", width=15, command=self.clear)
        self.btn_clear.grid(column=1, row=4, padx=5, pady=5)

        # Button 03 - Calculate
        self.btn_calculate = ttk.Button(self, text="Calcular", width=15, command=self.calculate)
        self.btn_calculate.grid(column=2, row=4, padx=5, pady=5)

        # Loop window
        self.mainloop()

    def save(self):
        pass

    def clear(self):
        self.entry_01.clear()
        self.entry_02.clear()
        self.entry_03.clear()
        self.entry_04.clear()

    def calculate(self):
        if self.validate():
            # Input values
            self.engine.salary = self.entry_01.value
            self.engine.dependents = self.entry_02.value
            self.engine.pension_percentage = self.entry_03.value
            self.engine.other_discounts = self.entry_04.value
            # Start calculation
            self.engine.calculate()
            self.report()

    def validate(self) -> bool:
        status = []
        status.append(self.entry_01.status)
        status.append(self.entry_02.status)
        status.append(self.entry_03.status)
        status.append(self.entry_04.status)
        for valid in status:
            if not valid:
                return False
        return True

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
