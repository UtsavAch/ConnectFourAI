#Function to check the winner
# Takes argument board
# Returns
# 'X' if X is the winner
# 'O' if O is the winner
# 'tie' if all cells are filled and noone is the winner
# None if noone is winner
#############################
def check_winner(board):
    # Check horizontally
    for row in range(6):
        for col in range(4):
            if (
                board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]
                and board[row][col] != ' '
            ):
                return board[row][col]
    # Check vertically
    for row in range(3):
        for col in range(7):
            if (
                board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]
                and board[row][col] != ' '
            ):
                return board[row][col]
    # Check diagonally (from bottom-left to top-right)
    for row in range(3, 6):
        for col in range(4):
            if (
                board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]
                and board[row][col] != ' '
            ):
                return board[row][col]
    # Check diagonally (from top-left to bottom-right)
    for row in range(3):
        for col in range(4):
            if (
                board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]
                and board[row][col] != ' '
            ):
                return board[row][col]
    # Check for tie
    if all(board[row][col] != ' ' for row in range(6) for col in range(7)):
        return "tie"
    # When noone is the winner
    return None