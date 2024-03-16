from flask import Flask, render_template, jsonify, request
from a_star import best_move as best_move_a_star;
from mcts import best_move as best_move_mcts;
from minimax import best_move as best_move_minimax;

app = Flask(__name__)

# Function to initialize the game board
def initialize_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

# Initialize the game board
board = initialize_board()
current_player = 'X'
# cells_occupied = 0 #To track how many boxes are occupied

# Initialize scores 
player_one_score = 0
player_two_score = 0

#Function to check the winner
#############################
def check_winner():
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
    return None

######################################################
# IMPORTANT FUNCTION(ai_move())
######################################################
def ai_move():
    return best_move_a_star(board, "O")
######################################################
######################################################

@app.route("/")
def index():
    return render_template("index.html")

# Click "New game" button to see its function 
@app.route("/reset_all")
def reset():
    global board, player_one_score, player_two_score, current_player
    board = initialize_board()
    player_one_score = 0
    player_two_score = 0
    current_player = 'X'
    return jsonify({'board': board, 'winner': None, 'player_one_score': player_one_score, 'player_two_score': player_two_score})

# Click "Next round" buttion to see its function
@app.route("/reset_board")
def board_reset():
    global board, player_one_score, player_two_score, current_player
    board = initialize_board()
    current_player = 'X'
    return jsonify({'board': board, 'winner': None, 'player_one_score': player_one_score, 'player_two_score': player_two_score})

##################################
# Player's and AI's moves
@app.route("/move")
def move():
    global current_player, player_one_score, player_two_score
    col = int(request.args.get('col'))

# ////////////////////////////  
    # Player move
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = current_player
            break
# ///////////////////////////
    
    # Check for a winner after player's move
    winner = check_winner()
    if winner:
        player_one_score += 1
        if(player_one_score == 3):
            winner_message = "X is the winner"
        else:
            winner_message = "X won the round"
        return jsonify({'board': board, 'winner': winner, 'player_one_score': player_one_score, 'player_two_score': player_two_score, 'winner_message': winner_message})

# ////////////////////////////
    # AI move
    ai_col = ai_move()
    for row in range(5, -1, -1):
        if board[row][ai_col] == ' ':
            board[row][ai_col] = 'O'
            break
# ////////////////////////////

    # Check for the winner after ai's move
    winner = check_winner()
    if winner:
        player_two_score += 1
        if(player_two_score == 3):
            winner_message = "O is the winner"
        else:
            winner_message = "O won the round"
        return jsonify({'board': board, 'winner': winner, 'player_one_score': player_one_score, 'player_two_score': player_two_score, 'winner_message': winner_message})

    if winner == 'X':
        player_one_score += 1
        winner_message = 'X won the round'
    elif winner == 'O':
        player_two_score += 1
        winner_message = 'O won the round'
    else:
        winner_message = None
        
    return jsonify({'board': board, 'winner': winner, 'player_one_score': player_one_score, 'player_two_score': player_two_score, 'winner_message': winner_message})
#######################################

if __name__ == "__main__":
    app.run(debug=True)
    