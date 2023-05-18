
Done:
	.Play against Computer
	.calculate the score of the position ( Vertically & Horizontally)
	.Check score Diagonally
	.get all valid moves
	.choose the best move depending on the one with highest score.
import random

import numpy as np
import pygame

import sys
import math

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
def positionScore(board, piece):
    score = 0

    # calculate score horizontally
    for row in range(ROWS):
        rowElements = [int(i) for i in list(board[row, :])]
        for col in range(COLUMNS - 3):
            window = rowElements[col:col + WINDOW_SIZE]
            if window.count(piece) == 4:
                score += 1000
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    # calculate score vertically
    for col in range(COLUMNS):
        colElements = [int(i) for i in list(board[:, col])]
        for row in range(ROWS - 3):
            window = colElements[row:row + WINDOW_SIZE]
            if window.count(piece) == 4:
                score += 1000
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    # calculate score of + diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + i][col + i] for i in range(WINDOW_SIZE)]
            if window.count(piece) == 4:
                score += 1000
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

    # calculate score of - diagonal
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            window = [board[row + 3 - i][col + i] for i in range(WINDOW_SIZE)]
            if window.count(piece) == 4:
                score += 1000
            elif window.count(piece) == 3 and window.count(EMPTY) == 1:
                score += 10

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

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, SIZEOFSQUARE))
            posx = event.pos[0]
            if switch == 0:
                pygame.draw.circle(screen, red, (posx, int(SIZEOFSQUARE / 2)), radius)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, SIZEOFSQUARE))
            # print(event.pos)
            # continue
            # #Player 1 play:
            if switch == 0:
                posx = event.pos[0]

                select = int(math.floor(posx / SIZEOFSQUARE))  # int(input("Select (player 1) from 0-6: "))
                switch = 1
                if isValid(board, select):
                    row = GetNextRow(board, select)
                    SetPiece(board, row, select, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        label = font.render("Player 1 wins", 1, red)
                        screen.blit(label, (40, 10))
                        GameOver = True

                    printBoard(board)
                    draw(board)
            #
            #      #print(select)
            #
            # # Player 2 play:
    if switch == AI and not GameOver:
        select = chooseBestMove(board, AI_PIECE)
        switch = PLAYER
        if isValid(board, select):
            row = GetNextRow(board, select)
            SetPiece(board, row, select, AI_PIECE)
            if winning_move(board, AI_PIECE):
                label = font.render("Player 2 wins", 1, yellow)
                screen.blit(label, (40, 10))
                GameOver = True

            pygame.time.wait(500)
            printBoard(board)
            draw(board)
    if GameOver == True:
        pygame.time.wait(1000)
