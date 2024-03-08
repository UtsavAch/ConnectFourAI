import random;

# After applying all the AI logic this method will return the valid move
# For now it is only using random module
# //////////
# For now, this is just a simple implementation of AI
# where it choses a vacant cell(cell without 'X' or 'O' already),
# We are just using a random module(import random)
# Therefore, for now, the AI only choses a random vacant cell
def valid_move(board):
    print(board) #Check the state of the board
    valid_moves = [col for col in range(7) if board[0][col] == ' ']
    print(random.choice(valid_moves))
    return random.choice(valid_moves)
    # This function gets board as an argument and returns the valid column
