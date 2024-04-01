import math
from check_winner import check_winner

# Constants
WIN_SCORE = 100000
DEPTH = 5  # Increased depth for deeper search
BLOCKING_SCORE = 10000  # Score for blocking opponent's winning moves

def evaluate_position(board, player):
    """
    Evaluate the score of a given board position for a player.

    Parameters:
    - board (list): The game board.
    - player (str): The player ('X' or 'O') for whom to evaluate the position.

    Returns:
    - score (int): The score representing the evaluation of the position for the player.
    """
    score = 0
    opponent = get_opponent(player)

    # Check horizontal
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            score += score_window(board[row][col:col+4], player, opponent)

    # Check vertical
    for col in range(len(board[0])):
        for row in range(len(board) - 3):
            window = [board[row+i][col] for i in range(4)]
            score += score_window(window, player, opponent)

    # Check diagonal (down-right)
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            window = [board[row+i][col+i] for i in range(4)]
            score += score_window(window, player, opponent)

    # Check diagonal (up-right)
    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            window = [board[row-i][col+i] for i in range(4)]
            score += score_window(window, player, opponent)

    return score

def score_window(window, player, opponent):
    """
    Calculate the score for a window of 4 tokens.

    Parameters:
    - window (list): The window of 4 tokens to evaluate.
    - player (str): The player ('X' or 'O') for whom to calculate the score.
    - opponent (str): The opponent player ('X' or 'O').

    Returns:
    - score (int): The score for the given window.
    """
    score = 0
    if window.count(player) == 4:
        score += WIN_SCORE
    elif window.count(player) == 3 and window.count(' ') == 1:
        score += 1000
    elif window.count(player) == 2 and window.count(' ') == 2:
        score += 100
    if window.count(opponent) == 3 and window.count(' ') == 1:
        if window.count(player) == 0:
            score -= BLOCKING_SCORE  # Penalize opponent's potential winning moves
        else:
            score += WIN_SCORE  # Prioritize winning over blocking opponent's winning move
    return score

def minimax(board, depth, maximizing_player, player, alpha, beta):
    """
    Perform minimax search with alpha-beta pruning.

    Parameters:
    - board (list): The game board.
    - depth (int): The current depth of the search.
    - maximizing_player (bool): Indicates whether the player is maximizing or minimizing.
    - player (str): The current player ('X' or 'O').
    - alpha (float): The alpha value for alpha-beta pruning.
    - beta (float): The beta value for alpha-beta pruning.

    Returns:
    - eval (int): The evaluation score of the board position.
    """
    if depth == 0 or game_over(board):
        return evaluate_position(board, player)

    if maximizing_player:
        max_eval = -math.inf
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                row = get_next_open_row(board, col)
                temp_board = [row[:] for row in board]
                temp_board[row][col] = player
                eval = minimax(temp_board, depth - 1, False, player, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                row = get_next_open_row(board, col)
                temp_board = [row[:] for row in board]
                temp_board[row][col] = get_opponent(player)
                eval = minimax(temp_board, depth - 1, True, player, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def is_valid_move(board, col):
    """
    Check if a move is valid in a given column.

    Parameters:
    - board (list): The game board.
    - col (int): The column index to check.

    Returns:
    - valid (bool): True if the move is valid, False otherwise.
    """
    return board[0][col] == ' '

def get_next_open_row(board, col):
    """
    Get the row where a token would fall in a given column.

    Parameters:
    - board (list): The game board.
    - col (int): The column index.

    Returns:
    - row (int): The row index where the token would fall.
    """
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            return row

def game_over(board):
    """
    Check if the game is over.

    Parameters:
    - board (list): The game board.

    Returns:
    - over (bool): True if the game is over, False otherwise.
    """
    return check_winner(board) is not None

def get_opponent(player):
    """
    Get the opponent player.

    Parameters:
    - player (str): The current player ('X' or 'O').

    Returns:
    - opponent (str): The opponent player ('X' or 'O').
    """
    return 'O' if player == 'X' else 'X'

def best_move(board, player):
    """
    Find the best move using minimax algorithm with alpha-beta pruning.

    Parameters:
    - board (list): The game board.
    - player (str): The current player ('X' or 'O').

    Returns:
    - best_col (int): The column index of the best move.
    """
    best_score = -math.inf
    alpha = -math.inf
    beta = math.inf
    max_score_columns = []  # Store columns with the highest score

    for col in range(len(board[0])):
        if is_valid_move(board, col):
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            temp_board[row][col] = player
            score = minimax(temp_board, DEPTH - 1, False, player, alpha, beta)
            print(col, score)
            if score > best_score:
                best_score = score
                max_score_columns = [col]  # Reset max_score_columns
            elif score == best_score:
                max_score_columns.append(col)  # Add column to max_score_columns
            alpha = max(alpha, best_score)
    # print(max_score_columns) #List of columns with maximum scores

    # If there are multiple columns with the same highest score
    # Checks if opponent is going to win in the next move and tries to block it
    # Chooses the best column among those highest score columns 
    if len(max_score_columns) > 1:
        # Check if there's a move that blocks opponent's winning move
        for col in max_score_columns:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            temp_board[row][col] = get_opponent(player)
            if game_over(temp_board):
                print("Opponent was about to win!")
                print(col)
                return col  # Block opponent's winning move

    return max_score_columns[0] if max_score_columns else None
