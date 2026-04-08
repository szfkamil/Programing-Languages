import pygame
import random
import os
import pygame_widgets as pw
import pygame_gui
from pygame_widgets.button import Button
from pygame.locals import *

# Списки для літер та цифр
files = "abcdefgh"
ranks = "87654321"  # Рядок 0 у масиві — це 8-й ряд шахівниці

# Створюємо словник {(row, col): "notation"}
coord_to_notation = {
    (r, c): files[c] + ranks[r] 
    for r in range(8) 
    for c in range(8)
}

square_size = 120
coords_list = []

def pieces_draw():
    for i in range(8):
        for j in range (8):
            if board[i][j] !=0 :
                if board[i][j] == 9:
                    screen.blit(queen_img, (20 + square_size * j + 1/5*square_size, 20 + square_size * i + 1/9*square_size))
                elif board[i][j] == 1:
                    screen.blit(pawn_img, (20 + square_size * j + 1/5*square_size, 20 + square_size * i + 1/9*square_size))

def queen_vision(board, coords_list, queens_quantity):
    directions = [(0,1), (1,0), (1,1), (-1,0), (-1,1), (0,-1), (1,-1), (-1,-1)]
    for q in range(queens_quantity):
        for dr, dc in directions:
            for i in range(1,8):
                check_x, check_y = coords_list[q][1] + dr * i, coords_list[q][0] + dc * i
                if 0 <= check_x < 8 and 0 <= check_y < 8:
                    if board[check_y][check_x] == 1:
                        print(f"The pawn is attacked by queen on square {coords_list[q][1]}, {coords_list[q][0]}")
                        break
                    elif board[check_y][check_x] != 0:
                        break
                else:
                    break
def delete_queen(board):
    return board
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

def random_pieces_spawn(board,conf):
    if conf == 0:
        for i in range(8):
            for j in range (8):
                    if board[i][j] == 1:
                        board[i][j] = 0
    os.system('clear')
    y = random.randint(0,7)
    x = random.randint(0,7)
    while board[y][x] != 0:
            y = random.randint(0,7)
            x = random.randint(0,7)
    board[y][x] = 1
    if conf == 1:
        k = int(input("How many queens do you want to insert? "))
        for _ in range(k):
            y = random.randint(0,7)
            x = random.randint(0,7)
            while board[y][x] != 0:
                y = random.randint(0,7)
                x = random.randint(0,7)
            board[y][x] = 9
            coords_list.append((y,x)) 
    if conf == 2:
        pass
    queen_vision(board, coords_list, len(coords_list))
    return board

#Pygame display settings and board initialisation
pygame.init()
board = board_init()
board = random_pieces_spawn(board,1)
HEIGHT = 1200
WIDTH = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
pygame.display.set_caption("Window")
##Images download block
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

#UI ELEMENTS
button1 = Button(
    screen, 100, 1000, 300, 80, text='New pawn position',
    fontSize=28, margin=20,
    inactiveColour=(59, 89, 152),
    pressedColour=(59, 89, 152), radius=20,
    onClick = lambda: random_pieces_spawn(board,0)
)

button2 = Button(
    screen, 600, 1000, 300, 80, text='Delete a queen',
    fontSize=28, margin=20,
    inactiveColour=(59, 89, 152),
    pressedColour=(59, 89, 152), radius=20,
    onClick = lambda: random_pieces_spawn(board,2)
)
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH - WIDTH*5/6,HEIGHT - 80), (650, 50), manager = MANAGER, object_id = "#Text_input"))
#Pygame running segment 
while running:
    UI_REFRESH_RATE = CLOCK.tick(60)/1000
    screen.fill((200,200,240))
    board_draw()
    pieces_draw()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        MANAGER.process_events(event)
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#Text_input":
            pass
    MANAGER.update(UI_REFRESH_RATE)
    MANAGER.draw_ui(screen)
    pw.update(events)
    pygame.display.flip()
pygame.quit()