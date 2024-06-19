from engine import Calculator
from tkinter import Tk


class Window(Tk):
    def __init__(self):
        super().__init__()

        # Creating calculator
        self.engine = Calculator()

        self.mainloop()


if __name__ == "__main__":
    app = Window()
