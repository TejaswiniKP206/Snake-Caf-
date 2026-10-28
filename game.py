
import pygame
import random

pygame.init()

# Settings
W, H, CELL = 900, 700, 20
COLS, ROWS = 36, 25
X, Y = 90, 150

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Cafe")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 22)
BIG = pygame.font.SysFont("arial", 40, bold=True)
SMALL = pygame.font.SysFont("arial", 16)

# Themes: name, background, board, grid, text, snake, food, button
THEMES = [
    ("SNAKE CAFE", (248, 240, 225), (255, 250, 240),
     (237, 225, 207), (90, 65, 50), (95, 145, 95),
     (190, 80, 75), (220, 195, 165)),

    ("JUNGLE ESCAPE", (28, 55, 42), (38, 75, 52),
     (48, 88, 60), (235, 245, 220), (145, 205, 90),
     (210, 55, 80), (70, 115, 75)),

    ("OCEAN QUEST", (20, 55, 85), (30, 80, 115),
     (42, 95, 130), (235, 250, 255), (70, 180, 190),
     (210, 240, 250), (45, 115, 150)),

    ("DESERT ADVENTURE", (245, 220, 175), (255, 235, 195),
     (235, 205, 160), (100, 65, 40), (220, 155, 75),
     (210, 75, 95), (225, 180, 120)),
]

BEST_FILE = "best_score.txt"

try:
    with open(BEST_FILE, "r") as file:
        best = int(file.read())
except (FileNotFoundError, ValueError):
    best = 0


def text(msg, font, color, pos):
    image = font.render(msg, True, color)
    screen.blit(image, image.get_rect(center=pos))


def button(msg, rect, color, ink):
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, ink, rect, 2, border_radius=8)
    text(msg, SMALL, ink, rect.center)


def make_food(snake):
    while True:
        food = (random.randrange(COLS), random.randrange(ROWS))
        if food not in snake:
            return food


