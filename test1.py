import constants as c
from practice_code.body import Body, Circle, Rectangle, Polygon

player = Rectangle(
    x=450,
    y=250,
    width=25,
    height=25,
    name="Player",
    mass=50,
)

rectangle_2 = Rectangle(
    x=200,
    y=250,
    width=50,
    height=50,
    mass=100,
)

circle_1 = Circle(
    x=400,
    y=200,
    radius=10,
    mass=30,
)

circle_2 = Circle(x=c.WIDTH / 2 + 200, y=300, radius=25, mass=120, is_static=False)

polygon_1 = Polygon(
    x=310,
    y=250,
    vertices=[(0, 0), (50, 0), (50, 25), (0, 50)],
    mass=100,
)

polygon_1.rotate(90, in_radians=False)

rectangle_3 = Rectangle(
    x=c.WIDTH / 2,
    y=100,
    width=c.WIDTH / 1.5,
    height=20,
    is_static=True,
    bounce=0.7,
    name="Ground"
)

platform_1 = Rectangle(
    x=600, y=300, width=200, height=20, is_static=True, bounce=0.8
)

platform_1.rotate(30, in_radians=False)

platform_2 = Rectangle(
    x=70, y=200, height=20, width=200, is_static=True, bounce=0.8
)

platform_2.rotate(-60, in_radians=False)

test1_objs =[
        player,
        rectangle_2,
        rectangle_3,
        circle_1,
        circle_2,
        polygon_1,
        platform_1,
        platform_2,
    ]