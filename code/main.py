import math


def CALCULO_INSS(DADOS_INSS, SB):
    INSS = 0.0
    for line in DADOS_INSS:
        if SB >= line[0] and SB <= line[1]:
            INSS += (SB - line[0]) * (line[2] / 100)
            return INSS
        else:
            INSS += (line[1] - line[0]) * (line[2] / 100)
    return INSS


def CALCULO_IRPF(DADOS_IRPF, SB, INSS, DP, DEP, VPA):
    # Cálculo Salário Base IRPF
    SBA_IRPF = SB - INSS - (DP * DEP) - VPA
    for line in DADOS_IRPF:
        if SBA_IRPF >= line[0] and SBA_IRPF <= line[1]:
            IRPF = SBA_IRPF * (line[2] / 100) - line[3]
            return IRPF


# fmt:off
DADOS_INSS = [(0.0, 1320.0, 7.5),
              (1319.99, 2571.29, 9.0),
              (2571.28, 3856.94, 12.0),
              (3856.93, 7507.49, 14.0)]

DADOS_IRPF = [(0.0, 2112.0, 0.0, 0.0),
              (2112.01, 2826.65, 7.5, 158.4),
              (2826.66, 3751.05, 15, 370.4),
              (3751.06, 4664.68, 22.5, 651.73),
              (4665.68, math.inf, 27.5, 884.96)]
# fmt:on

DEP = 189.59

SB = float(input("Digite o seu salário bruto: R$"))
DP = int(input("Quantos dependentes? "))
PA = float(input("Porcentagem pensão alimentícia [%]: "))
OD = float(input("Outros descontos: R$"))

# Calculo do o INSS
INSS = CALCULO_INSS(DADOS_INSS, SB)

# Cálculo Pensão Alimentícia
VPA = 0.0
IRPF = 0.0
for value in range(0, 10):
    # Calculo do IRPF
    IRPF = CALCULO_IRPF(DADOS_IRPF, SB, INSS, DP, DEP, VPA)
    # Salário Líquido Parcial
    SLP = SB - INSS - IRPF
    # Valor pensão alimentícia
    VPA = SLP * (PA / 100)

# Total de descontos
TD = INSS + IRPF + VPA + OD

# Cálculo Salário Líquido
SL = SB - TD

print(f"\nSalário bruto: R${SB:.2f}")
print(f"INSS: R${INSS:.2f}")
print(f"IRPF: R${IRPF:.2f}")
print(f"Pensão alimentícia: R${VPA:.2f}")
print(f"Outros descontos: R${OD:.2f}")
print(f"Total de descontos: R${TD:.2f}")
print(f"\nSalário Líquido: R${SL:.2f}")
