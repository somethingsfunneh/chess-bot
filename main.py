import random
import time
import os

# Chess piece Unicode symbols
PIECES = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
}

class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("  ａ ｂ ｃ ｄ ｅ ｆ ｇ ｈ")
        print(" ┌───────────────────────┐")
        for i, row in enumerate(self.board):
            print(f"{8-i}│", end="")
            for j, piece in enumerate(row):
                if piece == ' ':
                    print("▢ " if (i + j) % 2 == 0 else "▣ ", end="")
                else:
                    print(f"{PIECES[piece]} ", end="")
            print(f"│{8-i}")
        print(" └───────────────────────┘")
        print("  ａ ｂ ｃ ｄ ｅ ｆ ｇ ｈ")

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = ' '

        def is_valid_move(self, start, end, current_player):
            start_row, start_col = start
            end_row, end_col = end
            piece = self.board[start_row][start_col]

            # Check if the piece belongs to the current player
            if (current_player == 'white' and not piece.isupper()) or (current_player == 'black' and not piece.islower()):
                return False

            # Check if the move is within the board
            if not (0 <= end_row < 8 and 0 <= end_col < 8):
                return False

            # Check if the destination is not occupied by a piece of the same color
            if piece.isupper() and self.board[end_row][end_col].isupper():
                return False
            if piece.islower() and self.board[end_row][end_col].islower():
                return False

            # Check for pieces blocking the path
            def is_path_clear(start, end, step_row, step_col):
                row, col = start
                while (row, col) != end:
                    row += step_row
                    col += step_col
                    if (row, col) != end and self.board[row][col] != ' ':
                        return False
                return True

            # Simplified piece movement rules (not considering check, en passant, castling, etc.)
            if piece.lower() == 'p':  # Pawn
                if piece.isupper():  # White pawn
                    if end_col == start_col:
                        if end_row == start_row - 1:
                            return self.board[end_row][end_col] == ' '
                        elif start_row == 6 and end_row == 4:
                            return self.board[5][end_col] == ' ' and self.board[4][end_col] == ' '
                    elif abs(end_col - start_col) == 1 and end_row == start_row - 1:
                        return self.board[end_row][end_col].islower()  # Capture
                else:  # Black pawn
                    if end_col == start_col:
                        if end_row == start_row + 1:
                            return self.board[end_row][end_col] == ' '
                        elif start_row == 1 and end_row == 3:
                            return self.board[2][end_col] == ' ' and self.board[3][end_col] == ' '
                    elif abs(end_col - start_col) == 1 and end_row == start_row + 1:
                        return self.board[end_row][end_col].isupper()  # Capture
                return False
            elif piece.lower() == 'r':  # Rook
                if start_row == end_row:
                    step = 1 if end_col > start_col else -1
                    return is_path_clear(start, end, 0, step)
                elif start_col == end_col:
                    step = 1 if end_row > start_row else -1
                    return is_path_clear(start, end, step, 0)
            elif piece.lower() == 'n':  # Knight
                return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
                       (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)
            elif piece.lower() == 'b':  # Bishop
                if abs(start_row - end_row) == abs(start_col - end_col):
                    step_row = 1 if end_row > start_row else -1
                    step_col = 1 if end_col > start_col else -1
                    return is_path_clear(start, end, step_row, step_col)
            elif piece.lower() == 'q':  # Queen
                if start_row == end_row or start_col == end_col:
                    step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
                    step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)
                    return is_path_clear(start, end, step_row, step_col)
                elif abs(start_row - end_row) == abs(start_col - end_col):
                    step_row = 1 if end_row > start_row else -1
                    step_col = 1 if end_col > start_col else -1
                    return is_path_clear(start, end, step_row, step_col)
            elif piece.lower() == 'k':  # King
                return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

            return False

def parse_move(move_str):
    cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    start = (8 - int(move_str[1]), cols[move_str[0]])
    end = (8 - int(move_str[3]), cols[move_str[2]])
    return start, end

def bot_move(board, elo, bot_color):
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if (bot_color == 'white' and board.board[i][j].isupper()) or (bot_color == 'black' and board.board[i][j].islower()):
                for x in range(8):
                    for y in range(8):
                        if board.is_valid_move((i, j), (x, y), bot_color):
                            valid_moves.append(((i, j), (x, y)))

    if not valid_moves:
        return None

    if elo < 800:
        # Very weak bot: completely random moves
        return random.choice(valid_moves)
    elif elo < 1200:
        # Weak bot: slight preference for captures
        capture_moves = [move for move in valid_moves if board.board[move[1][0]][move[1][1]] != ' ']
        return random.choice(capture_moves) if capture_moves else random.choice(valid_moves)
    elif elo < 1600:
        # Intermediate bot: preference for center control and captures
        center_moves = [move for move in valid_moves if 2 <= move[1][0] <= 5 and 2 <= move[1][1] <= 5]
        capture_moves = [move for move in valid_moves if board.board[move[1][0]][move[1][1]] != ' ']
        preferred_moves = center_moves + capture_moves
        return random.choice(preferred_moves) if preferred_moves else random.choice(valid_moves)
    else:
        # Strong bot: prioritize piece development, center control, and captures
        developed_pieces = ['N', 'B', 'Q', 'K'] if bot_color == 'white' else ['n', 'b', 'q', 'k']
        develop_moves = [move for move in valid_moves if board.board[move[0][0]][move[0][1]] in developed_pieces]
        center_moves = [move for move in valid_moves if 2 <= move[1][0] <= 5 and 2 <= move[1][1] <= 5]
        capture_moves = [move for move in valid_moves if board.board[move[1][0]][move[1][1]] != ' ']
        preferred_moves = develop_moves + center_moves + capture_moves
        return random.choice(preferred_moves) if preferred_moves else random.choice(valid_moves)

def play_chess():
    board = ChessBoard()

    while True:
        player_color = input("Choose your color (white/black): ").lower()
        if player_color in ['white', 'black']:
            break
        print("Invalid choice. Please enter 'white' or 'black'.")

    bot_color = 'black' if player_color == 'white' else 'white'

    while True:
        try:
            bot_elo = int(input("Enter the bot's ELO rating (500-2000): "))
            if 500 <= bot_elo <= 2000:
                break
            print("Invalid ELO. Please enter a number between 500 and 2000.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    current_turn = 'white'

    while True:
        board.display()

        if current_turn == player_color:
            while True:
                move = input(f"{current_turn.capitalize()}'s move (e.g., 'e2e4'): ")
                try:
                    start, end = parse_move(move)
                    if board.is_valid_move(start, end, current_turn):
                        board.move_piece(start, end)
                        break
                    else:
                        print("Invalid move. Try again.")
                except (ValueError, IndexError, KeyError):
                    print("Invalid input. Try again.")
        else:
            print(f"{bot_color.capitalize()} (Bot) is thinking...")
            time.sleep(1)
            bot_move_result = bot_move(board, bot_elo, bot_color)
            if bot_move_result:
                start, end = bot_move_result
                board.move_piece(start, end)
                print(f"{bot_color.capitalize()} (Bot) moved: {chr(start[1] + ord('a'))}{8-start[0]}{chr(end[1] + ord('a'))}{8-end[0]}")
            else:
                print(f"{bot_color.capitalize()} (Bot) has no valid moves.")
                break

        current_turn = 'black' if current_turn == 'white' else 'white'

    print("Game Over")

if __name__ == "__main__":
    play_chess()
