import pygame
import sys
from Primitives.square2D import Square
from mouse_trajectory import Mouse_Trajectory as mT

wall_thickness = 5
fps = 60
mouse_trajectory = []
out_of_bounds = False

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
        self.mouse_trajectory = mT([])
    
    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start(self):
        squareID = 0 #incremented each time a square is created
        #self.generateStaticObstacle()
        to_generate = False #introduce a toggle function
        running = True
        self.mouse_trajectory.add_mouse_position(pygame.mouse.get_pos())

        while running:
            mouse_cPos = pygame.mouse.get_pos() #coordinates of the mouse's current position
            self.clock.tick(fps)
            active_square = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('game quit by user')
                        running = False
                    elif event.key == pygame.K_a: #toggle square generation¨
                        print('Squares will now generate on mouse click')
                        if to_generate == False:
                            to_generate = True
                        else: 
                            print('Squares will not generate on mouse click [THROW ACTIVATED]')
                            to_generate = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if to_generate == False: #Do not generate squares
                        mouse_pos = event.pos
                        for square in self.squares:
                            if square.contains_point(mouse_pos):
                                active_square = square #square is clicked
                                print(f"Square {square.id} follows mouse at {mouse_cPos}")
                                square.setSelected(True) #square is selected
                                while active_square.out_of_bounds == False:
                                    self.move_square_with_mouse(square, mouse_pos)
                                    if active_square.out_of_bounds == True:
                                        print('!!!!!!!!!!!!!Square is not out of bounds')
                                        active_square.init_position[1] = 200
                                        active_square.init_position[0] = 200
                                        active_square.draw(self.screen)
                                        square.apply(mouse_cPos)
                                        square.draw(self.screen)
                            else:
                                square.setSelected(False) #square is not selected
                                active_square = None
                    else: #OK to generate squares
                        square = Square(init_position=event.pos)
                        square.setID(squareID)
                        squareID += 1
                        self.squares.append(square)
                        print('Square created at:', event.pos)             
                elif event.type == pygame.MOUSEBUTTONUP: #when we release the selected mouse button
                    if active_square is not None and active_square.out_of_bounds == True:
                        print('Square is out of bounds')
                        active_square.init_position[1] = 200
                        active_square.init_position[0] = 200
                        active_square.setOutOfBounds(False)
                    active_square = None #no square is selected
                    for square in self.squares:
                        square.setSelected(False)
                
            self.screen.fill((1, 1, 1))
            self.draw_text("Press A to generate squares. Press A again to move the squares.", 10, 10)
            self.walls = self.draw_walls() #collision

            for square in self.squares:
                square.apply(mouse_cPos)
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
    
    def move_square_with_mouse(self, square, mouse_pos):
        """Move the square with the mouse, ensuring no collision with walls."""
        # Center the square on the mouse position
        square.init_position[0] = mouse_pos[0] - square.width // 2
        square.init_position[1] = mouse_pos[1] - square.height // 2

        # Prevent the square from going out of bounds and keep it at the wall when touching
        if square.init_position[0] < wall_thickness:  # Left wall
            square.init_position[0] = wall_thickness
            
            print('Square is out of bounds on the left wall')
            square.out_of_bounds = True
        elif square.init_position[0] + square.width > self.windowWidth - wall_thickness:  # Right wall
            square.init_position[0] = self.windowWidth - square.width - wall_thickness
            print('Square is out of bounds on the right wall')
            square.out_of_bounds = True


        if square.init_position[1] < 0:  # Top wall
            square.init_position[1] = 0
            print('Square is out of bounds on the top wall')
            square.out_of_bounds = True


        elif square.init_position[1] + square.height > self.windowHeight:  # Bottom wall
            square.init_position[1] = self.windowHeight - square.height
            square.out_of_bounds = True
            print('Square is out of bounds on the bottom wall')

        if square.out_of_bounds == True:
            square.reset_pos(self.windowWidth, self.windowHeight)

        


