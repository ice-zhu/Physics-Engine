import pygame, sys
from Primitives.circle2D import Circle
from Primitives.square2D import Square
from mouse_trajectory import Mouse_Trajectory as mT
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
        self.mouse_trajectory = mT([])
        
    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def start(self):
        self.shapeID = 0
        to_generate = False
        running = True
        self.mouse_trajectory.add_mouse_position(pygame.mouse.get_pos())
        active_object = None
        dragging = False
        isFloating = False
    
        staticObstacle = Square(init_position=(self.windowWidth * 0.5, self.windowHeight * 0.5), enable_gravity=False, is_walls=False) #if gravity is false, we know its a static obstacle
        self.primitive_shapes.append(staticObstacle)
        self.draw_static_walls()
        
        while running:
            mouse_cPos = pygame.mouse.get_pos()
            self.clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: #reset all balls position
                        print('Game quit by user')
                        running = False
                    elif event.key == pygame.K_a:  # Toggle circle generation/instansiation
                            if to_generate == True:
                                to_generate = False
                                print('circle generation is now disabled')
                            else:
                                to_generate = True
                                print('circle generation is now enabled')
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not to_generate:  # Do not generate shapes
                        mouse_pos = event.pos
                        for circle in self.primitive_shapes:
                            if circle.contains_point(mouse_pos):
                                if circle is not None:
                                    active_object = circle  # circle is clicked
                                    dragging = True  # Start dragging the shape
                                    print(f"circle {circle.id} follows mouse at {mouse_cPos}")
                                    circle.setSelected(True)  # circle is selected
                            else:
                                circle.setSelected(False)  # circle is not selected
                                active_object = None
                    else:  # OK to generate shapes
                        circle = Circle(init_position=event.pos)
                        if isFloating:
                            circle.gravity.toggle_floating(isFloating)
                        circle.setID(self.shapeID)
                        self.shapeID += 1
                        self.primitive_shapes.append(circle)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if active_object is not None and dragging:
                        dragging = False
                        if active_object.out_of_bounds:
                            print(f"circle {active_object.id} is out of bounds. Resetting position.")
                            self.check_wall_collisions(active_object)
                    active_object = None
                    for circle in self.primitive_shapes:
                        if circle is not None:
                            circle.setSelected(False)

                if dragging and active_object is not None:
                    print(f"circle {active_object.id} is being moved. Current mouse position: {mouse_cPos}")
                    self.move_shape_with_mouse(active_object, mouse_cPos)

            self.screen.fill((1, 1, 1))
            self.draw_text("Press A to generate shapes. Press A again to move the shapes.", 10, 10)
            
            self.iterate_through_list(self.primitive_shapes, mouse_cPos)
            self.check_collisions()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def iterate_through_list(self, primitive_shapes, mouse_cPos):
        for obj in primitive_shapes:
                if obj is not None:
                    if obj.init_position[0] > 0 and obj.init_position[1] < self.windowHeight:
                        obj.apply(mouse_cPos)
                        obj.draw(self.screen)
                    else:
                        obj.init_position[0] = self.windowHeight * 0.5

    
    def draw_static_walls(self):
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
    
    def move_shape_with_mouse(self, shape, mouse_pos):
        """Move the shape with the mouse, ensuring no collision with walls."""
        
        if hasattr(shape, 'radius'):
            width = height = 2 * shape.radius
        else:
            width = shape.width
            height = shape.height

        shape.init_position[0] = mouse_pos[0] - width // 2
        shape.init_position[1] = mouse_pos[1] - height // 2

        if shape.init_position[0] < wall_thickness:  # Left wall
            shape.init_position[0] = wall_thickness
            shape.out_of_bounds = True
        elif shape.init_position[0] + width > self.windowWidth - wall_thickness:  # Right wall
            shape.init_position[0] = self.windowWidth - width - wall_thickness
            shape.out_of_bounds = True

        if shape.init_position[1] < 0:  # Top wall
            shape.init_position[1] = 0
            shape.out_of_bounds = True

        elif shape.init_position[1] + height > self.windowHeight:  # Bottom wall
            shape.init_position[1] = self.windowHeight - height
            shape.out_of_bounds = True

        if shape.out_of_bounds: # redundant see a way to fix this as similar methods are doing the same thing already.
            shape.out_of_bounds = False 
            if hasattr(shape, 'radius'):
                if shape.init_position[0] < shape.radius:
                    shape.init_position[0] = shape.radius
                elif shape.init_position[0] > self.windowWidth - shape.radius:
                    shape.init_position[0] = self.windowWidth - shape.radius

                if shape.init_position[1] < shape.radius:
                    shape.init_position[1] = shape.radius
                elif shape.init_position[1] > self.windowHeight - shape.radius:
                    shape.init_position[1] = self.windowHeight - shape.radius

    def check_collisions(self):
        for i in range(len(self.primitive_shapes)):
            for j in range(i + 1, len(self.primitive_shapes)):
                shape1 = self.primitive_shapes[i]
                shape2 = self.primitive_shapes[j]
                if CollisionManager.handle_collision(shape1, shape2):
                    CollisionManager.resolve_collision(shape1, shape2)


    def check_wall_collisions(self, shape): #redundant too.
        if isinstance(shape, Circle):
            width = height = 2 * shape.radius 
            if shape.init_position[0] < wall_thickness:  # Left wall
                shape.init_position[0] = wall_thickness
                shape.out_of_bounds = False
            elif shape.init_position[0] + width > self.windowWidth - wall_thickness:  # Right wall
                shape.init_position[0] = self.windowWidth - width - wall_thickness
                shape.out_of_bounds = False

            if shape.init_position[1] < wall_thickness:  # Top wall
                shape.init_position[1] = 0
                shape.out_of_bounds = False

            elif shape.init_position[1] + height > self.windowHeight:  # Bottom wall
                shape.init_position[1] = self.windowHeight - height
                shape.out_of_bounds = False

       

        
        


