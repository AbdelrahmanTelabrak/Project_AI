import numpy as np
import pygame

import sys
import math

COLUMNS = 7
ROWS = 6
blue = (0,0,255)
black = (0,0,0)
red=(255,0,0)
yellow=(255,255,0)



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
# printBoard(board)

################ function to check winning###################
def winning_move(board,piece):
    for c in range(COLUMNS-3):
        for r in range (ROWS):
            if board[r][c] == piece and board [r][c+1] == piece and board [r][c+2] == piece and board[r][c+3]:
                return True
#check vertical
    for c in range(COLUMNS):
        for r in range (ROWS-3):
            if board[r][c] == piece and board [r+1][c] == piece and board [r+2][c] == piece and board[r+3][c]:
                return True

#check + diagonal
    for c in range(COLUMNS-3):
        for r in range (ROWS-3):
            if board[r][c] == piece and board [r+1][c+1] == piece and board [r+2][c+2] == piece and board[r+3][c+3]:
                return True

#check - diagonal
    for c in range(COLUMNS-3):
        for r in range (ROWS-3):
          if board[r][c] == piece and board [r-1][c+1] == piece and board [r-2][c+2] == piece and board[r-3][c+3]:
                return True
################ function to check winning###################




def draw(board):
    for col in range(COLUMNS):
        for row in range(ROWS):
            pygame.draw.rect(screen,blue,(col*SIZEOFSQUARE,row*SIZEOFSQUARE+SIZEOFSQUARE,SIZEOFSQUARE,SIZEOFSQUARE))
            pygame.draw.circle(screen,black,(int(col*SIZEOFSQUARE+SIZEOFSQUARE/2),int(row*SIZEOFSQUARE+SIZEOFSQUARE+SIZEOFSQUARE/2)),radius)

    for col in range(COLUMNS):
            for row in range(ROWS):
                if board[row][col]==1:
                    pygame.draw.circle(screen,red,(int(col*SIZEOFSQUARE+SIZEOFSQUARE/2),height-int(row*SIZEOFSQUARE+SIZEOFSQUARE/2)),radius)
                elif board[row][col]==2:
                    pygame.draw.circle(screen,yellow,(int(col*SIZEOFSQUARE+SIZEOFSQUARE/2),height-int(row*SIZEOFSQUARE+SIZEOFSQUARE/2)),radius)
    pygame.display.update()
switch=0 #to turn play to another player
GameOver = False

########pygame utilities###################
pygame.init()
SIZEOFSQUARE = 100
width = COLUMNS*SIZEOFSQUARE
height = (ROWS+1) * SIZEOFSQUARE
size = (width,height)
radius = int(SIZEOFSQUARE/2 -5)
screen = pygame.display.set_mode(size)
draw(board)
pygame.display.update()
font = pygame.font.SysFont("monospace",75)

########pygame utilities###################





while  (GameOver==False):

    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## 3shan lma ndos 3la X y5rgny mn el window
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black,(0,0,width, SIZEOFSQUARE))
            posx= event.pos[0]
            if switch ==0:
                pygame.draw.circle(screen,red,(posx, int(SIZEOFSQUARE/2)),radius)
            else:
                pygame.draw.circle(screen,yellow,(posx, int(SIZEOFSQUARE/2)),radius)
        pygame.display.update()
            


        if event.type == pygame.MOUSEBUTTONDOWN:
             pygame.draw.rect(screen, black,(0,0,width, SIZEOFSQUARE))
            #print(event.pos)
            #continue
            # #Player 1 play:
             if switch == 0:
                 posx=event.pos[0]
                 
                 select = int(math.floor(posx/SIZEOFSQUARE)) #int(input("Select (player 1) from 0-6: "))
                 switch = 1
                 if isValid(board,select):
                     row =GetNextRow(board,select)
                     SetPiece(board,row,select,1)
                     if winning_move(board,1):
                         label = font.render("Player 1 wins",1,red)
                         screen.blit(label,(40,10))
                         GameOver=True
            #
            #      #print(select)
            #
            # # Player 2 play:
             else:
                 posx=event.pos[0]
                 select =int(math.floor(posx/SIZEOFSQUARE)) #int(input("Select (player 2) from 0-6: "))
                 switch = 0
                 if isValid(board,select):
                     row = GetNextRow(board,select)
                     SetPiece(board,row,select,2)
                     if winning_move(board, 2):
                        label = font.render("Player 2 wins",1,yellow)
                        screen.blit(label,(40,10))
                        GameOver=True
            
             printBoard(board)
             draw(board)
    


         
             










