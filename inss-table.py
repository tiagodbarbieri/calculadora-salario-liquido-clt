from html.parser import HTMLParser
from urllib.request import urlopen

# INSS table from website: www.gov.br
INSS_SOURCE = "https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal"


class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.table = False
        self.row = False
        self.cell = False
        self.all_tables = []
        self.this_table = []
        self.table_row = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.table = True
        elif tag == "tr":
            self.row = True
        elif tag == "td":
            self.cell = True

    def handle_endtag(self, tag):
        if tag == "table":
            self.table = False
            self.all_tables.append(self.this_table)
            self.this_table = []
        elif tag == "tr":
            self.row = False
            self.this_table.append(self.table_row)
            self.table_row = []
        elif tag == "td":
            self.cell = False

    def handle_data(self, data):
        if self.table and self.row and self.cell:
            self.table_row.append(data)

    def __str__(self):
        for table in self.all_tables:
            for row in table:
                print(row)
            print("")
        return ""


class INSS:
    def __init__(self) -> None:
        self.html = self.get_source(INSS_SOURCE)
        self.parser = TableParser()
        self.parser.feed(self.html)
        self.table = self.extract_data(self.parser.all_tables[0])

    def get_source(self, url):
        response = urlopen(url)
        html = response.read()
        return html.decode("utf-8")

    def extract_data(self, table):
        tb = []
        for row in range(1, len(table)):
            rw = []
            if row == 1:
                rw.append(0.0)
                self.get_elements(table[row], rw)
                tb.append(rw)
            else:
                self.get_elements(table[row], rw)
                tb.append(rw)
        return tb

    def get_elements(self, row, elements_list: list):
        for cell in row:
            s = str(cell)
            s = s.strip()
            s = s.replace(".", "")
            s = s.replace(",", ".")
            s = s.replace("%", "")
            s = s.replace(" ", "-")
            sl = s.split("-")
            for element in sl:
                e = element.replace(".", "")
                if e.isnumeric():
                    elements_list.append(float(element))


if __name__ == "__main__":
    inss_table = INSS()
    print(inss_table.table)
