import tkinter as tk
from time import sleep
import load_maze
import breadth_first

class MainPage():
    def __init__(self, input_location, output_location, white_border = False):
        self.input_location = input_location
        self.output_location = output_location

        self.data, self.start, self.end = load_maze.get_grid(self.input_location, white_border)
        self.root = tk.Tk()
        self.run = tk.Button(self.root,command=self.show_explore, text='Run')
        self.run.pack(side='top')
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(side='top')
        self.explored, self.moves, _ = breadth_first.main(self.input_location, True)
        self.show_grid()

        self.root.mainloop()

    def show_grid(self):
        self.cells = {}
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                b = tk.Button(self.canvas, text='',width=1,height=1)
                if self.data[i][j] == 0:
                    b.config({'background' : 'Black'})
                else:
                    b.config({'background' : 'White'})
                b.grid(column=j, row =i )
                self.cells[(i,j)] = b

    def show_explore(self):
        for step in self.explored:
            if step in self.moves:
                self.cells[(step[0],step[1])].config({'background' : "Blue"})
            else:
                self.cells[(step[0],step[1])].config({'background' : "Red"})
            sleep(1)

if __name__ == "__main__":
    MainPage('Mazes/maze1.gif', 'BFS_complete_path.png', True)