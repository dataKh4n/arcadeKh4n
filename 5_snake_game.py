import pygame, sys, random
pygame.init()

WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 50)]
snake_dir = (10, 0)
food = (300, 200)
score = 0

def draw():
    win.fill((0,0,0))
    for s in snake: pygame.draw.rect(win, (0,255,0), (*s,10,10))
    pygame.draw.rect(win, (255,0,0), (*food,10,10))
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: snake_dir = (0,-10)
    if keys[pygame.K_DOWN]: snake_dir = (0,10)
    if keys[pygame.K_LEFT]: snake_dir = (-10,0)
    if keys[pygame.K_RIGHT]: snake_dir = (10,0)
    new_head = (snake[0][0]+snake_dir[0], snake[0][1]+snake_dir[1])
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = (random.randrange(0, WIDTH, 10), random.randrange(0, HEIGHT, 10))
    else:
        snake.pop()
    if new_head[0]<0 or new_head[0]>=WIDTH or new_head[1]<0 or new_head[1]>=HEIGHT or new_head in snake[1:]:
        print(f"Game Over! Score: {score}")
        pygame.quit(); sys.exit()
    draw()
    clock.tick(15)

