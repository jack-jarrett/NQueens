def is_valid_solution(board):
    """checks for valid solution of the board"""

    n = len(board)  # The size of the board (number of queens)
    
    # Check for column conflicts (no two queens should be in the same column)
    if len(board) != len(set(board)):
        return False

    # Check for diagonal conflicts
    for i in range(n):
        for j in range(i + 1, n):
            if abs(i - j) == abs(board[i] - board[j]):
                return False

    return True


def read_board_from_file(filename):
    """Reads the board configuration from a text file."""
    board = []
    
    with open(filename, 'r') as file:
        for line in file:
            # Read each line, strip it of leading/trailing spaces and convert to an integer
            column = int(line.strip())
            board.append(column)
    
    return board


def main():
    filename = 'nqueens_verification.txt'
    
    # Read the board configuration from the file
    board = read_board_from_file(filename)
    
    # Check if the solution is valid
    if is_valid_solution(board):
        print("The solution is valid!")
    else:
        print("The solution is invalid!")


if __name__ == "__main__":
    main()
