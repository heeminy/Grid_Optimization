import pygame
import sys
import random
import time

import constants as c
from practice_code.body import Body, Circle, Rectangle, Polygon
from components.scene import Scene
import test1
import test2


# Set test mode
mode = 2 #if mode==1 : execute test1 , elif mode == 2 : execute test2
use_grid = True


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Grid Optimization Test")


#for test
def add_random_rectangles(scene, n):
    """Add n rectangles at random positions on the screen"""
    for _ in range(n):
        rand_x = random.randint(0, c.WIDTH)
        rand_y = random.randint(0, c.HEIGHT)

        new_rect = Rectangle(
            x=rand_x,
            y=rand_y,
            width=10,
            height=10,
            mass=50
        )
        scene.add(new_rect)

#set objects
if mode == 1:
    objs = test1.test1_objs
    player = test1.player
elif mode == 2:
    objs = test2.test2_objs
    player = test2.player
    

Scene = Scene(
    objs,
    c.WIDTH,
    c.HEIGHT,
    c.X_GRID,
    c.Y_GRID,
    use_grid,
    c.GRAVITY
)

#for test
n_random_rects = 30
add_random_rectangles(Scene, n_random_rects)


move_left = False
move_right = False
move_up = False
move_down = False
dt = 1 / c.FPS

if use_grid:
    Scene.init_box()

prev_time = time.time()
sec_count = 0
real_fps = 0
avg_fps = 0

# Main game loop
while True:
    timer = time.time() - prev_time
    real_fps += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_UP:
                move_up = True
            elif event.key == pygame.K_DOWN:
                move_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_UP:
                move_up = False
            elif event.key == pygame.K_DOWN:
                move_down = False

    if move_left:
        player.velocity[0] -= c.PLAYER_SPEED_X
    if move_right:
        player.velocity[0] += c.PLAYER_SPEED_X
    if move_up:
        player.velocity[1] += c.PLAYER_SPEED_Y
    if move_down:
        player.velocity[1] -= c.PLAYER_SPEED_Y

    Scene.step(dt)
    screen.fill(c.COLORS["white"])

    for body in Scene.bodies:
        if body.name == "Player":
            color = c.COLORS["red"]
        else : 
            color = c.COLORS["black"]

        if body.shape_type == "Polygon":
            
            pygame.draw.polygon(
                screen,
                color,
                [(vertex.x, c.HEIGHT - vertex.y) for vertex in body.get_vertices()],
            )
        elif body.shape_type == "Circle":
            color = c.COLORS["cyan"]
            pygame.draw.circle(
                screen, color, (body.center[0], c.HEIGHT - body.center[1]), body.radius
            )
        elif body.shape_type == "Rectangle":
            pygame.draw.rect(
                screen,
                c.COLORS["black"],
                pygame.Rect(body.center[0], c.HEIGHT - body.center[1], body.width, body.height)
            )
            
    for point in Scene._contact_points:
        pygame.draw.circle(screen, c.COLORS["green"], (point.x, c.HEIGHT - point.y), 4)

    if (timer >= 1): #for print FPS
        sec_count += 1
        print (str(sec_count) + " sec . . . FPS : " + str(real_fps))
        prev_time = time.time()
        timer = 0
        avg_fps += real_fps
        real_fps = 0
        if (sec_count == 20):
            print ("avarage FPS (0~20sec) : " + str(avg_fps / 20))


    pygame.display.flip()

    pygame.time.Clock().tick(c.FPS)
