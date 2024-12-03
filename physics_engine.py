import pygame
import sys
from Primitives.square2D import Square

wall_thickness = 5
fps = 60

class Physics_Engine:
    def __init__(self) -> None:
        pygame.init()
        self.windowWidth = 800
        self.windowHeight = 600
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption("Physics Engine")
        self.squares = []
        self.clock = pygame.time.Clock()
    
    def start(self):
        #self.generateStaticObstacle()
        running = True
        while running:
            self.clock.tick(fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('game quit by user')
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    square = Square(init_position=event.pos)
                    self.squares.append(square)
                    print('Square created at:', event.pos)
                #throw functionality ?

            self.screen.fill((1, 1, 1))
            self.walls = self.draw_walls() #collision

            for obj in self.squares:
                square.apply()
                obj.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def generateStaticObstacle(self):
        """Generates a static obstacle in the middle of the screen"""

        static_square = Square((self.windowWidth * 0.5, self.windowHeight * 0.5))
        static_square.width = 300
        static_square.height = 50
        static_square.color = (0, 0, 0)
        self.squares.append(static_square)

    def draw_walls(self):
        left = pygame.draw.line(self.screen, 'white', (0, 0), (0, self.windowHeight), wall_thickness)
        right = pygame.draw.line(self.screen, 'white', (self.windowWidth, 0), (self.windowWidth, self.windowHeight), wall_thickness)
        top = pygame.draw.line(self.screen, 'white', (0, 0), (self.windowWidth, 0), wall_thickness)
        bottom = pygame.draw.line(self.screen, 'white', (0, self.windowHeight), (self.windowWidth, self.windowHeight), wall_thickness)
        wall_list = [left, right, top, bottom]
        return wall_list