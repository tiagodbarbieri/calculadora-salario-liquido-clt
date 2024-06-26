from engine import Calculator
from re import compile
from tkinter import filedialog
from tkinter import Button
from tkinter import Entry
from tkinter import Frame
from tkinter import Label
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import Tk
import platform

# Regular expression for integer numbers
INT_PATTERN = compile(r"^[0-9]+$")

# Regular expression for float numbers
FLOAT_PATTERN = compile(r"^[0-9]*[\.|,]?[0-9]+$")

REPORT_TEXT = """
INSS:...........................R$
IRPF:...........................R$
Pensão alimentícia:...R$
Outros descontos:.....R$
-------------------------------------
Total de descontos:...R$
Salário Líquido:..........R$
"""


class MyButton(Button):
    def __init__(self, master, text=None, width=None, command=None):
        super().__init__(master=master, text=text, width=width, command=command)
        self.bind("<Button-1>", self.focus_in)

    def focus_in(self, event):
        self.focus()


class MyEntry(Frame):
    def __init__(self, master, text, type: int | float):
        super().__init__(master=master)
        self.type = type
        self.value: int | float = 0
        self.msg = ""
        self.status = True

        # Label for text
        self.label_text = Label(master=self, text=text)
        self.label_text.grid(column=0, row=0, sticky="e", padx=5, pady=5)
        # Entry for values
        self.entry = Entry(
            master=self,
            width=10,
            background="white",
            justify="right",
            validate="focusout",
            validatecommand=self.function_select,
        )
        self.entry.grid(column=1, row=0)

    def function_select(self) -> bool:
        if self.type == int:
            return self.check_int(self.entry.get())
        elif self.type == float:
            return self.check_float(self.entry.get())

    def check_int(self, value: str) -> bool:
        if value == "":
            return self.fill_variables()
        elif INT_PATTERN.match(value.strip()):
            return self.fill_variables(int(value.strip()))
        else:
            return self.fill_variables(msg="O número deve ser inteiro!", status=False)

    def check_float(self, value: str) -> bool:
        if value == "":
            return self.fill_variables()
        elif FLOAT_PATTERN.match(value.strip()):
            return self.fill_variables(float(value.strip().replace(",", ".")))
        else:
            return self.fill_variables(msg="Número inválido!", status=False)

    def fill_variables(self, value=0, msg="", status=True) -> bool:
        self.value = value
        self.msg = msg
        self.status = status
        if status:
            self.entry.configure(background="white")
        else:
            self.entry.configure(background="yellow")
        return status

    def clear(self) -> None:
        self.value = 0
        self.msg = ""
        self.status = True
        self.entry.configure(background="white")
        self.entry.delete(0, "end")


