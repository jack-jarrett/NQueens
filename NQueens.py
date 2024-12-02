import random
import time

# Constants
INF = float('inf')
N = 10000  # Number of queens

# Board and conflict tracking
def initialize():
    global queens, col_count, upper_diag_count, lower_diag_count

    queens = [-1] * N
    col_count = [0] * N
    upper_diag_count = [0] * (2 * N - 1)
    lower_diag_count = [0] * (2 * N - 1)

    # Place the first queen randomly
    queens[0] = random.randint(0, N - 1)
    col_count[queens[0]] += 1
    upper_diag_count[queens[0]] += 1
    lower_diag_count[N - queens[0] - 1] += 1

    # Place the remaining queens with minimum conflicts
    for i in range(1, N):
        min_conflict_cols = []
        min_conflicts = INF

        for j in range(N):
            conflicts = (
                col_count[j] 
                + upper_diag_count[j + i]
                + lower_diag_count[N - j + i - 1]
            )

            if conflicts < min_conflicts:
                min_conflicts = conflicts
                min_conflict_cols = [j]
            elif conflicts == min_conflicts:
                min_conflict_cols.append(j)

        queens[i] = random.choice(min_conflict_cols)
        col_count[queens[i]] += 1
        upper_diag_count[queens[i] + i] += 1
        lower_diag_count[N - queens[i] + i - 1] += 1

def board_conflicts(exclude_row=-1):
    """Returns the total number of conflicts on the board."""
    conflicts = 0
    temp_col_count = [0] * N
    temp_upper_diag_count = [0] * (2 * N - 1)
    temp_lower_diag_count = [0] * (2 * N - 1)

    for i in range(N):
        if i != exclude_row:
            col = queens[i]
            temp_col_count[col] += 1
            temp_upper_diag_count[col + i] += 1
            temp_lower_diag_count[N - col + i - 1] += 1

    # Calculate conflicts for columns and diagonals
    for count in temp_col_count:
        if count > 1:
            conflicts += count * (count - 1) // 2
    for count in temp_upper_diag_count:
        if count > 1:
            conflicts += count * (count - 1) // 2
    for count in temp_lower_diag_count:
        if count > 1:
            conflicts += count * (count - 1) // 2

    return conflicts

def highest_conflicts():
    """Finds the row with the highest number of conflicts."""
    max_conflicts = -1
    max_conflict_rows = []

    for i in range(N):
        col = queens[i]
        conflicts = (
            col_count[col] - 1
            + upper_diag_count[col + i] - 1
            + lower_diag_count[N - col + i - 1] - 1
        )

        if conflicts > max_conflicts:
            max_conflicts = conflicts
            max_conflict_rows = [i]
        elif conflicts == max_conflicts:
            max_conflict_rows.append(i)

    return random.choice(max_conflict_rows)

def min_conflicts():
    """Moves a queen to the column with the least conflicts."""
    row = highest_conflicts()
    min_conflicts = INF
    min_conflict_cols = []

    for col in range(N):
        conflicts = (
            col_count[col]
            + upper_diag_count[col + row]
            + lower_diag_count[N - col + row - 1]
        )

        if conflicts < min_conflicts:
            min_conflicts = conflicts
            min_conflict_cols = [col]
        elif conflicts == min_conflicts:
            min_conflict_cols.append(col)

    new_col = random.choice(min_conflict_cols)

    # Update conflict tracking
    old_col = queens[row]
    col_count[old_col] -= 1
    upper_diag_count[old_col + row] -= 1
    lower_diag_count[N - old_col + row - 1] -= 1

    queens[row] = new_col
    col_count[new_col] += 1
    upper_diag_count[new_col + row] += 1
    lower_diag_count[N - new_col + row - 1] += 1

def write_board():
    """Writes the board configuration to a file."""
    board = [['.' for _ in range(N)] for _ in range(N)]

    for i in range(N):
        board[i][queens[i]] = 'Q'  # Place queens on the board

    with open("nqueens_solution.txt", "w") as file:
        for row in board:
            file.write(' '.join(row) + '\n')
        file.write("\n")

def main():
    """Main function to solve the N-Queens problem."""
    print(f"Number of queens: {N}")
    print("Initializing board...")
    start_time = time.time()

    initialize()

    initial_conflicts = board_conflicts()
    print(f"Initial conflicts: {initial_conflicts}\n")

    print("Solving...")
    steps = 0
    while board_conflicts() > 0:
        min_conflicts()
        steps += 1

        if steps % 1000 == 0:
            print(f"Step {steps}, conflicts: {board_conflicts()}")

    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000  # in milliseconds

    print(f"Solved in {steps} steps and {elapsed_time:.2f}ms.\n")
    write_board()

if __name__ == "__main__":
    main()
