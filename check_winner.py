def check_winner(board):
    """
    Checks the winner of the Connect Four game represented by the provided board.

    Args:
    - board (list of lists): The game board represented as a 2D list of characters.
                             Each cell may contain 'X', 'O', or ' ' (empty).

    Returns:
    - 'X' if player 'X' is the winner.
    - 'O' if player 'O' is the winner.
    - 'tie' if all cells are filled and no player wins.
    - None if no player has won yet.

    The function iterates through all rows, columns, and diagonals to check for four consecutive
    matching symbols ('X' or 'O'). It also checks for a tie when all cells are filled without a winner.
    """
    # Check horizontally
    for r in range(6):
        for c in range(4):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] != ' ':
                return board[r][c]

    # Check vertically
    for r in range(3):
        for c in range(7):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] != ' ':
                return board[r][c]

    # Check diagonally (from bottom-left to top-right)
    for r in range(3, 6):
        for c in range(4):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == board[r - 3][c + 3] != ' ':
                return board[r][c]

    # Check diagonally (from top-left to bottom-right)
    for r in range(3):
        for c in range(4):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == board[r + 3][c + 3] != ' ':
                return board[r][c]

    # Check for tie
    if all(board[r][c] != ' ' for r in range(6) for c in range(7)):
        return "tie"

    # No winner yet
    return None
