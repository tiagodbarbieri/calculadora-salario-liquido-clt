from engine import Calculator
from tkinter import Tk


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.engine = Calculator()
        self.mainloop()


if __name__ == "__main__":
    app = MainWindow()
