import copy
import time
class Box:
    def __init__(self,position = (None,None), value=0):
        self.value = value  
        self.position = position
        self.domain = set(range(1,10))
        self.pre_filled = False
    def __str__(self):
        return f"Box(Position={self.position}, Value={self.value}, Domain={self.domain})"
class Board:
    def __init__(self):
        self.grid = [[Box((i,j))for j in range(9)] for i in range(9)]

    def display_boxes(self):
        for row in self.grid:
            for box in row:
                print(box)

    def __str__(self):
        board = ""
        for row in self.grid:
            for box in row:
                board += f"{box.value} "
            board += "\n"
        return board.strip()
    
    def load_from_string_withDomains(self,puzzle_string):
        row = 0
        col = 0
        for num in puzzle_string:
            if num == ".":
                self.grid[row][col].value = 0
            else:
                self.grid[row][col].value = int(num)
            if col == 8:
                row +=1
            col = (col + 1) % 9
        self.find_domains_global()

    def load_from_string(self,puzzle_string):
        row = 0
        col = 0
        for num in puzzle_string:
            if num == ".":
                self.grid[row][col].value = 0
            else:
                self.grid[row][col].value = int(num)
                self.grid[row][col].pre_filled = True
            if col == 8:
                row +=1
            col = (col + 1) % 9


    def find_domains_global(self):
        for row in self.grid:
            for box in row:
                value = box.value
                if value != 0:
                    box.domain = set()
                    position = box.position
                    # Clear value in row
                    for i in range(9):
                        self.grid[position[0]][i].domain.discard(value)
                    # ## Clear value in column
                    for i in range(9):
                        self.grid[i][position[1]].domain.discard(value)
                    # ## Clear value in 3x3 square
                    start_row = position[0] // 3
                    start_col = position[1] // 3
                    for i in range(3):
                        for j in range(3):
                            self.grid[i+start_row*3][j+start_col*3].domain.discard(value)

    def forward_checking(self,position,value):
        for i in range(9):
            self.grid[position[0]][i].domain.discard(value)
            if len(self.grid[position[0]][i].domain) == 0 and self.grid[position[0]][i].value == 0:
                return False
            
        for i in range(9):
            self.grid[i][position[1]].domain.discard(value)
            if len(self.grid[i][position[1]].domain) == 0 and self.grid[i][position[1]].value == 0:
                return False
            
        start_row = position[0] // 3
        start_col = position[1] // 3
        for i in range(3):
            for j in range(3):
                self.grid[i+start_row*3][j+start_col*3].domain.discard(value)
                if len(self.grid[i+start_row*3][j+start_col*3].domain) == 0 and self.grid[i+start_row*3][j+start_col*3].value == 0:
                    return False
        return True

    def check_if_valid_assignment(self,position,value):

        for i in range(9):
            if self.grid[position[0]][i].value == value:
                return False
            
        for i in range(9):
            if self.grid[i][position[1]].value == value:
                return False
            
        start_row = position[0] // 3
        start_col = position[1] // 3
        for i in range(3):
            for j in range(3):
                if self.grid[i+start_row*3][j+start_col*3].value == value:
                    return False
        return True
    
    def check_if_valid_assignment_with_domains(self,position,value):

        for i in range(9):
            if self.grid[position[0]][i].value == value:
                return False
            
        for i in range(9):
            if self.grid[i][position[1]].value == value:
                return False
            
        start_row = position[0] // 3
        start_col = position[1] // 3
        for i in range(3):
            for j in range(3):
                if self.grid[i+start_row*3][j+start_col*3].value == value:
                    return False
                
        self.grid[position[0]][position[1]].value = value
        if self.update_domains(position,value):
            return True
        return False


    def find_empty(self):
        for row in self.grid:
            for box in row:
                if box.value == 0:
                    return box.position
        return None
    
    def solve_backtracking(self):
        position = self.find_empty()
        if position == None:
            return True
        for value in range(1,10):
            if self.check_if_valid_assignment(position,value):
                self.grid[position[0]][position[1]].value = value
                if self.solve_backtracking():
                    return True
                self.grid[position[0]][position[1]].value = 0
        return False
    
    def solve_backtracking_forwardChecking(self):
        position = self.find_empty()
        if position == None:
            return True

        for value in list(self.grid[position[0]][position[1]].domain):
            if self.check_if_valid_assignment(position,value):
                self.grid[position[0]][position[1]].value = value
                if self.forward_checking(position,value) and self.solve_backtracking_forwardChecking():
                    return True
                self.grid[position[0]][position[1]].value = 0
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j].domain = set(range(1,10))
                self.find_domains_global()
        return False
        
        

import pandas as pd
df = pd.read_csv("sudoku-3m.csv")
soduko_board = Board()
soduko_board.load_from_string_withDomains(df["puzzle"][0])
print(soduko_board)
start_time = time.time()
soduko_board.solve_backtracking_forwardChecking()
end_time = time.time()
print()
print(soduko_board)
time_taken = end_time - start_time
print(f"\nTime taken to solve: {time_taken:.4f} seconds")