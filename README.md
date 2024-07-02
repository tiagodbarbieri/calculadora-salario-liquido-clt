# <img src="./code/images/icon_32x32.png" title="icon 32x32" alt="icon 32x32" style="zoom:200%;"> Calculadora Salário Líquido CLT

Simples calculadora para cálculo do salário líquido para trabalhadores em regime CLT.
Os valores para cálculo  de *[IRPF](https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda/tabelas/2024)* e *[INSS](https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal)* são capturados **diretamente** do site do governo: *[www.gov.br](https://www.gov.br/pt-br)*.

 ---

## Funcionamento

1. Inserir dados do trabalhador e clicar em calcular.
   
   <img src="./code/images/image_01.png" title="type data" alt="image 01" style="zoom:60%;">

2. A calculadora possui um sistema de validação de dados. Caso o usuário tenha escrito algo **errado** será avisado disso.
   
   <img src="./code/images/image_02.png" title="type validation" alt="image 02" style="zoom:60%;">

3. Caso o usuário quiser, é possível gerar um relatório em formato .txt clicando em salvar.
   <img src="./code/images/image_03.png" title="report" alt="image 03" style="zoom:60%;"> 

---

## Aparência do aplicativo no Windows

<img src="./code/images/image_04.png" title="appearance on Windows" alt="image 04" style="zoom:50%;">

---

### Para criar um executável com pyinstaller:

No Windows:

```pyinstaller --onefile --windowed --icon=".\code\images\icon.ico" --add-data ".\code\images;images" ".\code\main.py"```

No Linux:

```pyinstaller --onefile --windowed --icon="./code/images/icon_32x32.png" --add-data "./code/images:images" "./code/main.py"```

---

<img src="./code/images/icon_16x16.png" title="icon 16x16" alt="icon 16x16" style="zoom:150%;"> *This icon was made by Uniconlabs from www.flaticon.com*
