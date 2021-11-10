import pygame
from pygame import draw
from pygame import display
from pygame.constants import QUIT
import requests
import time

size = 460
back = 255, 183, 3
qText = 2, 48, 71
aText = 202, 103, 2
winText = 255, 255, 255
border = 0, 95, 115

def getNewBoard():
    board = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']  #GET BOARD
    # board = [                         #EXAMPLE BOARD
    #     [7,8,0,4,0,0,1,2,0],
    #     [6,0,0,0,7,5,0,0,9],
    #     [0,0,0,6,0,1,0,7,8],
    #     [0,0,7,0,4,0,2,6,0],
    #     [0,0,1,0,5,0,9,3,0],
    #     [9,0,4,0,6,0,0,0,5],
    #     [0,7,0,3,0,0,0,1,2],
    #     [1,2,0,0,0,7,4,0,0],
    #     [0,4,9,2,0,6,0,0,7]
    # ]
    boardCopy = [[board[i][j] for j in range(len(board))] for i in range(len(board))]   #CREATE A COPY OF THE BOARD
    return board, boardCopy

def getEmpty(board):    #GET NEXT EMPTY POSITION
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return (i, j)   
    return None

def valid(board, pos, guess):   #CHECK IF POSITION IS VALID
    row = pos[0]    
    col = pos[1]    
    for i in range(len(board[row])):
        if board[row][i] == guess:
            return False
    for i in range(len(board)):
        if board[i][col] == guess: 
            return False
    i = row//3
    j = col//3
    for k in range(i*3, i*3 + 3):
        for l in range(j*3, j*3 + 3):
            if board[k][l] == guess: 
                return False
    return True

def solve(board, boardCopy, display, font):     # RECURSIVELY SOLVE BOARD
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            return
    pos = getEmpty(board)
    if not pos:
        win(display)
        return True
    for guess in range(1, 10):
        if valid(board, pos, guess):
            row = pos[0]
            col = pos[1]
            print_digit(board, boardCopy, guess, row, col, display, font)
            board[row][col] = guess
            if solve(board, boardCopy, display, font):
                return True
            board[row][col] = 0
    return False

def print_digit(board, boardCopy, digit, i, j, display, font):  # WRITES A DIGIT ON PYGAME WINDOW
    print_board(board, boardCopy, aText, display, font)
    val = font.render(str(digit), True, aText)
    display.blit(val, (20+50*j, 50*i))
    pygame.display.update()
    pygame.time.wait(100)

def print_board(board, boardCopy, color, display, font):    #DISPLAYS BOARD
    drawGrid(display)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                val = font.render(str(board[i][j]), True, color)
                display.blit(val, (20+50*j, 5+50*i))
    for i in range(len(boardCopy)):
        for j in range(len(boardCopy[i])):
            if boardCopy[i][j] > 0:
                val = font.render(str(boardCopy[i][j]), True, qText)
                display.blit(val, (20+50*j, 5+50*i))
    pygame.display.update()

def drawGrid(display):          #DRAW INITIAL EMPTY GRID
    color = border
    display.fill(back)
    pygame.display.flip()

    pygame.draw.line(display, color, (5, 5), (5, 455), 6)
    pygame.draw.line(display, color, (5, 5), (455, 5), 6)
    pygame.draw.line(display, color, (455, 455), (5, 455), 6)
    pygame.draw.line(display, color, (455, 455), (455, 5), 6)
    
    for i in range(9):
        if (i+1) % 3 == 0:
            pygame.draw.line(display, color,
                             (55+50*i, 5), (55+50*i, 455), 6)
            pygame.draw.line(display, color, (5, 55+50*i), (455, 55+50*i), 6)
        else:
            pygame.draw.line(display, color,
                             (55+50*i, 5), (55+50*i, 455), 2)
            pygame.draw.line(display, color,
                             (5, 55+50*i), (455, 55+50*i), 2)
    pygame.display.update()

def addNum(display, font, pos, board, boardCopy):         # PLAYER INSERTS DIGIT ON BOARD
    i, j = pos[0]//50, pos[1]//50
    if((i, j) == (4, 9)):
        solve(board, boardCopy, display, font)
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                num = event.key - 48
                if num == 0 and num not in boardCopy:
                    pygame.draw.rect(display, back, (i*50+8, j*50+8, 46, 46))
                    pygame.display.update()
                    board[j][i] = 0
                    print(board)
                    return
                else:
                    if not boardCopy[j][i]:
                        if not valid(board, (j, i), num):
                            val = font.render("x", True, (255, 0, 0))
                            display.blit(val, (i*50+20, j*50+4))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            pygame.draw.rect(display, back, (i*50+8, j*50+8, 46, 46))
                        else:
                            val = font.render(str(num), True, aText)
                            display.blit(val, (i*50+18, j*50+8))
                            board[j][i] = num
                            if not getEmpty(board):
                                win(display)
                        pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()[0]//50, pygame.mouse.get_pos()[1]//50
                if((x, y) == (4, 9)):
                    for i in range(len(board)):
                        for j in range(len(board[i])):
                            board[i][j] = boardCopy[i][j]
                    solve(board, boardCopy, display, font)
                else: i, j = x, y

def win(display):
    print("Win")
    font = pygame.font.SysFont('Verdana', 80)
    var = font.render("WIN", True, winText)
    display.blit(var, (150, 150))
    pygame.display.update()
    pygame.draw.rect(display, border, (190, 475, 80, 30), border_radius=7)
    font2 = pygame.font.SysFont("Verdana", 20)
    val = font2.render("Retry", True, (255, 255, 255))
    display.blit(val, (200, 477))
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                i, j = pygame.mouse.get_pos()[0]//50, pygame.mouse.get_pos()[1]//50
                if (i, j) == (4, 9):
                    pass

def main():
    board, boardCopy = getNewBoard()
    pygame.init()
    display = pygame.display.set_mode((size, size+50))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont("Verdana", 40)       # SET FONT
    print_board(board, boardCopy, qText, display, font)     #CREATES PYGAME WINDOW AND DISPLAYS BOARD

    pygame.draw.rect(display, border, (190, 475, 80, 30), border_radius=7)
    font2 = pygame.font.SysFont("Verdana", 20)
    val = font2.render("Solve", True, (255, 255, 255))
    display.blit(val, (200, 477))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                addNum(display, font, pos, board, boardCopy)      

if __name__ == "__main__":
    main()