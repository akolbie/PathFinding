from pygame.locals import *
import pygame 
from math import floor
import breadth_first
from load_maze import get_grid


class App:
 
    player = 0
 
    def __init__(self, data, start, end, explored, path, block_width, block_height):
        self.bw = block_width
        self.bh = block_height
        self.windowWidth = len(data[0]) * self.bw
        self.windowHeight = len(data) * self.bh
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.maze = Maze(data, start, end, explored, path, self.bw, self.bh)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Pygame pythonspot.com example')
        self._running = True
        self._image_surf = pygame.image.load("Blocks/player.png").convert()
        self._block_surf = pygame.image.load("Blocks/block.png").convert()
        self._start_surf = pygame.image.load("Blocks/start.png").convert()
        self._end_surf = pygame.image.load("Blocks/end.png").convert()
        self._explored_surf = pygame.image.load("Blocks/explored.png").convert()
        self._path_surf = pygame.image.load("Blocks/path.png").convert()

 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.maze.draw(self._display_surf, self._block_surf, self._start_surf, self._end_surf, self._explored_surf, self._path_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):

            self.on_render()
        self.on_cleanup()
      

class Maze:
    def __init__(self, data, start, end, explored, path, bw, bh):
        self.M = len(data[0])
        self.N = len(data)

        self.maze = data[:]
        self.start = start
        self.end = end
        self.explored = explored
        self.path = path
        self.counter = 0

        self.bw = bw
        self.bh = bh

    def draw(self, display_surf, block_surf, start_surf, end_surf, explored_surf, path_surf):
        self.counter += 1
        steps = floor(self.counter / .1)

        for row_index, row in enumerate(self.maze):
            for i_index, i in enumerate(row):
                if i == 1:
                    display_surf.blit(block_surf,(i_index * self.bw, row_index * self.bh))
        
        display_surf.blit(start_surf,(self.start[1] * self.bh, self.start[0] * self.bw))
        display_surf.blit(end_surf, (self.end[1] * self.bh, self.end[0] * self.bw))

        for i in range(min(len(self.explored) - 1, steps)):
            display_surf.blit(explored_surf,(self.explored[i][1] * self.bh, self.explored[i][0] * self.bw))

        for j in range(min(max(0, steps - (len(self.explored) - 1)), len(self.path) - 1)):
            display_surf.blit(path_surf, (self.path[j][1] * self.bh, self.path[j][0] * self.bw))


if __name__ == "__main__" :
    data, start, end = get_grid("Mazes/maze1.gif", True)
    explored, path = breadth_first.breadth_first_main(data, start, end)
    theApp = App(data, start, end, explored, path, 10, 10)
    theApp.on_execute()