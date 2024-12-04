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
        self.font = pygame.font.SysFont(None, 25)
        self.mouse_trajectory = mT([])
    
    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start(self):
        squareID = 0
        to_generate = False
        running = True
        self.mouse_trajectory.add_mouse_position(pygame.mouse.get_pos())
        active_square = None
        dragging = False

        while running:
            mouse_cPos = pygame.mouse.get_pos()
            self.clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('Game quit by user')
                        running = False
                    elif event.key == pygame.K_a:  # Toggle square generation/instansiation
                        print('Squares will now generate on mouse click')
                        to_generate = not to_generate
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not to_generate:  # Do not generate squares
                        mouse_pos = event.pos
                        for square in self.squares:
                            if square.contains_point(mouse_pos):
                                active_square = square  # Square is clicked
                                dragging = True  # Start dragging the square
                                print(f"Square {square.id} follows mouse at {mouse_cPos}")
                                square.setSelected(True)  # Square is selected
                            else:
                                square.setSelected(False)  # Square is not selected
                                active_square = None
                    else:  # OK to generate squares
                        square = Square(init_position=event.pos)
                        square.setID(squareID)
                        squareID += 1
                        self.squares.append(square)
                        print('Square created at:', event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if active_square is not None and dragging:
                        dragging = False
                        if active_square.out_of_bounds:
                            print(f"Square {active_square.id} is out of bounds. Resetting position.")
                            old_x_pos = active_square.init_position[0]
                            old_y_pos = active_square.init_position[1]
                            if old_x_pos < wall_thickness and old_y_pos > wall_thickness: #if out of x bound but within y bound
                                active_square.init_position[0] = wall_thickness
                            elif old_y_pos < wall_thickness and old_x_pos > wall_thickness: #if out of y bound but within x bound
                                active_square.init_position[1] = wall_thickness
                            elif old_x_pos and old_y_pos < wall_thickness: #if both
                                active_square.init_position[0] = self.windowWidth / 2
                                active_square.init_position[1] = self.windowHeight / 2
                            
                            print(f"Old position: ({old_x_pos}, {old_y_pos})")
                            active_square.setOutOfBounds(False, self.screen)
                    active_square = None
                    for square in self.squares:
                        square.setSelected(False)

                if dragging and active_square is not None:
                    print(f"Square {active_square.id} is being moved. Current mouse position: {mouse_cPos}")
                    self.move_square_with_mouse(active_square, mouse_cPos)

            self.screen.fill((1, 1, 1))
            self.draw_text("Press A to generate squares. Press A again to move the squares.", 10, 10)
            self.walls = self.draw_walls()

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
        square.init_position[0] = mouse_pos[0] - square.width // 2
        square.init_position[1] = mouse_pos[1] - square.height // 2

        if square.init_position[0] < wall_thickness:  # Left wall
            square.init_position[0] = wall_thickness
            square.out_of_bounds = True
        elif square.init_position[0] + square.width > self.windowWidth - wall_thickness:  # Right wall
            square.init_position[0] = self.windowWidth - square.width - wall_thickness
            square.out_of_bounds = True

        if square.init_position[1] < 0:  # Top wall
            square.init_position[1] = 0
            square.out_of_bounds = True

        elif square.init_position[1] + square.height > self.windowHeight:  # Bottom wall
            square.init_position[1] = self.windowHeight - square.height
            square.out_of_bounds = True
        


