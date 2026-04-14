import random

# ─────────────────────────────────────────────
# Dictionaries and constants
# ─────────────────────────────────────────────
files = "abcdefgh"
ranks = "87654321"

notation_to_coord = {
    files[c] + ranks[r]: (r, c)
    for r in range(8)
    for c in range(8)
}

coord_to_notation = {v: k for k, v in notation_to_coord.items()}

# ─────────────────────────────────────────────
# Logical Functions (No Pygame)
# ─────────────────────────────────────────────

def board_init():
    """Returns an empty 8x8 board filled with zeros."""
    return [[0 for _ in range(8)] for _ in range(8)]


def queen_vision(board):
    """
    Checks if any queens can attack the pawn.
    Returns a list of coordinates (y, x) of the attacking queens.
    """
    queens = []
    pawn_pos = None
    for i in range(8):
        for j in range(8):
            if board[i][j] == 9:
                queens.append((i, j))
            elif board[i][j] == 1:
                pawn_pos = (i, j)

    if not pawn_pos:
        return []

    attacking = []
    directions = [(0, 1), (1, 0), (1, 1), (-1, 0), (-1, 1), (0, -1), (1, -1), (-1, -1)]

    for qy, qx in queens:
        for dr, dc in directions:
            attack_found = False
            for step in range(1, 8):
                check_y, check_x = qy + dr * step, qx + dc * step
                if 0 <= check_y < 8 and 0 <= check_x < 8:
                    if board[check_y][check_x] == 1:
                        attacking.append((qy, qx))
                        attack_found = True
                        break
                    elif board[check_y][check_x] == 9:
                        break
                else:
                    break
            if attack_found:
                break

    return attacking


def delete_queen(board, chosen_square, notation_dict):
    """
    Removes a queen from the specified square.
    Returns True if a queen was removed, False otherwise.
    """
    if chosen_square not in notation_dict:
        return False
        
    y, x = notation_dict[chosen_square]
    if board[y][x] == 9:
        board[y][x] = 0
        return True
    return False


def sanitize_input(raw_text):
    """
    Cleans and formats user input (e.g., ' E4 ' -> 'e4', '4e' -> 'e4').
    """
    clean_text = raw_text.strip().lower()
    if len(clean_text) == 2 and clean_text[0].isdigit() and clean_text[1].isalpha():
        return clean_text[1] + clean_text[0]
    return clean_text


def random_pieces_spawn(board, conf):
    """
    Randomizes pawn position (conf=0) and optionally queens (conf=1).
    Returns the modified board. Does not modify global variables.
    """
    if conf == 0:
        for i in range(8):
            for j in range(8):
                if board[i][j] == 1:
                    board[i][j] = 0
                    
    y = random.randint(0, 7)
    x = random.randint(0, 7)
    while board[y][x] != 0:
        y = random.randint(0, 7)
        x = random.randint(0, 7)
    board[y][x] = 1
    
    if conf == 1:
        k = random.randint(1, 5) 
        for _ in range(k):
            y = random.randint(0, 7)
            x = random.randint(0, 7)
            while board[y][x] != 0:
                y = random.randint(0, 7)
                x = random.randint(0, 7)
            board[y][x] = 9
            
    return board