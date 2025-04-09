import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Enhanced Paint Tool")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, RED, GREEN, BLUE]

current_color = BLACK
brush_size = 5
mode = 'brush'  # 'brush', 'rect', 'circle', 'eraser'
start_pos = None

screen.fill(WHITE)
running = True

# UI Rects
color_buttons = [pygame.Rect(10 + i*50, 10, 40, 40) for i in range(len(COLORS))]
rect_button = pygame.Rect(220, 10, 80, 40)
circle_button = pygame.Rect(310, 10, 80, 40)
eraser_button = pygame.Rect(400, 10, 80, 40)

font = pygame.font.SysFont(None, 24)

def draw_ui():
    for i, rect in enumerate(color_buttons):
        pygame.draw.rect(screen, COLORS[i], rect)
        if COLORS[i] == current_color:
            pygame.draw.rect(screen, WHITE, rect, 2)

    pygame.draw.rect(screen, (200,200,200), rect_button)
    pygame.draw.rect(screen, (200,200,200), circle_button)
    pygame.draw.rect(screen, (200,200,200), eraser_button)
    screen.blit(font.render("Rect", True, BLACK), (rect_button.x + 10, rect_button.y + 10))
    screen.blit(font.render("Circle", True, BLACK), (circle_button.x + 5, circle_button.y + 10))
    screen.blit(font.render("Eraser", True, BLACK), (eraser_button.x + 5, eraser_button.y + 10))

while running:
    clock.tick(200)
    mouse = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check color buttons
                for i, rect in enumerate(color_buttons):
                    if rect.collidepoint(event.pos):
                        current_color = COLORS[i]

                if rect_button.collidepoint(event.pos):
                    mode = 'rect'
                elif circle_button.collidepoint(event.pos):
                    mode = 'circle'
                elif eraser_button.collidepoint(event.pos):
                    mode = 'eraser'
                else:
                    start_pos = event.pos

        if event.type == MOUSEBUTTONUP:
            if start_pos and mode in ['rect', 'circle']:
                end_pos = event.pos
                if mode == 'rect':
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(start_pos[0] - end_pos[0])
                    h = abs(start_pos[1] - end_pos[1])
                    pygame.draw.rect(screen, current_color, (x, y, w, h), brush_size)
                elif mode == 'circle':
                    center = ((start_pos[0]+end_pos[0])//2, (start_pos[1]+end_pos[1])//2)
                    radius = max(abs(start_pos[0]-end_pos[0]), abs(start_pos[1]-end_pos[1]))//2
                    pygame.draw.circle(screen, current_color, center, radius, brush_size)
                start_pos = None

    if pressed[0] and start_pos and mode == 'brush':
        pygame.draw.circle(screen, current_color, mouse, brush_size)
    if pressed[0] and start_pos and mode == 'eraser':
        pygame.draw.circle(screen, WHITE, mouse, brush_size)

    draw_ui()
    pygame.display.flip()

pygame.quit()
