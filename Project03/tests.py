from chess_logic import (
    board_init, queen_vision, delete_queen, 
    sanitize_input, notation_to_coord
)

# ═════════════════════════════════════════════
# 1. BOARD INITIALIZATION 
# ═════════════════════════════════════════════
class TestBoardInit:
    def test_returns_8x8(self):
        board = board_init()
        assert len(board) == 8
        assert all(len(row) == 8 for row in board)

    def test_all_zeros(self):
        board = board_init()
        assert all(board[i][j] == 0 for i in range(8) for j in range(8))

# ═════════════════════════════════════════════
# 2. QUEEN VISION LOGIC 
# ═════════════════════════════════════════════
class TestQueenVision:
    def test_no_pawn_returns_empty(self):
        board = board_init()
        board[0][0] = 9
        assert queen_vision(board) == []

    def test_queen_attacks_pawn_horizontally(self):
        board = board_init()
        board[4][4] = 1   # pawn e4
        board[4][0] = 9   # queen a4
        assert (4, 0) in queen_vision(board)

    def test_queen_attacks_pawn_vertically(self):
        board = board_init()
        board[4][4] = 1   # pawn
        board[0][4] = 9   # queen on the same column
        assert (0, 4) in queen_vision(board)

    def test_queen_attacks_pawn_diagonally(self):
        board = board_init()
        board[4][4] = 1   # pawn
        board[1][1] = 9   # queen on the diagonal
        assert (1, 1) in queen_vision(board)

    def test_queen_blocked_by_other_queen(self):
        board = board_init()
        board[4][4] = 1   # pawn
        board[4][0] = 9   # queen further away
        board[4][2] = 9   # blocking queen in between
        result = queen_vision(board)
        assert (4, 0) not in result # Queen (4,0) is blocked

    def test_queen_not_attacking_pawn_off_line(self):
        board = board_init()
        board[0][0] = 9
        board[4][3] = 1   # not on any of the queen's lines from (0,0)
        assert queen_vision(board) == []

    def test_all_eight_directions(self):
        # Checks if the queen can attack in all 8 directions
        directions_offsets = [(0, 3), (3, 0), (2, 2), (-2, 0), (-2, 2), (0, -3), (2, -2), (-2, -2)]
        qy, qx = 4, 4
        for dy, dx in directions_offsets:
            board = board_init()
            board[qy][qx] = 9
            py, px = qy + dy, qx + dx
            if 0 <= py < 8 and 0 <= px < 8:
                board[py][px] = 1
                result = queen_vision(board)
                assert (qy, qx) in result

    def test_pawn_surrounded_by_queens(self):
        board = board_init()
        board[4][4] = 1   # pawn in the center
        board[4][6] = 9
        board[4][2] = 9
        board[2][4] = 9
        board[6][4] = 9
        assert len(queen_vision(board)) == 4

# ═════════════════════════════════════════════
# 3. QUEEN DELETION 
# ═════════════════════════════════════════════
class TestDeleteQueen:
    def test_delete_existing_queen(self):
        board = board_init()
        board[0][0] = 9   # queen at a8
        assert delete_queen(board, "a8", notation_to_coord) is True
        assert board[0][0] == 0

    def test_delete_nonexistent_square(self):
        board = board_init()
        assert delete_queen(board, "z9", notation_to_coord) is False

    def test_delete_pawn_square_returns_false(self):
        board = board_init()
        board[4][4] = 1   # pawn
        assert delete_queen(board, "e4", notation_to_coord) is False
        assert board[4][4] == 1  # pawn remains intact

    def test_delete_does_not_affect_other_pieces(self):
        board = board_init()
        board[0][0] = 9
        board[4][4] = 1
        board[7][7] = 9
        delete_queen(board, "a8", notation_to_coord)
        assert board[4][4] == 1
        assert board[7][7] == 9

# ═════════════════════════════════════════════
# 4. INPUT VALIDATION 
# ═════════════════════════════════════════════
class TestSanitizeInput:
    def test_normal_lowercase(self):
        assert sanitize_input("e4") == "e4"

    def test_uppercase_converted(self):
        assert sanitize_input("E4") == "e4"

    def test_reversed_input_digit_first(self):
        assert sanitize_input("4e") == "e4"

# ═════════════════════════════════════════════
# 5. INTEGRATION TESTS
# ═════════════════════════════════════════════
class TestIntegration:
    def test_delete_attacking_queen_clears_attack(self):
        board = board_init()
        board[4][4] = 1   # pawn e4
        board[4][0] = 9   # queen a4 attacks
        assert (4, 0) in queen_vision(board)
        delete_queen(board, "a4", notation_to_coord)
        assert queen_vision(board) == []

    def test_delete_blocker_exposes_far_queen(self):
        board = board_init()
        board[4][4] = 1   # pawn
        board[4][2] = 9   # blocker 
        board[4][0] = 9   # further queen
        assert (4, 0) not in queen_vision(board) # blocker obstructs the view
        delete_queen(board, "c4", notation_to_coord) # remove the blocker
        assert (4, 0) in queen_vision(board) # further queen now attacks

    def test_full_scenario_spawn_and_check(self):
        board = board_init()
        board[0][0] = 9   # queen a8
        board[7][6] = 1   # pawn g1 
        assert queen_vision(board) == []
        board[7][0] = 9   # queen a1 (horizontal attack)
        assert (7, 0) in queen_vision(board)
        delete_queen(board, "a1", notation_to_coord)
        assert (7, 0) not in queen_vision(board) # Verify that the attack is cleared after removal