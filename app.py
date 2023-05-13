import numpy as np
COLUMNS = 7
ROWS = 6

def Build_board():
    board = np.zeros((6,7))
    return board


def SetPiece(board,row,col,piece):
    board[row][col] = piece

def isValid(board,col):
    if board[5][col] == 0:
        return True
    else:
        return False



def GetNextRow(board,col):
    for r in range(ROWS):
        if board[r][col]==0:
            return r



####to print board right(flip it)#############
def printBoard(board):
    print(np.flip(board,0))
####to print board right#############

#call function (Build_board)
board = Build_board()
printBoard(board)


switch=0 #to turn play to another player
GameOver = False
while  (GameOver==False):


    #Player 1 play:
    if switch == 0:
        select = int(input("Select (player 1) from 0-6: "))
        switch = 1
        if isValid(board,select):
            row =GetNextRow(board,select)
            SetPiece(board,row,select,1)

        # print(select)

    # Player 2 play:
    else:
        select = int(input("Select (player 2) from 0-6: "))
        switch = 0
        if isValid(board,select):
            row = GetNextRow(board,select)
            SetPiece(board,row,select,2)


    printBoard(board)
