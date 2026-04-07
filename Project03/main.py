import pygame
import random
import os
import pygame_widgets
from pygame.locals import *
square_size = 120

def pieces_draw():
    for i in range(8):
        for j in range (8):
            if board[i][j] !=0 :
                if board[i][j] == 9:
                    screen.blit(queen_img, (20 + square_size * j + 1/5*square_size, 20 + square_size * i + 1/9*square_size))
                elif board[i][j] == 1:
                    screen.blit(pawn_img, (20 + square_size * j + 1/5*square_size, 20 + square_size * i + 1/9*square_size))

    print(board)

def queen_vision(board, coords_list, queens_quantity):
    directions = [(0,1), (1,0), (1,1), (-1,0), (-1,1), (0,-1), (1,-1), (-1,-1)]
    for q in range(queens_quantity):
        for dr, dc in directions:
            for i in range(1,8):
                check_x, check_y = coords_list[q][1] + dr * i, coords_list[q][0] + dc * i
                if 0 <= check_x < 8 and 0 <= check_y < 8:
                    if board[check_y][check_x] == 1:
                        print(f"The pawn is attacked by queen on square {coords_list[q][1]}, {coords_list[q][0]}")
                        print(f"pawn position: {check_x}, {check_y}")
                        break
                    elif board[check_y][check_x] != 0:
                        break
                else:
                    break


def board_init():
    board = [[0 for _ in range(8)] for _ in range(8)]
    return board

def board_draw():
    for i in range(8):
        for j in range (8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), [20 + square_size * j, 20 + square_size * i, 120, 120], 0)
            elif (i + j) % 2 != 0:
                pygame.draw.rect(screen, (0, 0, 0), [20 + square_size * j, 20 + square_size * i, 120, 120], 0)

def random_pieces_spawn(board):
    os.system('clear')
    k = int(input("How many queens do you want to insert? "))
    y = random.randint(0,7)
    x = random.randint(0,7)
    coords_list = []
    board[y][x] = 1
    for _ in range(k):
        y = random.randint(0,7)
        x = random.randint(0,7)
        while board[y][x] != 0:
            y = random.randint(0,7)
            x = random.randint(0,7)
        board[y][x] = 9
        coords_list.append((y,x)) 
    queen_vision(board, coords_list, k)
    return board

pygame.init()
board = board_init()
board = random_pieces_spawn(board)
screen = pygame.display.set_mode((1000, 1100))
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