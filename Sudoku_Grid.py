import numpy as np


class Sudoku_Grid():

    def __init__(self):
        self.locked_cells = []
        self.values = np.full(81, np.nan)
        self.integrity = np.full(81, True)

    def set_value(self, row, col, val):
        self.values[row*9 + col] = val
        self.check_integrity_cell(row*9 + col)

    def clear_value(self, row, col):
        self.values[row*9 + col] = np.nan

    def set_start_values(self):
        self.locked_cells = np.where(np.isfinite(self.values))[0]

    def clear_start_values(self):
        self.locked_cells = []

    def check_integrity_all(self):

        self.integrity[:] = True

        # check horizontally, row by row
        for row in range(9):
            self.check_integrity_row(row)

        # check vertically, column by column
        for col in range(9):
            self.check_integrity_col(col)

        # check sub-cells
        for box in range(9):
            self.check_integrity_box(box)

    def check_integrity_cell(self, cell):
        row = cell // 9
        col = cell - row * 9
        box = (row // 3)*3 + (col // 3)

        self.check_integrity_row(row)
        self.check_integrity_col(col)
        self.check_integrity_box(box)

    def check_integrity_row(self, row):
        for col_1 in range(9):
            for col_2 in range(8 - col_1):
                i1 = row*9 + col_1
                i2 = row*9 + col_1 + col_2 + 1
                if self.values[i1] == self.values[i2]:
                    self.integrity[i1] = True if i1 in self.locked_cells else False
                    self.integrity[i2] = True if i2 in self.locked_cells else False

    def check_integrity_col(self, col):
        for row_1 in range(9):
            for row_2 in range(8 - row_1):
                i1 = row_1*9 + col
                i2 = (row_1+row_2+1)*9 + col
                if self.values[i1] == self.values[i2]:
                    self.integrity[i1] = True if i1 in self.locked_cells else False
                    self.integrity[i2] = True if i2 in self.locked_cells else False

    def check_integrity_box(self, box):
        top_row = (box // 3) * 3
        left_col = (box % 3) * 3

        box_vals = self.values.reshape(9,9)[top_row:top_row+3, left_col:left_col+3].flatten()

        for i_1 in range(9):
            for i_2 in range(8-i_1):
                i_2 = i_1 + i_2 + 1
                if box_vals[i_1] == box_vals[i_2]:
                    i1 = (top_row + i_1//3)*9 + left_col + i_1 % 3
                    i2 = (top_row + i_2//3)*9 + left_col + i_2 % 3
                    self.integrity[i1] = True if i1 in self.locked_cells else False
                    self.integrity[i2] = True if i2 in self.locked_cells else False
