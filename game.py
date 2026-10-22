import math
import random
import pygame
pygame.init()
CELL = 30
COLS, ROWS = 24, 18
TOP = 50  # height of the score bar
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + TOP
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Eat the Apples")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
# ---------- Pre-draw the grass background once ----------
GRASS_1 = (120, 200, 90)
GRASS_2 = (105, 185, 78)
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((40, 55, 40))
for r in range(ROWS):
    for c in range(COLS):
        color = GRASS_1 if (r + c) % 2 == 0 else GRASS_2
        pygame.draw.rect(background, color, (c * CELL, TOP + r * CELL, CELL, CELL))
pygame.draw.rect(background, (30, 40, 30), (0, 0, WIDTH, TOP))  # score bar
pygame.draw.rect(background, (60, 90, 50), (0, TOP, WIDTH, ROWS * CELL), 4)  # border
# ---------- Drawing helpers ----------
def draw_apple(surface, cx, cy, radius):
    # body
    pygame.draw.circle(surface, (220, 30, 40), (cx, cy + 1), radius)
    # shine
    pygame.draw.circle(surface, (255, 140, 140), (cx - radius // 3, cy - radius // 3), max(2, radius // 4))
    # stem
    pygame.draw.line(surface, (110, 70, 30), (cx, cy - radius + 2), (cx + 2, cy - radius - 5), 3)
    # leaf
    pygame.draw.ellipse(surface, (40, 150, 50), (cx + 2, cy - radius - 6, 10, 6))
def cell_center(pos):
    return pos[0] * CELL + CELL // 2, TOP + pos[1] * CELL + CELL // 2
def draw_snake(surface, snake, direction):
    n = len(snake)
    for i in range(n - 1, -1, -1):  # draw tail first, head last
        cx, cy = cell_center(snake[i])
        shade = max(0, 60 - i * 3)
        color = (30 + shade // 3, 120 + shade, 200 + shade // 4)
        rect = pygame.Rect(0, 0, CELL - 4, CELL - 4)
        rect.center = (cx, cy)
        pygame.draw.rect(surface, color, rect, border_radius=10)
    # eyes on the head
    hx, hy = cell_center(snake[0])
    dx, dy = direction
    px, py = -dy, dx  # perpendicular to direction
    for side in (-1, 1):
        ex = hx + dx * 6 + px * 6 * side
        ey = hy + dy * 6 + py * 6 * side
        pygame.draw.circle(surface, (255, 255, 255), (ex, ey), 5)
        pygame.draw.circle(surface, (0, 0, 0), (ex + dx * 2, ey + dy * 2), 2)
def new_food(snake):
    while True:
        pos = (random.randrange(COLS), random.randrange(ROWS))
        if pos not in snake:
            return pos
def reset():
    start = (COLS // 2, ROWS // 2)
    snake = [start, (start[0] - 1, start[1]), (start[0] - 2, start[1])]
    return snake, (1, 0), new_food(snake), 0
# ---------- Game state ----------
snake, direction, food, score = reset()
next_direction = direction
best = 0
game_over = False
speed = 8
running = True
while running:
    # 1. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    snake, direction, food, score = reset()
                    next_direction = direction
                    game_over = False
                    speed = 8
            else:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != (-1, 0):
                    next_direction = (1, 0)
    # 2. Update
    if not game_over:
        direction = next_direction
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if not (0 <= head[0] < COLS and 0 <= head[1] < ROWS) or head in snake:
            game_over = True
            best = max(best, score)
        else:
            snake.insert(0, head)
            if head == food:
                score += 1
                food = new_food(snake)
                speed = min(8 + score // 2, 18)
            else:
                snake.pop()
    # 3. Draw
    screen.blit(background, (0, 0))
    # apple (gently pulsing)
    pulse = int(2 * math.sin(pygame.time.get_ticks() / 200))
    fx, fy = cell_center(food)
    draw_apple(screen, fx, fy, CELL // 2 - 4 + pulse)
    draw_snake(screen, snake, direction)
    # score bar with apple icon
    draw_apple(screen, 30, TOP // 2 + 4, 11)
    screen.blit(font.render(f"x {score}", True, (255, 255, 255)), (50, TOP // 2 - 10))
    best_text = font.render(f"Best: {max(best, score)}", True, (255, 220, 100))
    screen.blit(best_text, (WIDTH - best_text.get_width() - 20, TOP // 2 - 10))
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        title = big_font.render("Game Over", True, (255, 255, 255))
        info = font.render(f"You ate {score} apples  -  Press R to restart", True, (230, 230, 230))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25)))
        screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
    pygame.display.flip()
    clock.tick(speed if not game_over else 30)
pygame.quit()