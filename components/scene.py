from practice_code.body import Body
from practice_code.collision import collide
from .grid import Grid


class Scene:
    def __init__(self, bodies: list[Body], screen_width, screen_height, g_xnum, g_ynum, _grid_on=True, gravity=9.8):
        self.bodies: list[Body] = bodies
        self._contact_points = []
        
        self.gravity = gravity

        #Create the grid
        self.grid = Grid(screen_width, screen_height, g_xnum, g_ynum)
        self.grid_on = _grid_on

    def add(self, body: Body):
        self.bodies.append(body)
    
    def simulate_gravity(self, dt):
        for body in self.bodies:
            if body.is_static == False:
                body.velocity[1] -= self.gravity * body.mass * dt

    def init_box(self):
        for body in self.bodies:
            body.set_box()

    def update_position(self, dt):
        for body in self.bodies:
            if body.is_static == False:
                body.center += body.velocity * dt
                body.angle += body.angular_velocity * dt
                body.set_box()

    def handle_collisions_no_grid(self):
        self._contact_points = []
        for i in range(len(self.bodies) - 1):
            for j in range(i + 1, len(self.bodies)):
                if self.bodies[i] == self.bodies[j]:
                    continue

                contact_points = collide(self.bodies[i], self.bodies[j])
                if contact_points is None:
                    continue

                for point in contact_points:
                    if point is None:
                        continue

                    self._contact_points.append(point)

    def handle_collisions(self):
        self._contact_points = []

        #Assign objects to the grid
        for body in self.bodies:
            self.grid.object_allocation(body)

        #Detect collisions only among objects in the same grid cell
        for x in range(self.grid.x_max + 1):
            for y in range(self.grid.y_max + 1):
                cell_bodies = self.grid.grids[x][y]  #Objects within a single grid cell
                for i in range(len(cell_bodies) - 1):
                    for j in range(i + 1, len(cell_bodies)):
                        if cell_bodies[i] == cell_bodies[j]:
                            continue

                        contact_points = collide(cell_bodies[i], cell_bodies[j])
                        if contact_points is None:
                            continue

                        for point in contact_points:
                            if point is not None:
                                self._contact_points.append(point)
                self.grid.grids[x][y] = [] #Initialize the grid

    def step(self, dt):
        self.simulate_gravity(dt)
        self.update_position(dt)
        if self.grid_on:
            self.handle_collisions()
        else:
            self.handle_collisions_no_grid()
