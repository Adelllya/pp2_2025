import pygame
import random
import sys
import psycopg2

conn = psycopg2.connect(
    dbname="game_data",
    user="postgres",
    password="adeliya",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS snake_game (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100),
        best_score INTEGER,
        times INTEGER,
        notes TEXT
    )
""")
cur.execute("SELECT * FROM snake_game")
rows = cur.fetchall()

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
a = input("User: ")
is_user = False
for row in rows:
    if row[1] == a:
        is_user = True
if not is_user:
    cur.execute("""
        INSERT INTO snake_game (username, best_score, times)
        VALUES (%s, %s, %s)
        """, (a, 0, 0))

    
conn.commit()    # print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}, Почта: {row[3]}, Заметка: {row[4]}")

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
    for row in rows:
        if row[1] == a:
            current_best = row[2]
            current_times = row[3]
            if current_best is None:
                current_best = 0
            if current_times is None:
                current_times = 0
            if score > current_best:
                cur.execute("""
                    UPDATE snake_game
                    SET best_score = %s, times = %s
                    WHERE username = %s
                """, (score, current_times + 1, a))
            else:
                cur.execute("""
                    UPDATE snake_game
                    SET times = %s
                    WHERE username = %s
                """, (current_times + 1, a))
            conn.commit()    
            break



    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # скорость зависит от уровня
print("\nТаблица игроков:")
cur.execute("SELECT username, best_score, times FROM snake_game ORDER BY best_score DESC")
players = cur.fetchall()

for i, player in enumerate(players, start=1):
    print(f"{i}. {player[0]} — {player[1]} очков, {player[2]} игр")
pygame.quit()
sys.exit()
conn.commit()


cur.close()
conn.close()