class Window(Tk):
    def __init__(self):
        try:
            # Creating calculator
            self.engine = Calculator()
        except Exception:
            messagebox.showerror(
                "ERRO FATAL!", "O website www.gov.br não está acessível, verifique sua internet e reinicie a aplicação!"
            )
        else:
            # Main Window
            super().__init__()
            self.title("Calculadora CLT")
            self.resizable(False, False)

            # Defining windows icon
            if platform.system() == "Windows":
                self.iconbitmap(bitmap="code/images/icon.ico")
            elif platform.system() == "Linux":
                large_icon = PhotoImage(file="code/images/icon_32x32.png")
                small_icon = PhotoImage(file="code/images/icon_16x16.png")
                self.iconphoto(False, large_icon, small_icon)

            # === Entries =============================================================================================
            # Frame for MyEntries
            self.frame_entries = Frame(self)
            self.frame_entries.grid(column=0, row=0, padx=10, pady=5, sticky="e")

            # Label and Entry 01 - salary [R$]
            self.entry_01 = MyEntry(self.frame_entries, "Salário bruto R$", float)
            self.entry_01.grid(column=0, row=0, sticky="e")
            self.entry_01.entry.bind("<FocusOut>", self.update_msg)

            # Label and Entry 02 - dependents [qty]
            self.entry_02 = MyEntry(self.frame_entries, "Dependentes", int)
            self.entry_02.grid(column=0, row=1, sticky="e")
            self.entry_02.entry.bind("<FocusOut>", self.update_msg)

            # Label and Entry 03 - pension percentage [%]
            self.entry_03 = MyEntry(self.frame_entries, "Pensão [%]", float)
            self.entry_03.grid(column=0, row=2, sticky="e")
            self.entry_03.entry.bind("<FocusOut>", self.update_msg)

            # Label and Entry 04 - other discounts [R$]
            self.entry_04 = MyEntry(self.frame_entries, "Outros descontos R$", float)
            self.entry_04.grid(column=0, row=3, sticky="e")
            self.entry_04.entry.bind("<FocusOut>", self.update_msg)

            # === Messages ============================================================================================
            # Label for messages
            self.lbl_msgs = Label(self, justify="center", text="Dados carregados com sucesso!", fg="blue", height=2)
            self.lbl_msgs.grid(column=0, row=1, pady=5, sticky="we")

            # === Report =============================================================================================+
            # Frame for report outside
            self.frame_report_out = Frame(self, border=2, relief="groove")
            self.frame_report_out.grid(column=0, row=2, padx=10, pady=5)

            # Frame for report inside
            self.frame_report_in = Frame(self.frame_report_out)
            self.frame_report_in.grid(column=0, row=0, padx=15, pady=0)

            # Label report left side
            self.lbl_report_01 = Label(self.frame_report_in, text=REPORT_TEXT, justify="left")
            self.lbl_report_01.grid(column=0, row=0, padx=0, pady=0)

            # Label report right side
            self.lbl_report_02 = Label(self.frame_report_in, text=self.report(), justify="right")
            self.lbl_report_02.grid(column=1, row=0, padx=0, pady=0)

            # === Buttons =============================================================================================
            # Frame for buttons
            self.frame_buttons = Frame(self)
            self.frame_buttons.grid(column=0, row=3, padx=10, pady=10)

            # Button 01 - Save
            self.btn_save = MyButton(self.frame_buttons, text="Salvar", command=self.save)
            self.btn_save.grid(column=0, row=0, padx=1, pady=1, sticky="we")

            # Button 02 - Clear
            self.btn_clear = MyButton(self.frame_buttons, text="Limpar", command=self.clear)
            self.btn_clear.grid(column=1, row=0, padx=1, pady=1, sticky="we")

            # Button 03 - Calculate
            self.btn_calculate = MyButton(self.frame_buttons, text="Calcular", command=self.calculate, width=30)
            self.btn_calculate.grid(column=0, row=1, padx=1, pady=1, columnspan=2)

            # Loop window
            self.mainloop()

    def save(self) -> None:
        file_name = filedialog.asksaveasfilename(
            defaultextension=".txt", title="Salvar como", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )
        if file_name:
            report = []
            report.append("+-----------------------------------+\n")
            report.append("|             RELATÓRIO             |\n")
            report.append("+-----------------------------------+\n")
            report.append(f"| Salário bruto........R${self.engine.salary:>10.2f} |\n")
            report.append(f"| INSS.................R${self.engine.inss_value:>10.2f} |\n")
            report.append(f"| IRPF.................R${self.engine.irpf_value:>10.2f} |\n")
            report.append(f"| Pensão alimentícia...R${self.engine.pension_value:>10.2f} |\n")
            report.append(f"| Outros descontos.....R${self.engine.other_discounts:>10.2f} |\n")
            report.append("+-----------------------------------+\n")
            report.append(f"| Total de descontos...R${self.engine.total_discounts:>10.2f} |\n")
            report.append(f"| Salário Liquido......R${self.engine.net_salary:>10.2f} |\n")
            report.append("+-----------------------------------+")
            with open(file_name, "w") as r:
                for line in report:
                    r.write(line)

    def clear(self):
        self.entry_01.clear()
        self.entry_02.clear()
        self.entry_03.clear()
        self.entry_04.clear()
        self.lbl_msgs.configure(text="Dados carregados com sucesso!", foreground="blue")
        self.calculate()

    def calculate(self) -> None:
        if self.validate():
            # Input values
            self.engine.salary = self.entry_01.value
            self.engine.dependents = self.entry_02.value
            self.engine.pension_percentage = self.entry_03.value
            self.engine.other_discounts = self.entry_04.value
            # Start calculation
            self.engine.calculate()
            self.lbl_report_02.configure(text=self.report())

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

    def report(self) -> str:
        # fmt: off
        t1 = (f"{self.engine.inss_value:.2f}\n")
        t2 = (f"{self.engine.irpf_value:.2f}\n")
        t3 = (f"{self.engine.pension_value:.2f}\n")
        t4 = (f"{self.engine.other_discounts:.2f}\n")
        t5 = (("-" * 15) + "\n")
        t6 = (f"{self.engine.total_discounts:.2f}\n")
        t7 = (f"{self.engine.net_salary:.2f}")
        # fmt: on
        return t1 + t2 + t3 + t4 + t5 + t6 + t7

    def update_msg(self, event) -> None:
        data = []
        data.append((self.entry_01.status, self.entry_01.msg))
        data.append((self.entry_02.status, self.entry_02.msg))
        data.append((self.entry_03.status, self.entry_03.msg))
        data.append((self.entry_04.status, self.entry_04.msg))
        for info in data:
            if not info[0]:
                self.lbl_msgs.configure(text=info[1], foreground="red")
                break
            else:
                self.lbl_msgs.configure(text="Dados carregados com sucesso!", foreground="blue")


if __name__ == "__main__":
    app = Window()
