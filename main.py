import random
import os
import time

# Chess pieces
class ChessPiece:
    def __init__(self, color):
        self.color = color

class Pawn(ChessPiece):
    def __str__(self):
        return '♙' if self.color == 'white' else '♟'

class Rook(ChessPiece):
    def __str__(self):
        return '♖' if self.color == 'white' else '♜'

class Knight(ChessPiece):
    def __str__(self):
        return '♘' if self.color == 'white' else '♞'

class Bishop(ChessPiece):
    def __str__(self):
        return '♗' if self.color == 'white' else '♝'

class Queen(ChessPiece):
    def __str__(self):
        return '♕' if self.color == 'white' else '♛'

class King(ChessPiece):
    def __str__(self):
        return '♔' if self.color == 'white' else '♚'

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.move_history = []
        self.setup_board()

    def setup_board(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = Pawn('white')
            self.board[6][col] = Pawn('black')

        # Set up other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(piece_order):
            self.board[0][col] = piece_class('white')
            self.board[7][col] = piece_class('black')

    def display(self):
        print("  a b c d e f g h")
        print(" +-+-+-+-+-+-+-+-+")
        for row in range(7, -1, -1):
            print(f"{row+1}|", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    print(f"{piece}|", end="")
                else:
                    print(" |", end="")
            print(f" {row+1}")
            print(" +-+-+-+-+-+-+-+-+")
        print("  a b c d e f g h")

    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        if not piece or piece.color != self.current_player:
            return False

        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        if self.board[end_row][end_col] and self.board[end_row][end_col].color == self.current_player:
            return False

        if isinstance(piece, Pawn):
            return self.is_valid_pawn_move(start, end)
        elif isinstance(piece, Rook):
            return self.is_valid_rook_move(start, end)
        elif isinstance(piece, Knight):
            return self.is_valid_knight_move(start, end)
        elif isinstance(piece, Bishop):
            return self.is_valid_bishop_move(start, end)
        elif isinstance(piece, Queen):
            return self.is_valid_queen_move(start, end)
        elif isinstance(piece, King):
            return self.is_valid_king_move(start, end)

        return False

    def is_valid_pawn_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        direction = 1 if self.current_player == 'white' else -1

        if start_col == end_col and self.board[end_row][end_col] is None:
            if end_row == start_row + direction:
                return True
            if (self.current_player == 'white' and start_row == 1 and end_row == 3) or \
               (self.current_player == 'black' and start_row == 6 and end_row == 4):
                return self.board[start_row + direction][start_col] is None
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return self.board[end_row][end_col] is not None and self.board[end_row][end_col].color != self.current_player

        return False

    def is_valid_rook_move(self, start, end):
        return self.is_clear_path(start, end) and (start[0] == end[0] or start[1] == end[1])

    def is_valid_knight_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def is_valid_bishop_move(self, start, end):
        return self.is_clear_path(start, end) and abs(start[0] - end[0]) == abs(start[1] - end[1])

    def is_valid_queen_move(self, start, end):
        return self.is_valid_rook_move(start, end) or self.is_valid_bishop_move(start, end)

    def is_valid_king_move(self, start, end):
        row_diff = abs(start[0] - end[0])
        col_diff = abs(start[1] - end[1])
        return max(row_diff, col_diff) == 1

    def is_clear_path(self, start, end):
        row_step = 0 if start[0] == end[0] else (1 if start[0] < end[0] else -1)
        col_step = 0 if start[1] == end[1] else (1 if start[1] < end[1] else -1)
        row, col = start
        while (row, col) != end:
            row += row_step
            col += col_step
            if (row, col) != end and self.board[row][col] is not None:
                return False
        return True

    def make_move(self, start, end):
        if self.is_valid_move(start, end):
            piece = self.board[start[0]][start[1]]
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None
            self.move_history.append((start, end, piece))
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False

    def undo_move(self):
        if self.move_history:
            start, end, piece = self.move_history.pop()
            self.board[start[0]][start[1]] = piece
            self.board[end[0]][end[1]] = None
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False

    def get_all_valid_moves(self):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col].color == self.current_player:
                    for end_row in range(8):
                        for end_col in range(8):
                            if self.is_valid_move((row, col), (end_row, end_col)):
                                valid_moves.append(((row, col), (end_row, end_col)))
        return valid_moves

    def is_game_over(self):
        return len(self.get_all_valid_moves()) == 0

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_algebraic_notation(row, col):
    return f"{chr(col + ord('a'))}{row + 1}"

def bot_move(board):
    valid_moves = board.get_all_valid_moves()
    if not valid_moves:
        return None

    def evaluate_move(move):
        start, end = move
        piece = board.board[start[0]][start[1]]
        target = board.board[end[0]][end[1]]

        score = 0
        # Prioritize captures
        if target:
            score += 10
            # Prioritize capturing higher-value pieces
            if isinstance(target, Queen):
                score += 9
            elif isinstance(target, Rook):
                score += 5
            elif isinstance(target, Bishop) or isinstance(target, Knight):
                score += 3
            elif isinstance(target, Pawn):
                score += 1

        # Prioritize advancing pawns
        if isinstance(piece, Pawn):
            score += end[0] if board.current_player == 'white' else 7 - end[0]

        # Prioritize controlling the center
        if 2 <= end[0] <= 5 and 2 <= end[1] <= 5:
            score += 2

        # Prioritize developing pieces in the opening
        if len(board.move_history) < 10:
            if isinstance(piece, (Knight, Bishop)) and start[0] in (0, 7):
                score += 3

        return score

    # Choose the best move based on the evaluation
    best_move = max(valid_moves, key=evaluate_move)
    return best_move

def play_chess():
    board = ChessBoard()
    player_color = input("Choose your color (white/black): ").lower()
    bot_color = 'black' if player_color == 'white' else 'white'

    while not board.is_game_over():
        clear_console()
        board.display()
        print(f"{board.current_player}'s turn")

        if board.current_player == player_color:
            while True:
                move = input("Enter your move (e.g., e2 e4) or 'undo' to undo last move: ")
                if move.lower() == 'undo':
                    if board.undo_move():
                        board.undo_move()  # Undo both player and bot moves
                        print("Move undone.")
                        break
                    else:
                        print("Cannot undo further.")
                        continue

                try:
                    start, end = move.split()
                    start = (int(start[1]) - 1, ord(start[0]) - ord('a'))
                    end = (int(end[1]) - 1, ord(end[0]) - ord('a'))

                    if board.make_move(start, end):
                        print("Move successful!")
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid input. Please use the format 'e2 e4'.")
        else:
            print("Bot is thinking...")
            time.sleep(1)  # Simulate thinking time
            bot_move_result = bot_move(board)
            if bot_move_result:
                start, end = bot_move_result
                board.make_move(start, end)
                print(f"Bot moved: {get_algebraic_notation(start[0], start[1])} to {get_algebraic_notation(end[0], end[1])}")
            else:
                print("Bot has no valid moves!")

        time.sleep(1)  # Pause to show the move

    clear_console()
    board.display()
    print("Game over!")
    if board.current_player == player_color:
        print("You lose!")
    else:
        print("You win!")

if __name__ == "__main__":
    play_chess()
