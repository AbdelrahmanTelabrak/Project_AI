#Done:
	#add a function "evaluateWindow" to evaluate each window to clean the code
	#"evaluateWindow" can now make the Comp. agent block player's winning move
	#Implementing "isTerminal" to check if you reached the final nodes
	#Implementing MINMAX algorithm
	#No need for "chooseBestMove"

import random

import numpy as np
import pygame
from pygame.locals import *
import sys
import math


#=============== GUI to select the algorithm type and difficulty level of the game ====
# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Settings")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 24)

# Game settings
selected_algorithm = None
selected_difficulty = None

# Algorithm types and difficulty levels
algorithm_types = ["MiniMax", " Alpha-Beta"]
difficulty_levels = ["Easy", "Medium", "Hard"]


# Function to draw the settings screen
def draw_settings_screen():
    screen.fill(WHITE)

    # Draw algorithm type selection
    algorithm_text = font.render("Select Algorithm Type:", True, BLACK)
    screen.blit(algorithm_text, (50, 50))
    algorithm_y = 80
    for algorithm in algorithm_types:
        algorithm_button = pygame.Rect(50, algorithm_y, 150, 30)
        pygame.draw.rect(screen, BLACK, algorithm_button, 2)
        algorithm_text = font.render(algorithm, True, BLACK)
        screen.blit(algorithm_text, (60, algorithm_y + 5))
        algorithm_y += 40

    # Draw difficulty level selection
    difficulty_text = font.render("Select Difficulty Level:", True, BLACK)
    screen.blit(difficulty_text, (220, 50))
    difficulty_y = 80
    for difficulty in difficulty_levels:
        difficulty_button = pygame.Rect(220, difficulty_y, 150, 30)
        pygame.draw.rect(screen, BLACK, difficulty_button, 2)
        difficulty_text = font.render(difficulty, True, BLACK)
        screen.blit(difficulty_text, (230, difficulty_y + 5))
        difficulty_y += 40

    pygame.display.update()


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check algorithm type selection
            for i in range(len(algorithm_types)):
                algorithm_button = pygame.Rect(50, 80 + (40 * i), 150, 30)
                if algorithm_button.collidepoint(mouse_pos):
                    selected_algorithm = algorithm_types[i]

            # Check difficulty level selection
            for i in range(len(difficulty_levels)):
                difficulty_button = pygame.Rect(220, 80 + (40 * i), 150, 30)
                if difficulty_button.collidepoint(mouse_pos):
                    selected_difficulty = difficulty_levels[i]

    # Draw the settings screen
    draw_settings_screen()

# Print selected settings
print("Selected Algorithm Type:", selected_algorithm)
print("Selected Difficulty Level:", selected_difficulty)

# Quit Pygame
pygame.quit()

#=============== GUI to select the algorithm type and difficulty level of the game ====



COLUMNS = 7
ROWS = 6
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

WINDOW_SIZE = 4  # Window buffer size to calculate score in positionScore function.

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0  # Empty Piece on board


def Build_board():
    board = np.zeros((6, 7))
    return board


def SetPiece(board, row, col, piece):
    board[row][col] = piece


def isValid(board, col):
    if board[5][col] == 0:
        return True
    else:
        return False


def GetNextRow(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r


####to print board right(flip it)#############
def printBoard(board):
    print(np.flip(board, 0))


####to print board right#############

# call function (Build_board)
board = Build_board()


# printBoard(board)

################ function to check winning###################
def winning_move(board, piece):
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3]==piece:
                print("Won horizontal")
                return True
    # check vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c]==piece:
                print("Won vertical")
                return True

    # check + diagonal
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3]==piece:
                print("Won + diagonal")
                return True

    # check - diagonal
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3]==piece:
                print("Won - diagonal")
                return True


# -------------Calculate the score of the position---------
def evaluateWindow(window, piece):
    score = 0
    oppPiece = (piece+1)%2
    if window.count(piece) == 4:
        score += 1000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score +=2
    elif window.count(oppPiece) == 3 and window.count(EMPTY) == 1:
        score -= 10
    return score

