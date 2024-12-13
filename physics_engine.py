import pygame, sys
from Primitives.circle2D import Circle
from Primitives.square2D import Square
from collision import CollisionManager
from Primitives.shape_type import ShapeType

wall_thickness = 5
fps = 60
out_of_bounds = False

class Physics_Engine:
    def __init__(self) -> None:
        pygame.init()
        self.windowWidth = 800
        self.windowHeight = 600
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Physics Engine")
        self.primitive_shapes = []
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 25)
        
        
    def draw_text(self, text, x, y):
        '''Draws text on the screen.'''
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start(self):
        '''Starts the physics engine.'''
        self.collided_with_selected_object = [] #keep track of objects who collided with the active object
        self.shapeID = 0
        to_generate = False
        running = True
    
        active_object = None
        dragging = False

        staticObstacle = Square(init_position=(self.windowWidth * 0.5, self.windowHeight * 0.5), enable_gravity=False, is_walls=False)
        self.primitive_shapes.append(staticObstacle)
        self.draw_static_walls()

        while running:
            mouse_cPos = pygame.mouse.get_pos()  # Update mouse position
            self.clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Quit game
                        print('Clear all shapes')
                        self.clear_all_shapes()
                    elif event.key == pygame.K_a:  # Toggle shape generation
                        to_generate = not to_generate
                        print(f"Circle generation is now {'enabled' if to_generate else 'disabled'}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not to_generate:  # Check for existing shapes
                        mouse_pos = event.pos
                        for circle in self.primitive_shapes:
                            if circle is not None and circle.contains_point(mouse_pos) and circle.type == ShapeType.CIRCLE:
                                active_object = circle  # Select the clicked circle
                                dragging = True
                                circle.setSelected(True)  # Highlight the circle
                                self.check_collisions()
                                break  # Exit loop after selecting one circle
                    else:  # Generate a new circle
                        circle = Circle(init_position=event.pos)
                        circle.setID(self.shapeID)
                        self.shapeID += 1
                        self.primitive_shapes.append(circle)
                elif event.type == pygame.MOUSEBUTTONUP: # Upon release of mouse
                    mouse_pos = event.pos # We need to know where we released the selected shape
                    if active_object is not None and dragging:
                        dragging = False
                        self.check_if_selected_shape_of_bounds(active_object, mouse_pos)
                        if active_object.out_of_bounds: # If out of bounds upon release, reset position
                            print(f"circle {active_object.id} is out of bounds. Resetting position.")
                            self.reset_shape_position(active_object, new_pos_x = self.windowWidth / 2, new_pos_y= self.windowHeight / 2)
                    active_object = None
                    for circle in self.primitive_shapes:
                        if circle is not None:
                            circle.setSelected(False)

            if dragging and active_object is not None: # Used for debugging
                print(f"circle {active_object.id} is being moved. Current mouse position: {mouse_cPos}")

            self.screen.fill((1, 1, 1))  # Clear screen
            self.draw_text("Press A to generate shapes. Press A again to move the shapes.", 10, 10)
            self.iterate_through_list(self.primitive_shapes, mouse_cPos)
            self.check_collisions()
            self.draw_walls()
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()


    def iterate_through_list(self, primitive_shapes, mouse_cPos):
        '''Iterates through the list of shapes to draw the objects and update their positions continously.'''
        for obj in primitive_shapes:
                if obj is not None:
                    if obj.type == ShapeType.CIRCLE:
                            obj.apply(mouse_cPos)
                            obj.draw(self.screen)
                    else:
                        obj.draw(self.screen) # Manages squares

    def draw_walls(self):
        '''Draws the walls of the screen though visually.'''
        left = pygame.draw.line(self.screen, 'white', (0, 0), (0, self.windowHeight), wall_thickness)
        right = pygame.draw.line(self.screen, 'white', (self.windowWidth, 0), (self.windowWidth, self.windowHeight), wall_thickness)
        top = pygame.draw.line(self.screen, 'white', (0, 0), (self.windowWidth, 0), wall_thickness)
        bottom = pygame.draw.line(self.screen, 'white', (0, self.windowHeight), (self.windowWidth, self.windowHeight), wall_thickness)
        wall_list = [left, right, top, bottom]
        return wall_list
    
    def draw_static_walls(self):
        '''Draws the walls of the screen by creating objects of squares.'''
        left = Square(init_position=(0, self.windowHeight), enable_gravity=False, is_walls=True).setID(self.shapeID)
        self.shapeID += 1

        right = Square(init_position=(self.windowWidth - wall_thickness, 0), enable_gravity=False, is_walls=True).setID(self.shapeID)
        self.shapeID += 1

        top = Square(init_position=(0, 0), enable_gravity=False, is_walls=True).setID(self.shapeID)
        self.shapeID += 1
        
        bottom = Square(init_position=(0, self.windowHeight - wall_thickness), enable_gravity=False, is_walls=True).setID(self.shapeID)
        self.shapeID += 1
        wall_list = [left, right, top, bottom]

        for wall in wall_list:
            if wall is not None:
                self.primitive_shapes.append(wall)
        return wall_list

    def check_collisions(self):
        '''Checks for collisions between shapes'''
        for i in range(len(self.primitive_shapes)):
            for j in range(i + 1, len(self.primitive_shapes)):
                shape1 = self.primitive_shapes[i]
                shape2 = self.primitive_shapes[j]
                if CollisionManager.handle_collision(shape1, shape2):
                    print(f"Collision between {shape1.id} and {shape2.id} detected.")
                    

    def reset_shape_position (self, shape, new_pos_x, new_pos_y): # In case of release of selection,
        '''Resets the position of the shape to the center of the screen.'''
        shape.init_position[0] = new_pos_x
        shape.init_position[1] = new_pos_y
        shape.out_of_bounds = False
    

    def check_if_selected_shape_of_bounds(self, shape, mouse_pos):
        '''Check if the selected shape is out of bounds.'''
        if hasattr(shape, 'radius'):
            width = 2 * shape.radius
        else:
            width = shape.width

        if mouse_pos[0] <= 0: # If beyond the horizontal walls
            shape.out_of_bounds = True
            print(f"circle {shape.id} went past the left wall.")
        elif mouse_pos[0] + shape.radius >= self.windowWidth - width - (wall_thickness * 2) + shape.radius: # If beyond the horizontal walls
            shape.out_of_bounds = True
            print(f"circle {shape.id} went past the right wall.")
        if mouse_pos[1] <= 0:  # Top wall
            shape.out_of_bounds = True
            print(f"circle {shape.id} went past the top wall.")
        elif mouse_pos[1] + width > self.windowHeight - wall_thickness:  # Bottom wall
            shape.out_of_bounds = True
            print(f"circle {shape.id} went past the bottom wall.")

    def clear_all_shapes(self):
        """Set shapes to None conditionally to erase all shapes within the list."""
        for i, shape in enumerate(self.primitive_shapes):
            if shape is not None and shape.id != -1:
                self.primitive_shapes[i] = None



        
        


