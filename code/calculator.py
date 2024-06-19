from tables import INSS, IRPF, DEP


class Calculator:
    def __init__(self, salary=0.0, dependents=0, pension=0.0, other_discounts=0.0):
        # Inputs
        self.salary = salary
        self.dependents = dependents
        self.pension = pension
        self.other_discounts = other_discounts

        # Get INSS table from web
        self.inss_data = INSS()
        self.inss_table = self.inss_data.table

        # Get IRPF table from web
        self.irpf_data = IRPF()
        self.irpf_table = self.irpf_data.table

        # Get Dependent value from web
        self.dep_data = DEP()
        self.dep_value = self.dep_data.value

        # Calculations
        self.calculate()

    def calculate(self):
        self.pension_value = 0.0
        self.irpf = 0.0
        self.inss = self.inss_calculation()
        self.loop_calculation()
        self.total_discounts = self.inss + self.irpf + self.pension_value + self.other_discounts
        self.net_salary = self.salary - self.total_discounts

    def inss_calculation(self):
        inss = 0.0
        for line in self.inss_table:
            if self.salary >= line[0] and self.salary <= line[1]:
                inss += (self.salary - line[0]) * (line[2] / 100)
                return inss
            else:
                inss += (line[1] - line[0]) * (line[2] / 100)
        return inss

    def loop_calculation(self):
        for v in range(0, 10):
            irpf = self.irpf_calculation()
            self.irpf = irpf
            self.net_salary = self.salary - self.inss - irpf
            self.pension_value = self.net_salary * (self.pension / 100)

    def irpf_calculation(self):
        base_salary = self.salary - self.inss - (self.dependents * self.dep_value) - self.pension_value
        for line in self.irpf_table:
            if base_salary >= line[0] and base_salary <= line[1]:
                irpf = base_salary * (line[2] / 100) - line[3]
                return irpf


if __name__ == "__main__":
    c = Calculator(5300, 1, 25, 300)

    print("=" * 50)
    print(f"\nSalário bruto: R${c.salary:.2f}")
    print(f"INSS: R${c.inss:.2f}")
    print(f"IRPF: R${c.irpf:.2f}")
    print(f"Pensão alimentícia: R${c.pension_value:.2f}")
    print(f"Outros descontos: R${c.other_discounts:.2f}")
    print(f"Total de descontos: R${c.total_discounts:.2f}")
    print(f"Salário Líquido: R${c.net_salary:.2f}\n")
    print("=" * 50)

    c.salary = 3500
    c.dependents = 0
    c.pension = 20
    c.other_discounts = 150
    c.calculate()

    print("=" * 50)
    print(f"\nSalário bruto: R${c.salary:.2f}")
    print(f"INSS: R${c.inss:.2f}")
    print(f"IRPF: R${c.irpf:.2f}")
    print(f"Pensão alimentícia: R${c.pension_value:.2f}")
    print(f"Outros descontos: R${c.other_discounts:.2f}")
    print(f"Total de descontos: R${c.total_discounts:.2f}")
    print(f"Salário Líquido: R${c.net_salary:.2f}\n")
    print("=" * 50)