def positionScore(board, piece):
    score = -100

    # calculate center score
    centerElements = [int(i) for i in list(board[:, 3])]
    centerCounter = centerElements.count(piece)
    score += centerCounter*6
    # calculate score horizontally
    for row in range(ROWS):
        rowElements = [int(i) for i in list(board[row, :])]
        for col in range(COLUMNS - 3):
            window = rowElements[col:col + WINDOW_SIZE]
            evaluateWindow(window, piece)

    # calculate score vertically
    for col in range(COLUMNS):
        colElements = [int(i) for i in list(board[:, col])]
        for row in range(ROWS - 3):
            window = colElements[row:row + WINDOW_SIZE]
            evaluateWindow(window, piece)

    # calculate score of + diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + i][col + i] for i in range(WINDOW_SIZE)]
            evaluateWindow(window, piece)

    # calculate score of - diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + 3 - i][col + i] for i in range(WINDOW_SIZE)]
            evaluateWindow(window, piece)

    return score


def getAllValidMoves(board):
    validMoves = []
    for col in range(COLUMNS):
        if isValid(board, col):
            validMoves.append(col)
    return validMoves


def chooseBestMove(board, piece):
    # first get all valid moves
    validMoves = getAllValidMoves(board)
    bestScore = 0
    bestMove = random.choice(validMoves)
    # iterate over moves to get the move with highest score
    for move in validMoves:
        row = GetNextRow(board, move)
        tempBoard = board.copy()
        SetPiece(tempBoard, row, move, piece)
        # evaluate the move
        score = positionScore(tempBoard, piece)
        if score > bestScore:
            bestScore = score
            bestMove = move

    return bestMove

# ------------Implementing MINMAX------------------------------------
def isTerminalNode(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(getAllValidMoves(board)) == 0

def minmax(board, depth, maxPlayer):
    validMoves = getAllValidMoves(board)
    isTerminal = isTerminalNode(board)
    if depth==0 or isTerminal:
        if isTerminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000)
            else:
                return (None, 0)
        else: #for if depth==0
            return (None, positionScore(board, AI_PIECE))
    if maxPlayer:
        score = -math.inf
        column = random.choice(validMoves)
        for move in validMoves:
            row = GetNextRow(board, move)
            tempBoard = board.copy()
            SetPiece(tempBoard, row, move, AI_PIECE)
            newScore = minmax(tempBoard, depth-1, False)[1]
            if newScore>score:
                score = newScore
                column = move
        return column, score

    else:
        score = math.inf
        column = random.choice(validMoves)
        for move in validMoves:
            row = GetNextRow(board, move)
            tempBoard = board.copy()
            SetPiece(tempBoard, row, move, PLAYER_PIECE)
            newScore = minmax(tempBoard, depth-1, True)[1]
            if newScore<score:
                score = newScore
                column = move
        return column, score


# ------------Implementing MINMAX------------------------------------



# -----------------improve the code and implement the Alpha-Beta pruning algorithm---------


def Minmax(board, depth, alpha, beta, maxPlayer):
    validMoves = getAllValidMoves(board)
    isTerminal = isTerminalNode(board)

    if depth == 0 or isTerminal:
        if isTerminal:
            if winning_move(board, AI_PIECE):
                return (None, 1000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000)
            else:
                return (None, 0)
        else:
            return (None, positionScore(board, AI_PIECE))

    if maxPlayer:
        score = -math.inf
        column = random.choice(validMoves)
        for move in validMoves:
            row = GetNextRow(board, move)
            tempBoard = board.copy()
            SetPiece(tempBoard, row, move, AI_PIECE)
            newScore = Minmax(tempBoard, depth - 1, alpha, beta, False)[1]

            if newScore > score:
                score = newScore
                column = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return column, score
    else:
        score = math.inf
        column = random.choice(validMoves)
        for move in validMoves:
            row = GetNextRow(board, move)
            tempBoard = board.copy()
            SetPiece(tempBoard, row, move, PLAYER_PIECE)
            newScore = Minmax(tempBoard, depth - 1, alpha, beta, True)[1]

            if newScore < score:
                score = newScore
                column = move

            beta = min(beta, score)
            if alpha >= beta:
                break

        return column, score

