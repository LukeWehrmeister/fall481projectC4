import pygame
import sys
import numpy as np
import random

pygame.init()

WIDTH, HEIGHT = 700, 700  # Height increased to add a top row for drop selection
ROWS, COLS = 6, 7
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE // 2 - 5
board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
PLAYER_PIECE = 1
BOT_PIECE = 2


def position_evaluation(board, piece):
    score = 0
    c_arr = [int(board[i][COLS//2]) for i in range(ROWS)]
    c_count = c_arr.count(piece)
    score += c_count * 4
    
    #Horizontal scoring
    for h in range(ROWS):
        h_array = [int(board[h][c]) for c in range(COLS)]
        for c in range(COLS - 3):
            tally = h_array[h:h + 4]
            score += evaluate_moves(tally, piece)
    #Vertical Scoring
    for v in range(COLS):
        v_array = [int(board[r][v]) for r in range(ROWS)]
        for r in range(ROWS - 3):
            tally = v_array[v:v + 4]
            score += evaluate_moves(tally, piece)
    #Score Diagonal
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            tally = [board[r+i][c+i] for i in range(4)]
            score += evaluate_moves(tally, piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            rally = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_moves(tally, piece)
    return score

def evaluate_moves(block, piece):
    score = 0
    if piece == BOT_PIECE:
        opposition = PLAYER_PIECE
    else:
        opposition = BOT_PIECE
    
    if block.count(piece) == 4:
        score += 500
    elif block.count(piece) == 3 and block.count(0) == 1:
        score += 25
    elif block.count(piece) == 2 and block.count(0) == 2:
        score += 10
    
    if block.count(opposition) == 3 and block.count(0) == 1:
        score -= 20

    return score
    
def minimax(board, depth, alpha, beta, is_max):
    #checks for all available plays
    all_plays = [p for p in range(COLS) if is_valid_location(board, p)]
        
    #these are all situations where the game is over
    end_of_game = winning_move(BOT_PIECE) or winning_move(PLAYER_PIECE) or len(all_plays) == 0

    if depth == 0 or end_of_game:
        if end_of_game:
            if winning_move(BOT_PIECE):
                return None, 1124
            elif winning_move(PLAYER_PIECE):
                return None, -1124
            else:
                return None, 0
        else:
            return None, position_evaluation(board, BOT_PIECE)
        
    if is_max:
        v = -np.inf
        best_col = random.choice(all_plays)
        for c in all_plays:
            #row = get_next_open_row(board, c)
            temp_board = board.copy()
            row = get_next_open_row(temp_board, c)
            drop_piece(temp_board, row, c, BOT_PIECE)
            ingest_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if ingest_score > v:
                v = ingest_score
                best_col = c
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return best_col, v
    
    else:
        v = np.inf
        best_col = random.choice(all_plays)
        for c in all_plays:
            #row = get_next_open_row(board, c)
            temp_board = board.copy()
            row = get_next_open_row(temp_board, c)
            drop_piece(temp_board, row, c, PLAYER_PIECE)
            ingest_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if ingest_score < v:
                v = ingest_score
                best_col = c
            beta = min(beta, v)
            if alpha >= beta:
                break
        return best_col, v
    
def bot_move(board):
    max_depth = 4
    temp_board = board.copy()
    col, _ = minimax(temp_board, max_depth, -np.inf, np.inf, True)
    return col


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

# Function for the bot to drop pieces into a copy of the board for the minimax function
#def bot_drop_piece(board, row, col, piece):
#    b_board = board.copy()
#    b_board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
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
#bot = ConnectFourBot(ROWS, COLS)

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

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(row, col, 1)

                    if winning_move(1):
                        print("Player 1 wins!")
                        game_over = True

                else:
                    continue


            # Player 2 Input
            else:
                bot_col = bot_move(board)
                if is_valid_location(board, bot_col):
                    bot_row = get_next_open_row(board, bot_col)
                    drop_piece(bot_row, bot_col, 2)
                    
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
