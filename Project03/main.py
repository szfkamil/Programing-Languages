import pygame
from pygame.locals import *

def board_init():
    board = [[0 for _ in range(8)] for _ in range(8)]
    return board

def board_draw(board):
    square_size = 120
    for i in range(8):
        for j in range (8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), [300 + square_size * j, 100 + square_size * i, 120, 120], 0)
            elif (i + j) % 2 != 0:
                pygame.draw.rect(screen, (0, 0, 0), [300 + square_size * j, 100 + square_size * i, 120, 120], 0)

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Моє вікно Pygame")
running = True
screen.fill((200,200,240))
board = board_init()
board_draw(board)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()