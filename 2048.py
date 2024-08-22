import tkinter as tk
import random
from tkinter import messagebox

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.board = [[0] * 4 for _ in range(4)]
        self.colors = {0: "#ccc0b3", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                       16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
                       256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
        
        self.create_grid()
        self.spawn_new_tile()
        self.spawn_new_tile()
        self.update_grid()

        # Bind the arrow keys to the move function
        self.master.bind('<Left>', lambda event: self.move('left'))
        self.master.bind('<Right>', lambda event: self.move('right'))
        self.master.bind('<Up>', lambda event: self.move('up'))
        self.master.bind('<Down>', lambda event: self.move('down'))

    def create_grid(self):
        self.grid_frame = tk.Frame(self.master, bg="#bbada0", bd=3, width=400, height=400)
        self.grid_frame.grid()
        self.tiles = [[tk.Label(self.grid_frame, bg=self.colors[0], font=("Helvetica", 24), width=4, height=2)
                       for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].grid(row=i, column=j, padx=5, pady=5)

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                self.tiles[i][j].config(text=str(value) if value != 0 else "", bg=self.colors[value])

    def spawn_new_tile(self):
        empty_tiles = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        moved = False
        if direction == 'left':
            moved = self.move_left()
        elif direction == 'right':
            moved = self.move_right()
        elif direction == 'up':
            moved = self.move_up()
        elif direction == 'down':
            moved = self.move_down()
        
        if moved:
            self.spawn_new_tile()
            self.update_grid()
            if self.check_game_over():
                self.game_over()

    def move_left(self):
        moved = False
        for i in range(4):
            new_line, line_moved = self.merge(self.board[i])
            if line_moved:
                moved = True
            self.board[i] = new_line
        return moved

    def move_right(self):
        moved = False
        for i in range(4):
            new_line, line_moved = self.merge(self.board[i][::-1])
            if line_moved:
                moved = True
            self.board[i] = new_line[::-1]
        return moved

    def move_up(self):
        moved = False
        for j in range(4):
            col = [self.board[i][j] for i in range(4)]
            new_col, col_moved = self.merge(col)
            if col_moved:
                moved = True
            for i in range(4):
                self.board[i][j] = new_col[i]
        return moved

    def move_down(self):
        moved = False
        for j in range(4):
            col = [self.board[i][j] for i in range(4)]
            new_col, col_moved = self.merge(col[::-1])
            if col_moved:
                moved = True
            for i in range(4):
                self.board[i][j] = new_col[::-1][i]
        return moved

    def merge(self, line):
        new_line = [i for i in line if i != 0]
        merged = []
        moved = False
        skip = False
        for i in range(len(new_line)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
                merged.append(2 * new_line[i])
                moved = True
                skip = True
            else:
                merged.append(new_line[i])
        merged += [0] * (4 - len(merged))
        if merged != line:
            moved = True
        return merged, moved

    def check_game_over(self):
        if any(0 in row for row in self.board):
            return False
        for i in range(4):
            for j in range(4):
                if i < 3 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j + 1]:
                    return False
        return True

    def game_over(self):
        messagebox.showinfo("Game Over", "No more moves available. Game Over!")
        self.master.quit()

def main():
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()
