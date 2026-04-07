import pygame
import random
import os
from pygame.locals import *
square_size = 120

def pieces_draw():
    for i in range(8):
        for j in range (8):
            if board[i][j] !=0 :
                if board[i][j] == 9:
                    screen.blit(queen_img, (300 + square_size * j + 1/5*square_size, 100 + square_size * i + 1/9*square_size))
                elif board[i][j] == 1:
                    screen.blit(pawn_img, (300 + square_size * j + 1/5*square_size, 100 + square_size * i + 1/9*square_size))
                    pass

    print(board)


def board_init():
    board = [[0 for _ in range(8)] for _ in range(8)]
    return board

def board_draw():
    for i in range(8):
        for j in range (8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), [300 + square_size * j, 100 + square_size * i, 120, 120], 0)
            elif (i + j) % 2 != 0:
                pygame.draw.rect(screen, (0, 0, 0), [300 + square_size * j, 100 + square_size * i, 120, 120], 0)

def random_pieces_spawn(board):
    os.system('clear')
    random.randint(0,7)
    k = int(input("How many queens do you want to insert? "))
    for i in range(k):
        y = random.randint(0,7)
        x = random.randint(0,7)
        if board[y][x] == 0:
            board[y][x] = 9
    y = random.randint(0,7)
    x = random.randint(0,7)
    if board[y][x] == 0:
        board[y][x] = 1
    return board

pygame.init()
board = board_init()
board = random_pieces_spawn(board)
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Window")

try:
    queen_img = pygame.image.load("sprites/white/queen.png")
    queen_img = pygame.transform.scale(queen_img, (72, 96))
    pawn_img = pygame.image.load("sprites/white/pawn.png")
    pawn_img = pygame.transform.scale(pawn_img, (72, 96))
except pygame.error:
    print("Download of pictures cancelled")
    pygame.quit()
    exit()

running = True
screen.fill((200,200,240))
board_draw()
pieces_draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()