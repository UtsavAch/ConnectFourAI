from check_winner import check_winner

# This function remains unchanged
def check_token(board, x, y, x_incr, y_incr, player):
    if (x + 4 * x_incr >= len(board[0]) or x + 4 * x_incr < 0 or y + 4 * y_incr >= len(board) or y + 4 * y_incr < 0):
        return 0
    num_player = 0
    num_not_player = 0
    for i in range(4):
        if (board[y][x] != player and board[y][x] != ' '):
            num_not_player += 1
        elif (board[y][x] == player):
            num_player += 1
        x += x_incr
        y += y_incr

    if ((num_player > 0 and num_not_player > 0) or (num_player == 0 and num_not_player == 0)):
        return 0
    elif (num_not_player > 0):
        match (num_not_player):
            case (1):
                return -1
            case (2):
                return -10
            case (3):
                return -50
            case (4):
                return -512
    else:
        match (num_player):
            case (1):
                return 1
            case (2):
                return 10
            case (3):
                return 50
            case (4):
                return 512


# This function remains unchanged
def heuristic_1(board, player):
    total_value = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            total_value += check_token(board, col, row, 1, 0, player)
            total_value += check_token(board, col, row, 0, 1, player)
            total_value += check_token(board, col, row, 1, 1, player)
            total_value += check_token(board, col, row, -1, 1, player)

    return total_value


# This function remains unchanged
def make_temp_move(board_temp, x, player):
    y = len(board_temp) - 1
    while (board_temp[y][x] != ' ' and y >= 0):
        y -= 1
    if (y >= 0):
        board_temp[y][x] = player

    return board_temp


# This function remains unchanged
def max_val_index(values):
    max_val = values[0]
    index = 0
    for i in range(1, len(values)):
        if (values[i] > max_val):
            max_val = values[i]
            index = i

    return index


# This function is the minimax algorithm
def minimax(board, depth, maximizing_player, player):
    if depth == 0 or game_over(board):
        return heuristic_1(board, player)

    if maximizing_player:
        max_eval = float('-inf')
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                temp_board = make_temp_move([row[:] for row in board], col, player)
                eval = minimax(temp_board, depth - 1, False, player)
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(len(board[0])):
            if is_valid_move(board, col):
                temp_board = make_temp_move([row[:] for row in board], col, get_opponent(player))
                eval = minimax(temp_board, depth - 1, True, player)
                min_eval = min(min_eval, eval)
        return min_eval


# This function remains unchanged
def is_valid_move(board, col):
    return board[0][col] == ' '


# This function remains unchanged
def game_over(board):
    return check_winner(board) is not None


# This function remains unchanged
def get_opponent(player):
    return 'O' if player == 'X' else 'X'


# This function remains unchanged
def best_move(board, player):
    depth = 4  # Define the depth here
    values = []
    for col in range(len(board[0])):
        if is_valid_move(board, col):
            board_cp = [row[:] for row in board]
            board_cp = make_temp_move(board_cp, col, player)
            values.append(minimax(board_cp, depth - 1, False, player))
    return max_val_index(values)