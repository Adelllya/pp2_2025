import pygame
import random
import sys


pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20  # Размер клетки сетки
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

#Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE  = (0, 0, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


clock = pygame.time.Clock()
FPS = 3

# Шрифт
font = pygame.font.SysFont('Arial', 24)

# Змейка и еда
snake = [(5, 5)]
direction = (1, 0)  # по умолчанию движение вправо

# Стены (границы по умолчанию)
walls = []

# Функция генерации еды
def generate_food():
    margin = 2  # минимальное расстояние от краёв
    while True:
        x = random.randint(margin, COLS - 1 - margin)
        y = random.randint(margin, ROWS - 1 - margin)
        if (x, y) not in snake and (x, y) not in walls:
            return (x, y)


food = generate_food()

# Уровень и очки
score = 0
level = 1

# Главный цикл игры
running = True
while running:
    screen.fill(BLACK)

    # События (нажатия клавиш)
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            running = False

        # Управление стрелками
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Перемещение змейки
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Проверка на столкновение со стеной или выход за границы
    if (
        new_head[0] < 0 or new_head[0] >= COLS or
        new_head[1] < 0 or new_head[1] >= ROWS or
        new_head in snake or
        new_head in walls
    ):
        print("Game Over")
        running = False

    snake.insert(0, new_head)

    # Если съел еду
    if new_head == food:
        score += 1
        food = generate_food()

        # Повышение уровня каждые 4 очка
        if score % 4 == 0:
            level += 1
            FPS += 2  # увеличение скорости
    else:
        snake.pop()  # иначе удаляем хвост

    # Отрисовка змейки
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка еды
    pygame.draw.rect(screen, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Отрисовка счёта и уровня
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # скорость зависит от уровня

pygame.quit()
sys.exit()
