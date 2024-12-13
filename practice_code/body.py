import math
from components.vector import Vector2D


class Body():
    def __init__(self, x, y, mass = 1, bounce = 0.5, name = None, is_static = False):
        self.center = Vector2D(x, y)
        self.angle = 0    
        self.name = name
        self.shape_type = None
        self.velocity = Vector2D(0, 0)
        self.angular_velocity = 0#
        
        
        self.inertia = None#
        self.mass = mass if not is_static else float("inf") #
        self.bounce = bounce #
        self.is_static = is_static#

        self.box = [] #AABB bounding volume. xmin, ymin, xmax, ymax.

    def set_box(self):
        pass

class Rectangle(Body):
    def __init__(self, x, y, width, height, mass = 1, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, bounce, name, is_static)
        self.width = width
        self.height = height
        self.shape_type = "Polygon"
        half_width = self.width / 2
        half_height = self.height / 2

        self.local_vertices = [
            Vector2D(-half_width, -half_height),
            Vector2D(half_width, -half_height),
            Vector2D(half_width, half_height),
            Vector2D(-half_width, half_height)
        ]
        #
        self.inertia = (1 / 12) * mass * (width * width + height * height) if not is_static else float("inf")
        
    
    def get_axes(self):
        self.x_axis = Vector2D(math.cos(self.angle), math.sin(self.angle))
        self.y_axis = Vector2D(-math.sin(self.angle), math.cos(self.angle)) 
        
        return [self.x_axis, self.y_axis] 

    def get_vertices(self):
        return [vertex.rotate(self.angle).add(self.center) for vertex in self.local_vertices]

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

    def set_box(self):
        vertices = self.get_vertices()
        min_x = min(vertex.x for vertex in vertices)
        min_y = min(vertex.y for vertex in vertices)
        max_x = max(vertex.x for vertex in vertices)
        max_y = max(vertex.y for vertex in vertices)

        self.box = [min_x, min_y, max_x, max_y]



class Polygon(Body):
    def __init__(self, x, y, vertices: list[Vector2D, list, tuple], mass=1, bounce=0.5, name=None, is_static=False):
        super().__init__(x, y, mass, bounce, name, is_static)
        centroid = (
            sum(vertex[0] for vertex in vertices) / len(vertices),
            sum(vertex[1] for vertex in vertices) / len(vertices),
        )

        self.local_vertices = [Vector2D(vertex[0] - centroid[0], vertex[1] - centroid[1]) for vertex in vertices]
      
        self.shape_type = "Polygon"
        self.inertia = self.calculate_inertia() if not is_static else float("inf")#
    
    
    def get_vertices(self):
        return [vertex.rotate(self.angle).add(self.center) for vertex in self.local_vertices]
    
    def calculate_inertia(self):
        # Initialize variables
        area = 0
        center = Vector2D(0, 0)
        mmoi = 0

        # Set the last vertex as the initial previous vertex
        prev = len(self.local_vertices) - 1

        # Iterate through each edge of the polygon
        for index in range(len(self.local_vertices)):
            a = self.local_vertices[prev]  # Previous vertex
            b = self.local_vertices[index]  # Current vertex

            # Calculate the area of the triangle formed by the edge
            area_step = a.cross(b) / 2

            # Calculate the centroid of the triangle
            center_step = (a+b) / 3

            # Calculate the ""moment of inertia"" for the triangle
            mmoi_step = area_step * (a.dot(a) + b.dot(b) + a.dot(b)) / 6

            # Update the centroid considering the new triangle
            center = (center * area + center_step * area_step) / (area + area_step) 

            # Accumulate the area and moment of inertia 갱신하고
            area += area_step 
            mmoi += mmoi_step  

            # Move to the next edge
            prev = index

        # Calculate the density of the polygon
        density = self.mass / area  

        # Adjust the moment of inertia with the density
        mmoi *= density 

        # Apply the parallel axis theorem to adjust for the centroid
        mmoi -= self.mass * center.dot(center)

        # Return the final moment of inertia
        return mmoi


    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

    def set_box(self):
        vertices = self.get_vertices()
        min_x = min(vertex.x for vertex in vertices)
        min_y = min(vertex.y for vertex in vertices)
        max_x = max(vertex.x for vertex in vertices)
        max_y = max(vertex.y for vertex in vertices)

        self.box = [min_x, min_y, max_x, max_y]

class Circle(Body):
    def __init__(self, x, y, radius, mass = 1, bounce = 0.5, name = None, is_static = False):
        super().__init__(x, y, mass, bounce, name, is_static)
        self.radius = radius
        self.shape_type = "Circle"
        self.inertia = (1 / 2) * mass * radius * radius if not is_static else float("inf")

    def rotate(self, angle, in_radians=True):
        if not in_radians:
            angle = math.radians(angle)
        self.angle += angle

    def set_box(self):
        self.box = [self.center.x - self.radius,
                    self.center.y - self.radius,
                    self.center.x + self.radius,
                    self.center.y + self.radius]