def new_game():
    snake = [(COLS // 2 - i, ROWS // 2) for i in range(3)]
    direction = (1, 0)
    food = make_food(snake)
    return snake, direction, food, 0, "ready"


def draw_food(food, level, color):
    if food is None:
        return

    fx = X + food[0] * CELL + 10
    fy = Y + food[1] * CELL + 10

    if level == 0:  # Cafe cookie
        pygame.draw.circle(screen, (190, 130, 80), (fx, fy), 9)
        for dx, dy in [(-3, -2), (3, 2), (1, -5)]:
            pygame.draw.circle(
                screen, (85, 55, 38), (fx + dx, fy + dy), 2
            )

    elif level == 1:  # Jungle berries
        for dx, dy in [(-4, 2), (4, 2), (0, -4)]:
            pygame.draw.circle(screen, color, (fx + dx, fy + dy), 5)
        pygame.draw.line(
            screen, (100, 160, 65),
            (fx, fy - 5), (fx + 3, fy - 9), 2
        )

    elif level == 2:  # Ocean pearl
        pygame.draw.circle(screen, color, (fx, fy), 9)
        pygame.draw.circle(screen, "white", (fx - 2, fy - 3), 3)

    else:  # Desert fruit
        pygame.draw.ellipse(
            screen, color, (fx - 7, fy - 8, 14, 17)
        )
        pygame.draw.line(
            screen, (90, 135, 65),
            (fx, fy - 7), (fx + 2, fy - 12), 3
        )


def draw_snake(snake, color, direction):
    for i, (sx, sy) in enumerate(snake):
        rect = pygame.Rect(
            X + sx * CELL + 2,
            Y + sy * CELL + 2,
            CELL - 4,
            CELL - 4
        )
        pygame.draw.rect(screen, color, rect, border_radius=7)

        if i == 0:  # Two eyes on the head
            cx, cy = rect.center
            dx, dy = direction

            if dx == 1:
                eyes = [(cx + 4, cy - 4), (cx + 4, cy + 4)]
            elif dx == -1:
                eyes = [(cx - 4, cy - 4), (cx - 4, cy + 4)]
            elif dy == -1:
                eyes = [(cx - 4, cy - 4), (cx + 4, cy - 4)]
            else:
                eyes = [(cx - 4, cy + 4), (cx + 4, cy + 4)]

            for ex, ey in eyes:
                pygame.draw.circle(screen, "white", (ex, ey), 3)
                pygame.draw.circle(
                    screen, "black", (ex + dx, ey + dy), 1
                )


def draw(snake, food, score, state, direction):
    level = min(score // 50, 3)
    name, bg, board, grid, ink, snake_color, food_color, btn = THEMES[level]

    screen.fill(bg)
    text(name, BIG, ink, (W // 2, 38))
    text(
        f"Score: {score}     Best: {best}     Level: {level + 1}",
        FONT, ink, (W // 2, 105)
    )

    start_rect = pygame.Rect(420, 120, 75, 25)
    pause_rect = pygame.Rect(505, 120, 75, 25)
    reset_rect = pygame.Rect(590, 120, 75, 25)

    button("START", start_rect, btn, ink)
    button("PAUSE", pause_rect, btn, ink)
    button("RESET", reset_rect, btn, ink)

    pygame.draw.rect(screen, board, (X, Y, COLS * CELL, ROWS * CELL))

    for x in range(COLS + 1):
        px = X + x * CELL
        pygame.draw.line(screen, grid, (px, Y), (px, Y + ROWS * CELL))

    for y in range(ROWS + 1):
        py = Y + y * CELL
        pygame.draw.line(screen, grid, (X, py), (X + COLS * CELL, py))

    draw_food(food, level, food_color)
    draw_snake(snake, snake_color, direction)

    messages = {
        "ready": "Press an arrow key or START",
        "paused": "PAUSED - Press SPACE to continue",
        "gameover": "GAME OVER - Press R or START",
        "won": "YOU WON! - Press R to play again"
    }

    if state != "playing":
        text(
            messages[state], FONT, ink,
            (W // 2, Y + ROWS * CELL // 2)
        )

    pygame.display.flip()


# Main game
snake, direction, food, score, state = new_game()
move_timer = 0
running = True

keys = {
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0)
}


while running:
    dt = clock.tick(60)
    move_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_r:
                snake, direction, food, score, state = new_game()
                move_timer = 0

            elif event.key == pygame.K_SPACE:
                if state == "playing":
                    state = "paused"
                elif state == "paused":
                    state = "playing"

            elif event.key in keys and state in ("ready", "playing"):
                new_dir = keys[event.key]

                if new_dir != (-direction[0], -direction[1]):
                    direction = new_dir
                    state = "playing"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            if pygame.Rect(420, 120, 75, 25).collidepoint(mx, my):
                if state in ("gameover", "won"):
                    snake, direction, food, score, state = new_game()
                    move_timer = 0
                elif state == "ready":
                    state = "playing"

            elif pygame.Rect(505, 120, 75, 25).collidepoint(mx, my):
                if state == "playing":
                    state = "paused"
                elif state in ("paused", "ready"):
                    state = "playing"

            elif pygame.Rect(590, 120, 75, 25).collidepoint(mx, my):
                snake, direction, food, score, state = new_game()
                move_timer = 0

    # Move the snake
    if state == "playing" and move_timer >= max(65, 120 - (score // 50) * 5):
        move_timer = 0
        hx, hy = snake[0]
        head = (hx + direction[0], hy + direction[1])

        # Wall or self collision
        if (
            head[0] < 0 or head[0] >= COLS
            or head[1] < 0 or head[1] >= ROWS
            or head in snake[:-1]
        ):
            state = "gameover"

        else:
            snake.insert(0, head)

            if head == food:
                score += 10

                if score > best:
                    best = score
                    with open(BEST_FILE, "w") as file:
                        file.write(str(best))

                if len(snake) == COLS * ROWS:
                    food = None
                    state = "won"
                else:
                    food = make_food(snake)

            else:
                snake.pop()

    draw(snake, food, score, state, direction)

pygame.quit()
