import pygame
import sys
import numpy as np

pygame.init()

WIDTH, HEIGHT = 700, 700  # Height increased to add a top row for drop selection
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]


class ConnectFourBot:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        
    # Checks if a given column is valid to drop
    def check_valid_move(self, col):
        return board[ROWS-1][col] == 0

    # Makes the moves
    def make_move(self, col, player):
        row = 0
        while row < self.rows:
            if board[row][col] == 0:
                board[row][col] = player
                return row
            row += 1
            
    # Verifies a move will win
    def check_win(self, player):
        # Checks for a column win
        for row in range(self.rows):
            for col in range(self.cols - 3):
                # Adjust the self.board parameters to verify wins
                if all(board[row][col+i] == player for i in range(4)):
                    return True
        # Checks for a row win
        for row in range(self.rows - 3):
                for col in range(self.cols - 3):
                    if all(board[row+i][col] == player for i in range(4)):
                           return True
        # Checks for diagonal win
        for row in range(self.rows - 3):
                for col in range(self.cols - 3):
                    if all(board[row+i][col+i] == player for i in range(4)):
                        return True
                    if all(board[row+i][col + 3 - i] == player for i in range(4)):
                        return True
        return False
    
    # Helper function to chek for the board being full
    def is_board_full(self):
        return np.all(board != 0)

    # Evaluation function for the end of the minimax
    def board_evaluation(self):
        # This is *really* rudimentary, we can re-engineer this as needed
        if self.check_win(2):
            return 100
        elif self.check_win(1):
            return -100
        else:
            return 0
    
    # Recursive minimax implementation
    def minimax(self, depth, is_max):
        if depth == 0 or self.check_win(1) or self.check_win(2) or self.is_board_full():
            return self.board_evaluation()
        
        if is_max:
            best_score = -np.inf
            for col in range(self.cols):
                if self.check_valid_move(col):
                    row = self.make_move(col, 2)
                    score = self.minimax(depth - 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = np.inf
            for col in range(self.cols):
                if self.check_valid_move(col):
                    row = self.make_move(col, 1)
                    score = self.minimax(depth - 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
            return best_score
        
    def best_move(self, depth):
        best_val = -np.inf
        best_col = -1
        for col in range(self.cols):
            if self.check_valid_move(col):
                row = self.make_move(col, 2)
                score = self.minimax(depth - 1, False)
                board[row][col] = 0

                if score > best_val:
                    best_val = score
                    best_col = col
                elif score == best_val:
                    if abs(3 - col) < abs(3 - best_col):
                        best_col = col

        print(best_col)
        return best_col
                                        
# Note: Bot is not integrated to program, we've gotta still do that!
 
# TODO: Verify bot logic works with going first/second
#       Test bot once operational
#       

# Constants


# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# Create the board

def draw_board():
    screen.fill(BLACK)  # Fill background with black
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), RADIUS)

    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - (row * SQUARE_SIZE + SQUARE_SIZE // 2)), RADIUS)
    pygame.display.update()

def drop_piece(row, col, piece):
    board[row][col] = piece

def is_valid_location(col):
    return board[ROWS-1][col] == 0

def get_next_open_row(col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def winning_move(piece):
    # Check horizontal locations
    for c in range(COLS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
        
 # Main game loop
game_over = False
turn = 0  # 0 for Player 1 (RED), 1 for Player 2 (YELLOW)

draw_board()  # Initial draw
bot = ConnectFourBot(ROWS, COLS)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, SQUARE_SIZE // 2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
            # Player 1 Input
            if turn == 0:
                pos_x = event.pos[0]
                col = pos_x // SQUARE_SIZE

                if is_valid_location(col):
                    row = get_next_open_row(col)
                    drop_piece(row, col, 1)

                    if winning_move(1):
                        print("Player 1 wins!")
                        game_over = True

                else:
                    continue


            # Player 2 Input
            else:
                col = bot.best_move(1)
                if col >= 0:
                    row = get_next_open_row(col)
                    drop_piece(row, col, 2)

                    if winning_move(2):
                        print("Player 2 wins!")
                        game_over = True

                else:
                    continue

            draw_board()

            # Switch turn
            turn += 1
            turn %= 2

            if game_over:
                pygame.time.wait(3000)
