import pygame
import math
import random

pygame.init()

# -----------------------------------------------
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# -----------------------------------------------
BG_COLOR = (0, 180, 255)
BLOB_COLOR = (0, 50, 150)
SNAKE_COLOR = (50, 200, 50)
OUTLINE_COLOR = (0, 100, 0)
EYE_COLOR = (0, 0, 0)
ARROW_COLOR = (200, 50, 50)
JOYSTICK_BG = (200, 200, 200)
JOYSTICK_FG = (100, 100, 100)

# -----------------------------------------------
tail_length = 50
snake_radius = 15
snake_speed = 4
snake_segments = [[WIDTH//2, HEIGHT//2]] * tail_length
current_angle = 5

# -----------------------------------------------
joystick_center = (100, HEIGHT-100)
joystick_radius = 70
stick_pos = list(joystick_center)
stick_radius = 30

# -----------------------------------------------
bg_circles = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(5, 15)) for _ in range(50)]

clock = pygame.time.Clock()
running = True

while running:
  # bg
  screen.fill(BG_COLOR)
  for x, y, r in bg_circles:
    pygame.draw.circle(screen, BLOB_COLOR, (x, y), r)
    
  pygame.draw.circle(screen, JOYSTICK_BG, joystick_center, joystick_radius)
  pygame.draw.circle(screen, JOYSTICK_FG, stick_pos, stick_radius)
    
  dx = stick_pos[0] - joystick_center[0]
  dy = stick_pos[1] - joystick_center[1]
  magnitude = min(math.hypot(dx, dy)/joystick_radius, 1)
  if magnitude > 0.1:
    current_angle = math.atan2(dy, dx)
  move_x = math.cos(current_angle) * snake_speed
  move_y = math.sin(current_angle) * snake_speed
  new_head = [snake_segments[0][0] + move_x, snake_segments[0][1] + move_y]
  
  if (new_head[0] - snake_radius <= 0 or
    new_head[0] + snake_radius >= WIDTH or
    new_head[1] - snake_radius <= 0 or
    new_head[1] + snake_radius >= HEIGHT):
    print("Game Over! Snake hit the wall! :'(")
    running = False
    continue
  
  snake_segments = [new_head] + snake_segments[:-1]
  
  
  
  outline_thickness = int(snake_radius / 2.5)
  for i, seg in enumerate(snake_segments):
    radius = snake_radius
    pygame.draw.circle(screen, OUTLINE_COLOR, (int(seg[0]), int(seg[1])), radius + outline_thickness)
  for i, seg in enumerate(snake_segments):
    pygame.draw.circle(screen, SNAKE_COLOR, (int(seg[0]), int(seg[1])), snake_radius)
  
  arrow_dist = snake_radius * 20 
  arrow_size = 20
  arrow_x = snake_segments[0][0] + math.cos(current_angle) * (arrow_dist + arrow_size)
  arrow_y = snake_segments[0][1] + math.sin(current_angle) * (arrow_dist + arrow_size)
  points = [
    (arrow_x, arrow_y),
    (arrow_x - arrow_size*math.cos(current_angle - math.pi/6), arrow_y - arrow_size*math.sin(current_angle - math.pi/6)),
    (arrow_x - arrow_size*math.cos(current_angle + math.pi/6), arrow_y - arrow_size*math.sin(current_angle + math.pi/6))
  ]
  pygame.draw.polygon(screen, ARROW_COLOR, points)
  
  eye_offset = snake_radius * 0.5
  eye_radius = 3.5
  eye_dx = math.cos(current_angle + math.pi/2) * eye_offset
  eye_dy = math.sin(current_angle + math.pi/2) * eye_offset
  pygame.draw.circle(screen, EYE_COLOR, (int(snake_segments[0][0] + eye_dx), int(snake_segments[0][1] + eye_dy)), eye_radius)
  pygame.draw.circle(screen, EYE_COLOR, (int(snake_segments[0][0] - eye_dx), int(snake_segments[0][1] - eye_dy)), eye_radius)
  
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
      mx, my = pygame.mouse.get_pos()
      dx = mx - joystick_center[0]
      dy = my - joystick_center[1]
      dist = math.hypot(dx, dy)
      if dist < joystick_radius:
        stick_pos = [mx, my]
      else:
        angle_clamp = math.atan2(dy, dx)
        stick_pos = [
          joystick_center[0] + math.cos(angle_clamp) * joystick_radius,
          joystick_center[1] + math.sin(angle_clamp) * joystick_radius
        ]
    elif event.type == pygame.MOUSEBUTTONUP:
      stick_pos = list(joystick_center)
  
  pygame.display.flip()
  clock.tick(60)

pygame.quit()
  
    