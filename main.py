import random
import time
import os

class ChessPiece:
    def __init__(self, color):
        self.color = color

class Pawn(ChessPiece):
    pass

class Rook(ChessPiece):
    pass

class Knight(ChessPiece):
    pass

class Bishop(ChessPiece):
    pass

class Queen(ChessPiece):
    pass

class King(ChessPiece):
    pass

class ChessBoard:
    def __init__(self):
        self.board = self.create_initial_board()
        self.current_player = 'white'

    def create_initial_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Set up pawns
        for col in range(8):
            board[1][col] = Pawn('white')
            board[6][col] = Pawn('black')

        # Set up other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            board[0][col] = piece_order[col]('white')
            board[7][col] = piece_order[col]('black')

        return board

    def display(self):
        piece_symbols = {
            'white': {
                'Pawn': '♙', 'Rook': '♖', 'Knight': '♘',
                'Bishop': '♗', 'Queen': '♕', 'King': '♔'
            },
            'black': {
                'Pawn': '♟', 'Rook': '♜', 'Knight': '♞',
                'Bishop': '♝', 'Queen': '♛', 'King': '♚'
            }
        }

        print("  a b c d e f g h")
        print(" ┌───────────────┐")
        for row in range(8):
            print(f"{8-row}│", end="")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    symbol = piece_symbols[piece.color][piece.__class__.__name__]
                else:
                    symbol = '·' if (row + col) % 2 == 0 else '·'
                print(f"{symbol}", end=" ")
            print(f"│{8-row}")
        print(" └───────────────┘")
        print("  a b c d e f g h")

    def is_valid_move(self, start, end):
        # This is a simplified version. In a real chess game, you'd need to implement all the rules for each piece type.
        start_row, start_col = start
        end_row, end_col = end

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        piece = self.board[start_row][start_col]
        if not piece or piece.color != self.current_player:
            return False

        # Check if the end position is empty or contains an opponent's piece
        if self.board[end_row][end_col] and self.board[end_row][end_col].color == self.current_player:
            return False

        return True

    def make_move(self, start, end):
        if self.is_valid_move(start, end):
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = None
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False

    def get_all_valid_moves(self):
        valid_moves = []
        for start_row in range(8):
            for start_col in range(8):
                for end_row in range(8):
                    for end_col in range(8):
                        if self.is_valid_move((start_row, start_col), (end_row, end_col)):
                            valid_moves.append(((start_row, start_col), (end_row, end_col)))
        return valid_moves

    def is_capture(self, end_pos):
        return self.board[end_pos[0]][end_pos[1]] is not None

    def is_game_over(self):
        # This is a simplified version. In a real chess game, you'd need to check for checkmate, stalemate, etc.
        return len(self.get_all_valid_moves()) == 0

    def is_checkmate(self):
        # Simplified checkmate check
        return self.is_game_over()  # In this simplified version, game over is equivalent to checkmate

    def is_stalemate(self):
        # Simplified stalemate check
        return False  # In this simplified version, we're not implementing stalemate

    def get_opponent(self):
        return 'black' if self.current_player == 'white' else 'white'

def bot_move(board, elo=900):
    elo = min(900, max(100, elo))  # Ensure Elo is between 100 and 900
    valid_moves = board.get_all_valid_moves()
    if not valid_moves:
        return None

    # Adjust probabilities based on Elo
    random_move_chance = linear_interpolation(0.7, 0.3, elo, 100, 900)
    capture_chance = linear_interpolation(0.3, 0.7, elo, 100, 900)
    developing_move_chance = linear_interpolation(0.2, 0.4, elo, 100, 900)
    bad_move_chance = linear_interpolation(0.4, 0.2, elo, 100, 900)

    # 1. Occasionally make random moves
    if random.random() < random_move_chance:
        return random.choice(valid_moves)

    # 2. Prioritize captures, but don't always choose the best capture
    capture_moves = [move for move in valid_moves if board.is_capture(move[1])]
    if capture_moves and random.random() < capture_chance:
        return random.choice(capture_moves)

    # 3. Sometimes make "developing" moves (moving pieces towards the center)
    developing_moves = [move for move in valid_moves if is_developing_move(board, move)]
    if developing_moves and random.random() < developing_move_chance:
        return random.choice(developing_moves)

    # 4. Occasionally make "bad" moves (moving pieces to the edge)
    bad_moves = [move for move in valid_moves if is_bad_move(move)]
    if bad_moves and random.random() < bad_move_chance:
        return random.choice(bad_moves)

    # 5. If none of the above, make a random move
    return random.choice(valid_moves)

def linear_interpolation(start, end, current, min_val, max_val):
    return start + (end - start) * (current - min_val) / (max_val - min_val)

def is_developing_move(board, move):
    start, end = move
    piece = board.board[start[0]][start[1]]

    # Consider moves towards the center as developing moves
    center_rows = [3, 4]
    center_cols = [3, 4]

    if isinstance(piece, (Pawn, Knight, Bishop)):
        return end[0] in center_rows or end[1] in center_cols

    return False

def is_bad_move(move):
    _, end = move
    # Consider moves to the edge of the board as "bad" moves
    return end[0] in [0, 7] or end[1] in [0, 7]

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_chess():
    board = ChessBoard()
    player_color = input("Choose your color (white/black): ").lower()
    bot_color = 'black' if player_color == 'white' else 'white'

    while True:
        try:
            bot_elo = int(input("Enter bot Elo rating (100-900): "))
            if 100 <= bot_elo <= 900:
                break
            else:
                print("Please enter a value between 100 and 900.")
        except ValueError:
            print("Please enter a valid number.")

    while not board.is_game_over():
        clear_console()
        print(f"Bot Elo: {bot_elo}")
        print(f"Current player: {board.current_player.capitalize()}")
        board.display()

        if board.current_player == player_color:
            while True:
                move = input("Enter your move (e.g., e2e4) or 'quit' to end the game: ")
                if move.lower() == 'quit':
                    print("Game ended by player.")
                    return
                try:
                    start = (8 - int(move[1]), ord(move[0]) - ord('a'))
                    end = (8 - int(move[3]), ord(move[2]) - ord('a'))
                    if board.make_move(start, end):
                        break
                    else:
                        print("Invalid move. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input. Please use the format 'e2e4'.")
        else:
            print("Bot is thinking...")
            time.sleep(1)  # Simulate thinking time
            bot_move_result = bot_move(board, bot_elo)
            if bot_move_result:
                start, end = bot_move_result
                if board.make_move(start, end):
                    print(f"Bot moved: {chr(start[1] + ord('a'))}{8-start[0]} to {chr(end[1] + ord('a'))}{8-end[0]}")
                else:
                    print("Bot made an invalid move. Ending the game.")
                    break
            else:
                print("Bot has no valid moves!")
                break

        time.sleep(1)  # Pause to show the move

    clear_console()
    board.display()
    print("Game Over!")
    if board.is_checkmate():
        print(f"Checkmate! {board.get_opponent()} wins!")
    elif board.is_stalemate():
        print("Stalemate! The game is a draw.")
    else:
        print("The game has ended.")

# Run the game
if __name__ == "__main__":
    play_chess()
