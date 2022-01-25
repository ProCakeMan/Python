import sys, pygame
import time
from pygame.math import Vector2
pygame.init()

# Initializes the font and creates a font with font size 15
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 15)


# Sets screen size and creates screen
size = width, height = 640, 480
screen = pygame.display.set_mode(size)


# Buttons
showPosBtn = pygame.Rect(20, 420, 80, 30) # Shows position of points
incrPointsBtn = pygame.Rect(120, 420, 80, 30) # Increases points
dcrPointsBtn = pygame.Rect(120, 380, 80, 30) # Decreases points


# Creates the points
pointA = Vector2(100, 100) # Start point
points = list(map(Vector2, [(pointA.x, pointA.y), (pointA.x + 100, pointA.y)])) # Creates a list of Vector2s with point coordinates
points.append((pointA.x + 200, pointA.y)) # Appends point 2
target = Vector2(450, 300)
rel_points = []
angles = []
max_angle = 360 # Adjust for limited angles


mouse = pygame.mouse.get_pos()
showPos = False


for i in range(1, len(points)):
    rel_points.append(points[i] - points[i-1])
    angles.append(0)

def solve_ik(i, endpoint, target):
    if i < len(points) - 2:
        endpoint = solve_ik(i+1, endpoint, target)
    current_point = points[i]

    angle = (endpoint-current_point).angle_to(target-current_point)
    angles[i] += min(max(-3, angle), 3)
    angles[i] = min(max(180-max_angle, (angles[i]+180)%360), 180+max_angle)-180

    return current_point + (endpoint-current_point).rotate(angle)

def render():
    # Color
    black = 0, 0, 0
    white = 255, 255, 255

    screen.fill(white)

    for i in range(1, len(points)):
        prev = points[i-1]
        cur = points[i]
        pygame.draw.aaline(screen, black, prev, cur) # Draws a line between points
    for point in points:
        pygame.draw.circle(screen, black, (int(point[0]), int(point[1])), 5) # Draws points
        if showPos:
            screen.blit(myfont.render(str(point), 100, 100), (point.x, point.y)) # Blits text that shows the position of the points

    screen.blit(myfont.render("Points: " + str(len(points)), 100, 100), (10, 10)) # Blits text that shows amount of points

    # Buttons
    pygame.draw.rect(screen, (120, 120, 120), showPosBtn)
    pygame.draw.rect(screen, (120, 255, 120), incrPointsBtn)
    pygame.draw.rect(screen, (255, 120, 120), dcrPointsBtn)

    pygame.draw.circle(screen, black, (int(target[0]), int(target[1])), 10) # Draws target point
    pygame.display.flip()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit() # Quits game
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if showPosBtn.collidepoint(event.pos): # Enables the show position feature
                    if not showPos:
                        showPos = True   
                    else:
                        showPos = False
                if incrPointsBtn.collidepoint(event.pos): # Increases points
                    difference = points[len(points) - 1] - points[len(points) - 2]
                    print(difference)
                    points.append(points[len(points) - 1] + difference)
                    for i in range(1, len(points)):
                        rel_points.append(points[i] - points[i-1])
                        angles.append(0)
                if dcrPointsBtn.collidepoint(event.pos): # Decreases points
                    p = points[len(points) - 1]
                    points.remove(p)
                    for i in range(1, len(points)):
                        rel_points.append(points[i] - points[i-1])
                        angles.append(0)
    
    solve_ik(0, points[-1], target)

    angle = 0
    for i in range(1, len(points)):
        angle += angles[i-1]
        points[i] = points[i-1] + rel_points[i-1].rotate(angle)

    target = pygame.mouse.get_pos()

    render()
    pygame.time.wait(int(1000/60))
