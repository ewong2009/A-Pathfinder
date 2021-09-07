import sys
import pygame as pg


BACKGROUND = pg.Color("lightgrey")
BLACK = (0,0,0)
SIDE = 500
FPS = 60
BLOCKSIZE = 20 #Set the size of the grid block
SIZE = int(SIDE / BLOCKSIZE)

class Node:
    def __init__(self, on, coord):
        self.on = on
        self.coord = coord
        self.g = 0
        self.h = 0       
        self.f = 0
        self.parent = None
        
    def updateF(self):
        self.f = self.h + self.g
    
    def setG(self, value):
        self.g = value
        self.updateF()
    
    def setH(self, value):
        self.h = value
        self.updateF()
    
    def setParent(self, node):
        self.parent = node
    
    def display(self):
        print("Passable:", bool(self.on), "\nCoord:", self.coord, "\nG Score:", self.g, "\nH Score:", self.h, "\nF Score:", self.f)
        
class App(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False

    def update(self):
        """
        All updates to all actors occur here.
        Exceptions include things that are direct results of events which
        may occasionally occur in the event loop.
        For example, updates based on held keys should be found here, but
        updates to single KEYDOWN events would be found in the event loop.
        """
        pass

    def render(self):
        """
        All calls to drawing functions here.
        No game logic.
        """
        self.screen.fill(BACKGROUND)
        pg.display.update()

    def event_loop(self):
        """
        Event handling here.  Only things that are explicit results of the
        given events should be found here.  Do not confuse the event and update
        phases.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        """
        Main loop for your whole app.  This doesn't need to be touched until
        you start writing framerate independant games.
        """
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
def drawGrid(): 
    for x in range(0, SIDE, BLOCKSIZE):
        for y in range(0, SIDE, BLOCKSIZE):
            rect = pg.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pg.draw.rect(SCREEN, BLACK, rect, 1)
            
def colorBox(color, x, y):
    pg.draw.rect(SCREEN,color,pg.Rect(x * BLOCKSIZE, y * BLOCKSIZE, BLOCKSIZE, BLOCKSIZE))
    

def main():
    global SCREEN
    pg.init()
    pg.display.set_caption('Pathfinder')
    SCREEN = pg.display.set_mode((SIDE, SIDE))
    SCREEN.fill(BACKGROUND)
    clicks = 0
    selected = set()
    grid = CreateGrid(SIZE)
    ready = True
    while True:
        drawGrid()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        if ready:
            click = pg.mouse.get_pressed() 
            if click[0]:
                coord = pg.mouse.get_pos() 
                x = int(coord[0] / BLOCKSIZE)
                y = int(coord[1]  / BLOCKSIZE)           
                if (x,y) not in selected:
                    selected.add((x,y))                           
                    if clicks == 0:
                        colorBox('orange', x, y)
                        start = grid[x][y]
                        clicks += 1                    
                    elif clicks == 1:
                        colorBox('orange', x, y)
                        clicks += 1   
                        end = grid[x][y]
                    else:
                        colorBox('black', x, y)
                        grid[x][y].on = 0
                    
            if event.type == pg.KEYDOWN:
                ready = False
                if event.key == pg.K_RETURN:
                    path = Solve(grid, start, end)                  
                    if path: 
                        displayPath(path)                                 
                                                                    
        pg.display.update()
        
def displayPath(path):
    for item in path[1:-1]:
        colorBox('green', item.coord[0], item.coord[1])
        
class Node:
    def __init__(self, on, coord):
        self.on = on
        self.coord = coord
        self.g = 0
        self.h = 0       
        self.f = 0
        self.parent = None
        
    def updateF(self):
        self.f = self.h + self.g
    
    def setG(self, value):
        self.g = value
        self.updateF()
    
    def setH(self, value):
        self.h = value
        self.updateF()
    
    def setParent(self, node):
        self.parent = node
    
    def display(self):
        print("Passable:", bool(self.on), "\nCoord:", self.coord, "\nG Score:", self.g, "\nH Score:", self.h, "\nF Score:", self.f)
    
        
def CreateGrid(size):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(Node(1, (i, j)))
        grid.append(row)
    return grid 

def FindPath(node):
    path = []
    while node.parent:
        path.append(node)
        node = node.parent
    path.append(node)
    path.reverse()
    return path

def Solve(grid, start, end):
    opened, closed = set(), set()
    adjacent = {(0,-1),(0,1),(1,0),(-1,0)}
    opened.add(start)
    while opened:
        current = min(opened, key = lambda a: a.f)
        opened.remove(current)
        closed.add(current)        
        if current == end:
            return FindPath(end)
        for y,x in adjacent:
            nY = current.coord[0] + y
            nX = current.coord[1] + x
            if 0 <= nY < SIZE and 0 <= nX < SIZE:
                neighbour = grid[nY][nX]
                if neighbour.on and neighbour not in closed:
                    GScore = current.g + 1
                    HScore = abs(end.coord[0] - neighbour.coord[0]) + abs(end.coord[1] - neighbour.coord[1])
                    if neighbour not in opened:
                        neighbour.setG(GScore)
                        neighbour.setH(HScore)
                        neighbour.setParent(current)
                        opened.add(neighbour)
                    elif neighbour.f > GScore + HScore:
                        neighbour.setG(GScore) 
                        neighbour.setH(HScore)
                        neighbour.setParent(current)     
    return False       
  


if __name__ == "__main__": 
    main()

    