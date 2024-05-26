import numpy as np
import random
import pygame
import sys
import math
import asyncio
import time

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)
ORANGE = (255,165,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

start_first_button = None
AI_starts_button = None
level = None
start_turn = None
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece

def drop_piece_animated(board,row,col,piece):
    for r in range(ROW_COUNT -1,row,-1):
        b_copy = board.copy()
        b_copy[r][col] = piece
        draw_board(b_copy)
        time.sleep(.075)
    drop_piece(board, row, col, piece)


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE

    if window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 1

    return score


def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    ## Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in [3,4,2,5,1,0,6]:
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def draw_board(board):
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

async def reset_game():
    global board, game_over
    board = create_board()
    screen.fill(BLACK)
    draw_board(board)
    game_over = False
    print('hi')
async def draw_menu():

    global start_first_button, AI_starts_button, level, start_turn
    screen.fill(BLACK)
    level_selected = False
    while not level_selected:
        title = myfont.render("Connect Four", True, WHITE)
        screen.blit(title, (width // 2 - 275, height // 4 - 100))

        beginner_button = pygame.Rect(width //2 -150,height //2-25,300,50)
        pygame.draw.rect(screen,RED,beginner_button)
        label = small_font.render("Beginner",True,WHITE)
        screen.blit(label,(beginner_button.x+10,beginner_button.y+10))

        intermediate_button = pygame.Rect(width // 2 - 150, height // 2 - 85, 300, 50)
        pygame.draw.rect(screen, RED, intermediate_button)
        label = small_font.render("Intermediate", True, WHITE)
        screen.blit(label, (intermediate_button.x + 10, intermediate_button.y + 10))

        expert_button = pygame.Rect(width // 2 - 150, height // 2 - 145, 300, 50)
        pygame.draw.rect(screen, RED, expert_button)
        label = small_font.render("Expert", True, WHITE)
        screen.blit(label, (expert_button.x + 10, expert_button.y + 10))

        pygame.display.update()
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if beginner_button.collidepoint(event.pos):
                    print('hi')
                    level = "Beginner"
                    level_selected = True
                elif intermediate_button.collidepoint(event.pos):
                    level = "Intermediate"
                    level_selected = True
                elif expert_button.collidepoint(event.pos):
                    level = "Expert"
                    level_selected = True
            elif event.type == pygame.QUIT:
                sys.exit()

    screen.fill(BLACK)

    start_first_button = pygame.Rect(width // 2 - 150, height // 2 - 25, 300, 50)
    pygame.draw.rect(screen, RED, start_first_button)

    label = small_font.render("Start First", True, WHITE)

    screen.blit(label, (start_first_button.x + 10, start_first_button.y + 10))
    AI_starts_button = pygame.Rect(width // 2 - 150, height // 2 - 85, 300, 50)
    pygame.draw.rect(screen, RED, AI_starts_button)
    label = small_font.render("AI Starts First", True, WHITE)
    screen.blit(label, (AI_starts_button.x + 10, AI_starts_button.y + 10))
    pygame.display.update()
    turn_selected = False
    # await asyncio.sleep(0)
    while not turn_selected:
        await asyncio.sleep(0)
        for event in pygame.event.get():
            # print('beep')
            await asyncio.sleep(0)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print('bob')
                # await asyncio.sleep(0)
                if start_first_button.collidepoint(event.pos):
                    print('hi')
                    # await asyncio.sleep(0)
                    start_turn = PLAYER
                    print('b')
                    await reset_game()
                    print('hey')
                    turn_selected = True
                elif AI_starts_button.collidepoint(event.pos):
                    print('hey')
                    start_turn = AI
                    await reset_game()
                    turn_selected = True
    print('hi')
board = create_board()

game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

myfont = pygame.font.SysFont("monospace", 75)
small_font = pygame.font.SysFont("monospace",30)

async def main():
    global game_over, start_first_button, AI_starts_button, level, start_turn
    menu = True
    # turn = start_turn
    while True:
        await asyncio.sleep(0)
        if menu:
            await draw_menu()
            menu = False
            turn = start_turn
            await asyncio.sleep(0)

            print(start_first_button.collidepoint)

        else:
            # print('hi')
            for event in pygame.event.get():
                # print('b')
                # await asyncio.sleep(0)
                # print(event)
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION and not game_over:
                    # print('p')
                    # print(turn)
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == PLAYER:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    # print(event.pos)
                    # Ask for Player 1 Input
                    if turn == PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx / SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece_animated(board, row, col, PLAYER_PIECE)
                            draw_board(board)
                            if winning_move(board, PLAYER_PIECE):
                                label = myfont.render("You win!!", 1, RED)
                                print('hi')
                                screen.blit(label, (40, 10))
                                pygame.display.update()
                                game_over = True
                            elif len(get_valid_locations(board)) == 0:
                                label = myfont.render("It's a Draw!", 1, ORANGE)
                                screen.blit(label, (40, 10))
                                pygame.display.update()
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            # print_board(board)


                if game_over:
                    play_again_button_rect = pygame.Rect(width // 2 - 150, height // 2 , 300, 50)
                    pygame.draw.rect(screen, RED, play_again_button_rect)
                    label = small_font.render("Play Again", 1, WHITE)
                    screen.blit(label, (play_again_button_rect.x + 10, play_again_button_rect.y + 10))

                    menu_button = pygame.Rect(width //2 -150, height // 2 - 65,300,50)
                    pygame.draw.rect(screen,RED,menu_button)
                    label = small_font.render("Go Back to Menu",1,WHITE)
                    screen.blit(label,(menu_button.x+10,menu_button.y+10))

                    # await asyncio.sleep(0)
                    # quit_button_rect = pygame.Rect(width // 2 - 150, height // 2 - 130, 300, 50)
                    # pygame.draw.rect(screen, RED, quit_button_rect)
                    # label = small_font.render("Quit", 1, WHITE)
                    # screen.blit(label, (quit_button_rect.x + 10, quit_button_rect.y + 10))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_again_button_rect.collidepoint(event.pos):
                            turn = start_turn
                            await reset_game()
                        elif menu_button.collidepoint(event.pos):
                            menu = True

                        # elif quit_button_rect.collidepoint(event.pos):
                        #     sys.exit()


        # # Ask for Player 2 Input
                if turn == AI and not game_over:

                    import time

                    start_time = time.time()
                    if level == "Beginner":
                        col, minimax_score = minimax(board, 2, -math.inf, math.inf, True)
                    elif level == "Intermediate":
                        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
                    elif level == "Expert":
                        col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)
                    end_time = time.time()
                    time = end_time - start_time
                    print(time)
                    if is_valid_location(board, col):
                        # pygame.time.wait(500)
                        row = get_next_open_row(board, col)
                        drop_piece_animated(board, row, col, AI_PIECE)
                        draw_board(board)
                        if winning_move(board, AI_PIECE):
                            label = myfont.render("The AI wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            game_over = True
                        elif len(get_valid_locations(board)) == 0:
                            label = myfont.render("It's a Draw!",1, ORANGE)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            game_over = True
                        # print_board(board)

                        turn += 1
                        turn = turn % 2

asyncio.run(main())