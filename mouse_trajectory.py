class Mouse_Trajectory:
    def __init__(self, mouse_trajectory=None):
        if mouse_trajectory == None: #Singleton
            self.mouse_trajectory = []
        else:
            self.mouse_trajectory = mouse_trajectory

    def check_mouse_trajectory(self, fps):
        if len(self.mouse_trajectory) > (fps/3):
            self.mouse_trajectory.pop(0)
        x_force, y_force = self.calculate_motion_vector() #check this
        return x_force, y_force

    def calculate_motion_vector(self):
        x_force, y_force = 0, 0
        if len(self.mouse_trajectory) > (len(self.mouse_trajectory) / 2):
            x_force = self.mouse_trajectory[-1][0] - self.mouse_trajectory[0][0] / len(self.mouse_trajectory)
            y_force = self.mouse_trajectory[-1][1] - self.mouse_trajectory[0][1] / len(self.mouse_trajectory)
        return x_force, y_force

    def get_mouse_trajectory_list(self):
        return self.mouse_trajectory
    
    def add_mouse_position(self, pos):
        """Add a new mouse position to the trajectory."""
        self.mouse_trajectory.append(pos)
        self.check_mouse_trajectory(60)