# -----------------improve the code and implement the Alpha-Beta pruning algorithm---------


################ function to check winning###################


def draw(board):
    for col in range(COLUMNS):
        for row in range(ROWS):
            pygame.draw.rect(screen, blue,
                             (col * SIZEOFSQUARE, row * SIZEOFSQUARE + SIZEOFSQUARE, SIZEOFSQUARE, SIZEOFSQUARE))
            pygame.draw.circle(screen, black, (
                int(col * SIZEOFSQUARE + SIZEOFSQUARE / 2), int(row * SIZEOFSQUARE + SIZEOFSQUARE + SIZEOFSQUARE / 2)),
                               radius)

    for col in range(COLUMNS):
        for row in range(ROWS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, red, (
                    int(col * SIZEOFSQUARE + SIZEOFSQUARE / 2), height - int(row * SIZEOFSQUARE + SIZEOFSQUARE / 2)),
                                   radius)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, yellow, (
                    int(col * SIZEOFSQUARE + SIZEOFSQUARE / 2), height - int(row * SIZEOFSQUARE + SIZEOFSQUARE / 2)),
                                   radius)
    pygame.display.update()


switch = random.choice([AI, PLAYER])  # to turn play to another player
GameOver = False

########pygame utilities###################
pygame.init()
SIZEOFSQUARE = 100
width = COLUMNS * SIZEOFSQUARE
height = (ROWS + 1) * SIZEOFSQUARE
size = (width, height)
radius = int(SIZEOFSQUARE / 2 - 5)
screen = pygame.display.set_mode(size)
draw(board)
pygame.display.update()
font = pygame.font.SysFont("monospace", 75)

########pygame utilities###################


while (GameOver == False):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  ## 3shan lma ndos 3la X y5rgny mn el window
            sys.exit()

        # if event.type == pygame.MOUSEMOTION:
        #     pygame.draw.rect(screen, black, (0, 0, width, SIZEOFSQUARE))
        #     posx = event.pos[0]
        #     if switch == 0:
        #         pygame.draw.circle(screen, red, (posx, int(SIZEOFSQUARE / 2)), radius)

        pygame.display.update()

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pygame.draw.rect(screen, black, (0, 0, width, SIZEOFSQUARE))
        #     # print(event.pos)
        #     # continue
        #     # #Player 1 play:
        if switch == 0:
            select = chooseBestMove(board, PLAYER_PIECE)
            # posx = event.pos[0]

            #select = int(math.floor(posx / SIZEOFSQUARE))  # int(input("Select (player 1) from 0-6: "))
            switch = 1
            if isValid(board, select):
                row = GetNextRow(board, select)
                SetPiece(board, row, select, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    label = font.render("Computer wins", 1, red)
                    screen.blit(label, (40, 10))
                    GameOver = True
                pygame.time.wait(500)
                printBoard(board)
                draw(board)
            #
            #      #print(select)
            #
            # # Player 2 play:
    if switch == AI and not GameOver:
        #select = chooseBestMove(board, AI_PIECE)

        #select algo and depth
        if selected_algorithm=="MiniMax":
            if selected_difficulty == "Easy":
                select, minmaxScore = minmax(board, 1, True)
            elif selected_difficulty == "Medium":
                select,minmaxScore = minmax(board, 3, True)
            elif selected_difficulty == "Hard":
                select,minmaxScore = minmax(board, 5, True)
        else: #Alpha-Beta
            if selected_difficulty == "Easy":
                select, minmaxScore = Minmax(board, 1,-math.inf,math.inf, True)
            elif selected_difficulty == "Medium":
                select, minmaxScore = Minmax(board, 3,-math.inf,math.inf, True)
            elif selected_difficulty == "Hard":
                select, minmaxScore = Minmax(board, 5, -math.inf, math.inf, True)



        switch = PLAYER
        if isValid(board, select):
            row = GetNextRow(board, select)
            SetPiece(board, row, select, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = font.render("Ai wins", 1, yellow)
                screen.blit(label, (40, 10))
                GameOver = True

            pygame.time.wait(500)
            printBoard(board)
            draw(board)
    if GameOver == True:
        pygame.time.wait(5000)


