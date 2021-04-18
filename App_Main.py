from tkinter import *
from functools import partial
from Sudoku_Grid import Sudoku_Grid

grid = Sudoku_Grid()


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.cells = [None for i in range(81)]
        self.init_window()

    def init_window(self):
        self.pack(expand=1)
        self.configure(background='black')
        for i in range(3):
            for j in range(3):
                b = Box(self, i*3+j)
                b.grid(row=i, column=j, padx=3, pady=3)

        self.master.title('Sudoku')

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=False)
        file.add_command(label='Lock', command=partial(self.lock_cells, file))
        file.add_command(label='Open Solver', command=self.open_solver)
        file.add_command(label='Exit', command=self.client_exit)

        menu.add_cascade(label='File', menu=file)

    def lock_cells(self, file):
        action = file.entrycget(0, 'label')

        if action == 'Lock':
            file.entryconfig(0, label='Unlock')

            grid.set_start_values()
            for i in grid.locked_cells:
                self.cells[i].lock_cell()

        else:
            file.entryconfig(0, label='Lock')

            for i in grid.locked_cells:
                self.cells[i].unlock_cell()
            grid.clear_start_values()

    def open_solver(self):
        print(self.master.children)
        if '!solverwindow' not in self.master.children:
            solver = SolverWindow(self.master, self)

    def client_exit(self):
        exit()

    def repaint_cell_colors(self):
        for c in self.cells:
            if grid.integrity[c.id]:
                c.paint_right()
            else:
                c.paint_wrong()


class Box(Frame):

    def __init__(self, master=None, id=None):
        Frame.__init__(self, master)
        self.master = master
        self.id = id
        self.init_box()

    def init_box(self):
        self.configure(background='grey')
        for i in range(3):
            for j in range(3):
                cell_id = ((self.id // 3)*3 + i)*9 + (self.id % 3)*3 + j

                c = Cell(self, cell_id)
                c.grid(row=i, column=j, padx=1, pady=1, sticky=N+E+S+W)
                self.master.cells[cell_id] = c


class Cell(Frame):

    def __init__(self, master=None, id=None):
        Frame.__init__(self, master)
        self.master = master
        self.id = id
        self.buttons = []
        self.label = None
        self.init_cell()

    def init_cell(self):
        self.configure(background='white')
        for i in range(3):
            for j in range(3):
                button = Button(self, text=i*3+j+1)
                button.config(command=partial(self.fill_cell, button), background='white')
                button.bind('<Button-3>', self.cell_option_right_click)

                self.buttons.append(button)

                button.grid(row=i, column=j)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def fill_cell(self, button):
        for b in self.buttons:
            b.grid_remove()

        num = int(button['text'])
        grid.set_value(self.id // 9, self.id % 9, num)

        if not self.label:
            self.label = Button(self, command=self.empty_cell)
            # self.label.bind('<Button-1>', self.empty_cell)

        self.label.config(text=num, font=('bold'))

        self.label.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=N+E+S+W)
        self.grid_propagate(False)

        self.master.master.repaint_cell_colors()

    def empty_cell(self):
        for b in self.buttons:
            b.grid()

        grid.clear_value(self.id // 9, self.id % 9)

        self.label.grid_forget()
        self.grid_propagate(True)

        grid.check_integrity_all()
        self.master.master.repaint_cell_colors()

    def lock_cell(self):
        self.label.config(state=DISABLED, background='black', disabledforeground='white')

    def unlock_cell(self):
        self.label.config(state=NORMAL, background='white')

    def cell_option_right_click(self, event):
        button = event.widget
        if button['state'] == NORMAL:
            button['state'] = DISABLED
            button['disabledforeground'] = button['background']
        else:
            button['state'] = NORMAL

    def paint_right(self):
        if self.label and self.id not in grid.locked_cells:
            self.label.config(background='white')

    def paint_wrong(self):
        if self.label:
            self.label.config(background='red')

    def noop(self):
        pass


class SolverWindow(Toplevel):

    def __init__(self, master, grid_window):
        Toplevel.__init__(self, master)
        self.master = master
        self.app = grid_window
        self.init_window()

    def init_window(self):
        self.title('Solver')
        pass


root = Tk()

app = Window(root)
app.mainloop()
