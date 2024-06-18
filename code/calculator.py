from tables import INSS, IRPF, DEP


class Calculator:
    def __init__(self, salary=0.0, dependents=0, pension=0.0, other_discounts=0.0):
        # Inputs
        self.salary = salary
        self.dependents = dependents
        self.pension = pension
        self.other_discounts = other_discounts

        # INSS table
        self.inss_data = INSS()
        self.inss_table = self.inss_data.table

        # IRPF table
        self.irpf_data = IRPF()
        self.irpf_table = self.irpf_data.table

        # Dependent value
        self.dep_data = DEP()
        self.dep_value = self.dep_data.value

        # Calculations
        self.inss = self.inss_calculation
        self.irpf = self.irpf_calculation
        self.pension_calculation = 0.0
        self.total_discounts = 0.0
        self.net_salary = salary - self.total_discounts

    def inss_calculation(self):
        inss = 0.0
        for line in self.inss_table:
            if self.salary >= line[0] and self.salary <= line[1]:
                inss += (self.salary - line[0]) * (line[2] / 100)
                return inss
            else:
                inss += (line[1] - line[0]) * (line[2] / 100)
        return inss

    def irpf_calculation(self):
        base_salary = self.salary - self.inss - (self.dependents * self.dep_value) - VPA
        for line in self.irpf_table:
            if base_salary >= line[0] and base_salary <= line[1]:
                IRPF = base_salary * (line[2] / 100) - line[3]
                return IRPF
