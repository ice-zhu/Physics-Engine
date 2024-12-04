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
        self.font = pygame.font.SysFont(None, 25)  # Initialize font
    
    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start(self):
        squareID = 0 #incremented each time a square is created
        #self.generateStaticObstacle()
        to_generate = False #introduce a toggle function
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
                    elif event.key == pygame.K_a: #toggle square generation¨
                        print('A has been pressed, square will now generate on mouse click')
                        if to_generate == False:
                            to_generate = True
                        else: 
                            print('A has been pressed, squares will not generate on mouse click')
                            to_generate = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if to_generate == False: #Do not generate squares
                        mouse_pos = event.pos
                        for square in self.squares:
                            if square.contains_point(mouse_pos):
                                print(f"Square with ID {square.id} was clicked at position {mouse_pos}")
                    else: #OK to generate squares
                        square = Square(init_position=event.pos)
                        square.setID(squareID)
                        squareID += 1
                        self.squares.append(square)
                        print('Square created at:', event.pos)
                    #throw functionality ?
                
            self.screen.fill((1, 1, 1))
            self.draw_text("Press A to generate squares. Press A again to move the squares.", 10, 10)
            self.walls = self.draw_walls() #collision

            for square in self.squares:
                square.apply()
                square.draw(self.screen)
            
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