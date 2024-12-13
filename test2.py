import constants as c
from practice_code.body import Body, Circle, Rectangle, Polygon

player = Rectangle(
    x=30,
    y=600,
    width=25,
    height=25,
    name="Player",
    mass=50,
)

platform_1 = Rectangle(
    x=150, y=500, width=300, height=50, is_static=True, bounce=0.8
)

platform_2 = Rectangle(
    x=550, y=375, width=400, height=50, is_static=True, bounce=0.8
)

platform_3 = Rectangle(
    x=200, y=250, width=400, height=50, is_static=True, bounce=0.8
)

platform_4 = Rectangle(
    x=675, y=250, width=125, height=50, is_static=True, bounce=0.8
)

platform_5 = Rectangle(
    x=c.WIDTH/2, y=50, width=c.WIDTH, height=100, is_static=True, bounce=0.8
)

test2_objs =[
        player,
        platform_1,
        platform_2,
        platform_3,
        platform_4,
        platform_5,
    ]