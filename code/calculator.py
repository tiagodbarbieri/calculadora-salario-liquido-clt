from tables import INSS, IRPF, DEP


class Calculator:
    def __init__(self, salary=0.0, dependents=0, pension_percentage=0.0, other_discounts=0.0):
        # Inputs
        self.salary = salary
        self.dependents = dependents
        self.pension_percentage = pension_percentage
        self.other_discounts = other_discounts

        # Get INSS table from web
        self.inss_data = INSS()
        self.inss_table = self.inss_data.table

        # Get IRPF table from web
        self.irpf_data = IRPF()
        self.irpf_table = self.irpf_data.table

        # Get Dependent value from web
        self.dependent_data = DEP()
        self.dependent_value = self.dependent_data.value

        # Calculations
        self.calculate()

    def calculate(self):
        # Initializing variables
        self.pension_value = 0.0
        self.irpf_value = 0.0
        self.inss_value = self.inss_calculation()

        # Initializing loop calculation
        self.loop_calculation()

        # Initializing others variables
        self.total_discounts = self.inss_value + self.irpf_value + self.pension_value + self.other_discounts
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
            parcial_net_salary = self.salary - self.inss_value - irpf
            self.pension_value = parcial_net_salary * (self.pension_percentage / 100)
            self.irpf_value = irpf

    def irpf_calculation(self):
        base_salary = self.salary - self.inss_value - (self.dependents * self.dependent_value) - self.pension_value
        for line in self.irpf_table:
            if base_salary >= line[0] and base_salary <= line[1]:
                irpf = base_salary * (line[2] / 100) - line[3]
                return irpf


if __name__ == "__main__":
    c = Calculator(5300, 1, 25, 300)

    print("=" * 50)
    print(f"\nSalário bruto: R${c.salary:.2f}")
    print(f"INSS: R${c.inss_value:.2f}")
    print(f"IRPF: R${c.irpf_value:.2f}")
    print(f"Pensão alimentícia: R${c.pension_value:.2f}")
    print(f"Outros descontos: R${c.other_discounts:.2f}")
    print(f"Total de descontos: R${c.total_discounts:.2f}")
    print(f"Salário Líquido: R${c.net_salary:.2f}\n")
    print("=" * 50)

    c.salary = 3500
    c.dependents = 0
    c.pension_percentage = 20
    c.other_discounts = 150
    c.calculate()

    print("=" * 50)
    print(f"\nSalário bruto: R${c.salary:.2f}")
    print(f"INSS: R${c.inss_value:.2f}")
    print(f"IRPF: R${c.irpf_value:.2f}")
    print(f"Pensão alimentícia: R${c.pension_value:.2f}")
    print(f"Outros descontos: R${c.other_discounts:.2f}")
    print(f"Total de descontos: R${c.total_discounts:.2f}")
    print(f"Salário Líquido: R${c.net_salary:.2f}\n")
    print("=" * 50)
