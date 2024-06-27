from math import inf
from datetime import datetime
from html.parser import HTMLParser
from urllib.request import urlopen

# Get the current year
year = str(datetime.today().year)

# INSS and IRPF tables from website: www.gov.br
INSS_SOURCE = "https://www.gov.br/inss/pt-br/direitos-e-deveres/inscricao-e-contribuicao/tabela-de-contribuicao-mensal"
IRPF_SOURCE = "https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda/tabelas/" + year


class TableParser(HTMLParser):
    """Extract tables from a web page."""

    def __init__(self) -> None:
        """Initialize this class."""

        super().__init__()
        self.table = False
        self.row = False
        self.cell = False
        self.all_tables = []
        self.this_table = []
        self.table_row = []

    def handle_starttag(self, tag: str, attrs) -> None:
        """Verify if the parser is at the beginning of the tags."""

        if tag == "table":
            self.table = True
        elif tag == "tr":
            self.row = True
        elif tag == "td":
            self.cell = True

    def handle_endtag(self, tag: str) -> None:
        """Verify if the parser is at the end of the tags, and append data that was found."""

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

    def handle_data(self, data: str) -> None:
        """Get the data inside the 'cells'."""

        if self.table and self.row and self.cell:
            self.table_row.append(data)

    def __str__(self) -> str:
        for table in self.all_tables:
            for row in table:
                print(row)
            print("")
        return ""


class DepParser(HTMLParser):
    """Extract dependent value from a web page."""

    def __init__(self) -> None:
        """Initialize this class."""

        super().__init__()
        self.dep = False
        self.value = 0.0

    def handle_starttag(self, tag: str, attrs) -> None:
        """Verify if the parser is at the beginning of the tag 'span'."""

        if tag == "span":
            for attr in attrs:
                if attr[1] == "discreet":
                    self.dep = True

    def handle_endtag(self, tag: str) -> None:
        """Verify if the parser is at the end of the tag 'span'."""

        if tag == "span":
            self.dep = False

    def handle_data(self, data: str) -> None:
        """Get the data inside between the tags 'span'."""

        if self.dep:
            if "Dedução mensal por dependente:" in data:
                pos = data.find("$") + 1
                d = data[pos:]
                d = d.replace(",", ".").strip()
                self.value = float(d)


class INSS:
    """Create INSS data table."""

    def __init__(self, html_page=INSS_SOURCE) -> None:
        """Initialize this class."""

        self.html = self.get_source(html_page)
        self.parser = TableParser()
        self.parser.feed(self.html)
        self.parser.close()
        self.table = self.extract_data(self.parser.all_tables[0])

    def get_source(self, url: str) -> str:
        """Get source from a webpage."""

        response = urlopen(url)
        html = response.read()
        return html.decode("utf-8")

    def extract_data(self, table: list) -> list:
        """Extract data from a table and return a new table with the correct data."""

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

    def get_elements(self, row: list, elements_list: list) -> None:
        """Get the numeric value inside each cell and append it in the new row."""

        for cell in row:
            s = str(cell)
            s = s.strip()
            s = s.replace(".", "")
            s = s.replace(",", ".")
            s = s.replace("%", "")
            s = s.replace("\xa0", " ")
            s = s.replace(" ", "-")
            sl = s.split("-")
            for element in sl:
                e = element.replace(".", "")
                if e.isnumeric():
                    elements_list.append(float(element))


class IRPF(INSS):
    """Create IRPF data table."""

    def __init__(self) -> None:
        """Initialize this class."""

        super().__init__(html_page=IRPF_SOURCE)

    def extract_data(self, table: list) -> list:
        """Extract data from a table and return a new table with the correct data."""

        tb = []
        for row in range(0, len(table)):
            rw = []
            if row == 1:
                rw.append(0.0)
                self.get_elements(table[row], rw)
                rw.append(0.0)
                rw.append(0.0)
                tb.append(rw)
            elif (row > 1) and (row < 5):
                self.get_elements(table[row], rw)
                tb.append(rw)
            elif row == 5:
                self.get_elements(table[row], rw)
                rw.insert(1, inf)
                tb.append(rw)
        return tb


class DEP:
    """Create a DEP (dependent) class."""

    def __init__(self, html_page=IRPF_SOURCE) -> None:
        """Initialize this class."""

        self.html = self.get_source(html_page)
        self.parser = DepParser()
        self.parser.feed(self.html)
        self.parser.close()
        self.value = self.parser.value

    def get_source(self, url: str) -> str:
        """Get source from a webpage."""

        response = urlopen(url)
        html = response.read()
        return html.decode("utf-8")


if __name__ == "__main__":
    inss_table = INSS()
    irpf_table = IRPF()
    dependent_data = DEP()

    print("\n" + "=" * 12 + " INSS " + "=" * 12)
    for row in inss_table.table:
        print(row)

    print("\n" + "=" * 12 + " IRPF " + "=" * 12)
    for row in irpf_table.table:
        print(row)

    print("\n" + "=" * 12 + " DEP " + "=" * 12)
    print(f"R$ {dependent_data.value}")
