import pygame, sys
from Primitives.circle2D import Circle
from mouse_trajectory import Mouse_Trajectory as mT
from collision import CollisionForCircle as Collision
from static_obstacle import StaticObstacle as sO

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
        self.primitive_shapes = []
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 25)
        self.mouse_trajectory = mT([])
        self.sO = sO(self.screen, (self.windowWidth * 0.5, self.windowHeight * 0.5), 300, 50, (255, 255, 255))
    
    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start(self):
        shapeID = 0
        to_generate = False
        running = True
        self.mouse_trajectory.add_mouse_position(pygame.mouse.get_pos())
        active_object = None
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
                    elif event.key == pygame.K_a:  # Toggle circle generation/instansiation
                            if to_generate == True:
                                to_generate = False
                                print('circle generation is now disabled')
                            else:
                                to_generate = True
                                print('circle generation is now enabled')
                            #to_generate = not to_generate
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not to_generate:  # Do not generate shapes
                        mouse_pos = event.pos
                        for circle in self.primitive_shapes:
                            if circle.contains_point(mouse_pos):
                                active_object = circle  # circle is clicked
                                dragging = True  # Start dragging the shape
                                print(f"circle {circle.id} follows mouse at {mouse_cPos}")
                                circle.setSelected(True)  # circle is selected
                            else:
                                circle.setSelected(False)  # circle is not selected
                                active_object = None
                    else:  # OK to generate shapes
                        circle = Circle(init_position=event.pos)
                        circle.setID(shapeID)
                        shapeID += 1
                        self.primitive_shapes.append(circle)
                        print('circle created at:', event.pos)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if active_object is not None and dragging:
                        dragging = False
                        if active_object.out_of_bounds:
                            print(f"circle {active_object.id} is out of bounds. Resetting position.")
                            self.check_wall_collisions(active_object)
                    active_object = None
                    for circle in self.primitive_shapes:
                        circle.setSelected(False)

                if dragging and active_object is not None:
                    print(f"circle {active_object.id} is being moved. Current mouse position: {mouse_cPos}")
                    self.move_shape_with_mouse(active_object, mouse_cPos)

            self.screen.fill((1, 1, 1))
            self.draw_text("Press A to generate shapes. Press A again to move the shapes.", 10, 10)
            self.walls = self.draw_walls()
            
            for circle in self.primitive_shapes:
                circle.apply(mouse_cPos)
                circle.draw(self.screen)

            self.sO.draw()

            self.check_collisions()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def draw_walls(self):
        left = pygame.draw.line(self.screen, 'white', (0, 0), (0, self.windowHeight), wall_thickness)
        right = pygame.draw.line(self.screen, 'white', (self.windowWidth, 0), (self.windowWidth, self.windowHeight), wall_thickness)
        top = pygame.draw.line(self.screen, 'white', (0, 0), (self.windowWidth, 0), wall_thickness)
        bottom = pygame.draw.line(self.screen, 'white', (0, self.windowHeight), (self.windowWidth, self.windowHeight), wall_thickness)
        wall_list = [left, right, top, bottom]
        return wall_list
    
    def move_shape_with_mouse(self, shape, mouse_pos):
        """Move the circle with the mouse, ensuring no collision with walls."""
        shape.init_position[0] = mouse_pos[0] - shape.width // 2
        shape.init_position[1] = mouse_pos[1] - shape.height // 2

        if shape.init_position[0] < wall_thickness:  # Left wall
            shape.init_position[0] = wall_thickness
            shape.out_of_bounds = True
        elif shape.init_position[0] + shape.width > self.windowWidth - wall_thickness:  # Right wall
            shape.init_position[0] = self.windowWidth - shape.width - wall_thickness
            shape.out_of_bounds = True

        if shape.init_position[1] < 0:  # Top wall
            shape.init_position[1] = 0
            shape.out_of_bounds = True

        elif shape.init_position[1] + shape.height > self.windowHeight:  # Bottom wall
            shape.init_position[1] = self.windowHeight - shape.height
            shape.out_of_bounds = True

    def check_collisions(self):
        for i in range(len(self.primitive_shapes)):
            for j in range(i + 1, len(self.primitive_shapes)):
                shape1 = self.primitive_shapes[i]
                shape2 = self.primitive_shapes[j]
                if Collision.check_collision(shape1, shape2):
                    Collision.resolve_collision(shape1, shape2)

    def check_wall_collisions(self, shape):
        old_x_pos = shape.init_position[0] #modularize this
        old_y_pos = shape.init_position[1]

        if old_x_pos < shape.width or old_x_pos > self.windowWidth - shape.width:  # Check if out of bounds on left or right
            shape.init_position[0] = wall_thickness  # Reset to left boundary
        elif old_x_pos > self.windowWidth - shape.width:  # For right boundary
            shape.init_position[0] = self.windowWidth*2 - 50  # Reset to the right boundary
        elif (old_y_pos < shape.height or old_y_pos > self.windowHeight + shape.height): #if out of y bound but within x bound
            shape.init_position[1] = wall_thickness
        elif old_x_pos and old_y_pos < 100: #check how to deal with edges
            shape.init_position[0] = self.windowWidth / 2
            shape.init_position[1] = self.windowHeight / 2
        
        print(f"Old position: ({old_x_pos}, {old_y_pos})")
        shape.setOutOfBounds(False, self.screen)
        
        


