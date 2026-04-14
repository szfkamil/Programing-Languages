import pygame
import os
import pygame_gui
import pygame_widgets as pw
from pygame_widgets.button import Button


from chess_logic import (
    sanitize_input, 
    notation_to_coord, 
    coord_to_notation, 
    files, 
    ranks,
    board_init,          
    queen_vision,         
    delete_queen,         
    random_pieces_spawn   
)

square_size = 120
attacking_queens = []

def pieces_draw():
    for i in range(8):
        for j in range(8):
            if board[i][j] != 0:
                if (i, j) in attacking_queens:
                    pygame.draw.rect(screen, (255, 0, 0), [20 + square_size * j, 20 + square_size * i, 120, 120], 5)
                
                if board[i][j] == 9:
                    screen.blit(queen_img, (20 + square_size * j + 1/5*square_size, 20 + square_size * i + 1/9*square_size))
                elif board[i][j] == 1:
                    screen.blit(pawn_img, (20 + square_size * j + 1/5*square_size, 20 + square_size * i + 1/9*square_size))

def print_attack_status():
    if not attacking_queens:
        print("No capture detected. Pawn is safe.")
    else:
        positions = [coord_to_notation[(y, x)] for y, x in attacking_queens]
        print(f"WARNING! Pawn under attack. Attacking queens: {', '.join(positions)}")

def handle_delete_queen_button():
    global attacking_queens
    
    raw_text = TEXT_INPUT.get_text()
    final_text = sanitize_input(raw_text) # Using function from chess_logic
    
    success = delete_queen(board, final_text, notation_to_coord)
    
    if success:
        print(f"Removed queen from square {final_text}")
        attacking_queens = queen_vision(board) 
        print_attack_status()
    else:
        print(f"Rejected! Invalid square: '{final_text}' or no queen present.")
        
    TEXT_INPUT.set_text("")

def handle_new_pawn():
    """Helper function for the button, updating the UI state after rolling."""
    global attacking_queens
    random_pieces_spawn(board, 0)
    attacking_queens = queen_vision(board)
    print_attack_status()

def board_draw(font, text_col):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, (255, 255, 255), [20 + square_size * j, 20 + square_size * i, square_size, square_size], 0)
            else:
                pygame.draw.rect(screen, (0, 0, 0), [20 + square_size * j, 20 + square_size * i, square_size, square_size], 0)
            
            if i == 7:
                text = font.render(files[j], True, text_col)
                screen.blit(text, (120 + square_size * j, 110 + square_size * i))
            if j == 0:
                text = font.render(ranks[i], True, text_col)
                screen.blit(text, (25 + square_size * j, 25 + square_size * i))


# ═════════════════════════════════════════════
# MAIN GAME LOOP
# ═════════════════════════════════════════════
if __name__ == '__main__':
    pygame.init()
    text_font = pygame.font.SysFont("Arial", 24, True, False)
    
    # Board state initialization
    board = board_init()
    random_pieces_spawn(board, 1)
    attacking_queens = queen_vision(board)

    HEIGHT = 1200
    WIDTH = 1000
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
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
    screen.fill((200, 200, 240))

    button1 = Button(
        screen, 100, 1000, 300, 80, text='New pawn position',
        fontSize=28, margin=20,
        inactiveColour=(59, 89, 152),
        pressedColour=(59, 89, 152), radius=20,
        onClick=handle_new_pawn
    )
    
    button2 = Button(
        screen, 600, 1000, 300, 80, text='Delete a queen',
        fontSize=28, margin=20,
        inactiveColour=(59, 89, 152),
        pressedColour=(59, 89, 152), radius=20,
        onClick=handle_delete_queen_button
    )
    
    TEXT_INPUT = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((int(WIDTH - WIDTH*5/6), int(HEIGHT - 80)), (650, 50)),
        manager=MANAGER,
        object_id="#txt_input"
    )

    print_attack_status()

    while running:
        UI_REFRESH_RATE = CLOCK.tick(60) / 1000
        screen.fill((200, 200, 240))
        
        board_draw(text_font, (0, 112, 99))
        pieces_draw()
        
        events = pygame.event.get()
        for event in events:
            MANAGER.process_events(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == TEXT_INPUT:
                handle_delete_queen_button()

        MANAGER.update(UI_REFRESH_RATE)
        MANAGER.draw_ui(screen)
        pw.update(events)
        pygame.display.update()

    pygame.quit()