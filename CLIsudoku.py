def print_board(puzzle):
    for i in range(len(puzzle)):
        if i%3 == 0:
            print("-------------------------------")
        
        for j in range(len(puzzle[i])):
            if j%3 == 0:
                print("|", end="")
            if j==8:
                print(f" {puzzle[i][j]} ", end="|\n")
            else: print(f" {puzzle[i][j]} ", end="")
    print("-------------------------------")

def getEmpty(puzzle):
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                return (i, j)   
    return None

def valid(puzzle, pos, guess):
    row = pos[0]    
    col = pos[1]    
    for i in range(len(puzzle[row])):
        if puzzle[row][i] == guess:
            return False
    for i in range(len(puzzle)):
        if puzzle[i][col] == guess: 
            return False
    i = row//3
    j = col//3
    for k in range(i*3, i*3 + 3):
        for l in range(j*3, j*3 + 3):
            if puzzle[k][l] == guess: 
                return False
    return True

def solve(puzzle):
    pos = getEmpty(puzzle)
    if not pos:
        return True
    for guess in range(1, 10):
        if valid(puzzle, pos, guess):
            row = pos[0]
            col = pos[1]
            puzzle[row][col] = guess
            if solve(puzzle):
                return True
            puzzle[row][col] = 0
    return False

def main():
    puzzle = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]
    solve(puzzle)
    print_board(puzzle)

if __name__ == "__main__":
    main()