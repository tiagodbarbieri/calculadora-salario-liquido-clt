from tables import INSS, IRPF, DEP


class Calculator:
    def __init__(self):
        # INSS table
        self.inss_data = INSS()
        self.inss_table = self.inss_data.table

        # IRPF table
        self.irpf_data = IRPF()
        self.irpf_table = self.irpf_data.table

        # Dependent value
        self.dep_data = DEP()
        self.dep_value = self.dep_data.value
