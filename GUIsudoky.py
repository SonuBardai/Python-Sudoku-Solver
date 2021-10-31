import pygame
import requests
import time

size = 460
back = 217, 237, 146
qText = 2, 48, 71
aText = 52, 160, 164
winText = 255, 77, 109
border = 2, 48, 71

def getEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                return (i, j)   
    return None

def valid(board, pos, guess):
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

def solve(board, boardCopy, display, font):
    pos = getEmpty(board)
    if not pos:
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

def print_digit(board, boardCopy, digit, i, j, display, font):
    print_board(board, boardCopy, aText, display, font)
    val = font.render(str(digit), True, aText)
    display.blit(val, (20+50*j, 10+50*i))
    pygame.display.update()
    pygame.time.wait(200)

def print_board(board, boardCopy, color, display, font):
    drawGrid(display)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] > 0:
                val = font.render(str(board[i][j]), True, color)
                display.blit(val, (20+50*j, 10+50*i))
    for i in range(len(boardCopy)):
        for j in range(len(boardCopy[i])):
            if boardCopy[i][j] > 0:
                val = font.render(str(boardCopy[i][j]), True, qText)
                display.blit(val, (20+50*j, 10+50*i))
    pygame.display.update()

def drawGrid(display):
    display.fill(back)
    pygame.display.flip()

    pygame.draw.line(display, border, (5, 5), (5, 455), 6)
    pygame.draw.line(display, border, (5, 5), (455, 5), 6)
    pygame.draw.line(display, border, (455, 455), (5, 455), 6)
    pygame.draw.line(display, border, (455, 455), (455, 5), 6)
    
    for i in range(9):
        if (i+1) % 3 == 0:
            pygame.draw.line(display, border,
                             (55+50*i, 5), (55+50*i, 455), 6)
            pygame.draw.line(display, border, (5, 55+50*i), (455, 55+50*i), 6)
        else:
            pygame.draw.line(display, border,
                             (55+50*i, 5), (55+50*i, 455), 2)
            pygame.draw.line(display, border,
                             (5, 55+50*i), (455, 55+50*i), 2)
    pygame.display.update()

def main():
    pygame.init()
    display = pygame.display.set_mode((size, size+50))
    pygame.display.set_caption("Sudoku")

    board = requests.get('https://sugoku.herokuapp.com/board?difficulty=easy').json()['board']
    board = [[0, 1, 0, 5, 9, 0, 3, 0, 6], [0, 3, 5, 1, 0, 0, 7, 0, 0], [0, 0, 9, 2, 3, 8, 1, 0, 5], [1, 0, 0, 0, 0, 9, 6, 0, 8], [0, 4, 0, 0, 8, 1, 0, 9, 0], [8, 0, 7, 0, 0, 0, 0, 5, 1], [0, 0, 0, 8, 0, 4, 0, 0, 0], [7, 0, 0, 9, 0, 0, 8, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2]]
    boardCopy = [[board[i][j] for j in range(len(board))] for i in range(len(board))]
    print(board)
    font = pygame.font.SysFont("Verdana", 40)

    print_board(board, boardCopy, qText, display, font)

    solve(board, boardCopy, display, font)

    print_board(board, boardCopy, winText, display, font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


if __name__ == "__main__":
    main()