from flask import Flask, render_template, jsonify, request
import random #Just for the demo of AI move. Will be removed after AI implementation

app = Flask(__name__)

# Function to initialize the game board
def initialize_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

# Initialize the game board
board = initialize_board()
current_player = 'X'

# Initialize scores 
player_score = 0
ai_score = 0


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
# For now, this is just a simple implementation of AI
# where it choses a vacant cell(cell without 'X' or 'O' already),
# We are just using a random module(import random)
# Therefore, for now, the AI only choses a random vacant cell
# Later, when we implement an actual AI, we will change the code inside ai_move() function
# If we need to make a separate class we will create a new python file and apply the class methods here
######################################################
def ai_move():
    # Implement your AI logic here
    # For now, the AI makes a random valid move
    valid_moves = [col for col in range(7) if board[0][col] == ' ']
    return random.choice(valid_moves)
######################################################
######################################################

@app.route("/")
def index():
    return render_template("index.html")

# Click "New game" button to see its function 
@app.route("/reset_all")
def reset():
    global board, player_score, ai_score, current_player
    board = initialize_board()
    player_score = 0
    ai_score = 0
    current_player = 'X'
    return jsonify({'board': board, 'winner': None, 'player_score': player_score, 'ai_score': ai_score})

# Click "Next round" buttion to see its function
@app.route("/reset_board")
def board_reset():
    global board, player_score, ai_score, current_player
    board = initialize_board()
    current_player = 'X'
    return jsonify({'board': board, 'winner': None, 'player_score': player_score, 'ai_score': ai_score})

##################################
# Player's and AI's moves
@app.route("/move")
def move():
    global current_player, player_score, ai_score
    col = int(request.args.get('col'))
    
    # Player move
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = current_player
            break
    
    # Check for a winner after player's move
    winner = check_winner()
    if winner:
        player_score += 1
        return jsonify({'board': board, 'winner': winner, 'player_score': player_score, 'ai_score': ai_score, 'winner_message': f'{winner} won the round'})

    # AI move
    ai_col = ai_move()
    for row in range(5, -1, -1):
        if board[row][ai_col] == ' ':
            board[row][ai_col] = 'O'
            break
    
    print(board)
    # Check for the winner after ai's move
    winner = check_winner()
    if winner:
        ai_score += 1
        return jsonify({'board': board, 'winner': winner, 'player_score': player_score, 'ai_score': ai_score, 'winner_message': f'{winner} won the round'})

    if winner == 'X':
        player_score += 1
        winner_message = 'X won the round'
    elif winner == 'O':
        ai_score += 1
        winner_message = 'O won the round'
    else:
        winner_message = None

    # Check for game winner
    if player_score == 3:
        winner_message = 'X is the winner'
    elif ai_score == 3:
        winner_message = 'O is the winner'

    return jsonify({'board': board, 'winner': winner, 'player_score': player_score, 'ai_score': ai_score, 'winner_message': winner_message})
#######################################

if __name__ == "__main__":
    app.run(debug=True)
    