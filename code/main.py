from tables import INSS, IRPF, DEP


def CALCULO_INSS(DADOS_INSS, SB):
    inss = 0.0
    for line in DADOS_INSS:
        if SB >= line[0] and SB <= line[1]:
            inss += (SB - line[0]) * (line[2] / 100)
            return inss
        else:
            inss += (line[1] - line[0]) * (line[2] / 100)
    return inss


def CALCULO_IRPF(DADOS_IRPF, SB, inss, DP, DEP, VPA):
    # Cálculo Salário Base IRPF
    SBA_IRPF = SB - inss - (DP * DEP) - VPA
    for line in DADOS_IRPF:
        if SBA_IRPF >= line[0] and SBA_IRPF <= line[1]:
            IRPF = SBA_IRPF * (line[2] / 100) - line[3]
            return IRPF


INSS_table = INSS()
DADOS_INSS = INSS_table.table

IRPF_table = IRPF()
DADOS_IRPF = IRPF_table.table

dependent = DEP()
DEP = dependent.value

SB = float(input("Digite o seu salário bruto: R$"))
DP = int(input("Quantos dependentes? "))
PA = float(input("Porcentagem pensão alimentícia [%]: "))
OD = float(input("Outros descontos: R$"))

# Calculo do o INSS
inss = CALCULO_INSS(DADOS_INSS, SB)

# Cálculo Pensão Alimentícia
VPA = 0.0
IRPF = 0.0
for value in range(0, 10):
    # Calculo do IRPF
    IRPF = CALCULO_IRPF(DADOS_IRPF, SB, inss, DP, DEP, VPA)
    # Salário Líquido Parcial
    SLP = SB - inss - IRPF
    # Valor pensão alimentícia
    VPA = SLP * (PA / 100)

# Total de descontos
TD = inss + IRPF + VPA + OD

# Cálculo Salário Líquido
SL = SB - TD

print(f"\nSalário bruto: R${SB:.2f}")
print(f"INSS: R${inss:.2f}")
print(f"IRPF: R${IRPF:.2f}")
print(f"Pensão alimentícia: R${VPA:.2f}")
print(f"Outros descontos: R${OD:.2f}")
print(f"Total de descontos: R${TD:.2f}")
print(f"\nSalário Líquido: R${SL:.2f}")
