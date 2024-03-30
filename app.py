from flask import Flask, render_template, jsonify, request
from check_winner import check_winner
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
match_option = None

# Initialize scores 
player_one_score = 0
player_two_score = 0

######################################################
# IMPORTANT FUNCTIONS(Player and AI moves)
######################################################
def player_move(board, col, player):
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            break

def ai_move(board, ai_type, player):
    if(ai_type == "a_star"):
        col = best_move_a_star(board, player)
    if(ai_type == "mcts"):
        col = best_move_mcts(board, player)
    if(ai_type == "minimax"):
        col = best_move_minimax(board, player)
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            break

######################################################
# Getting button clicked information from backend whenever match option buttons are clicked
@app.route("/button_clicked", methods=["POST"])
def button_clicked():
    global match_option
    button_name = request.json.get("buttonName")
    print(button_name)
    match_option = button_name
    return jsonify({"buttonName": button_name})

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
# Player one's and player two's moves
@app.route("/move")
def move():
    global board, current_player, player_one_score, player_two_score, match_option
    col = int(request.args.get('col'))

# ////////////////////////////  
    # Player one move
    match(match_option):
        case("player_vs_astar"):
            player_move(board, col, "X")
        case ("player_vs_minimax"):
            player_move(board, col, "X")
        case ("player_vs_mcts"):
            player_move(board, col, "X")
        case ("astar_vs_mcts"):
            ai_move(board, "a_star", "X")
        case ("mcts_vs_minimax"):
            ai_move(board, "mcts", "X")
# ///////////////////////////
    
    # Check for a winner after player one's move
    winner = check_winner(board)
    if(winner == "tie"):
        winner_message = "This is a draw"
    elif winner == "X":
        player_one_score += 1
        if(player_one_score == 3):
            winner_message = "X is the winner"
        else:
            winner_message = "X won the round"
        return jsonify({'board': board, 'winner': winner, 'player_one_score': player_one_score, 'player_two_score': player_two_score, 'winner_message': winner_message})

# ////////////////////////////
    # Player two move
    match(match_option):
        case("player_vs_astar"):
            ai_move(board, "a_star", "O")
        case ("player_vs_minimax"):
            ai_move(board, "minimax", "O")
        case ("player_vs_mcts"):
            ai_move(board, "mcts", "O")
        case ("astar_vs_mcts"):
            ai_move(board, "mcts", "O")
        case ("mcts_vs_minimax"):
            ai_move(board, "minimax", "O")
# ////////////////////////////

    # Check for the winner after player two's move
    winner = check_winner(board)
    if(winner == 'tie'):
        winner_message = "This is a draw"
    elif winner == 'O':
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
    elif winner == 'tie':
        winner_message = 'It is a draw'
    else:
        winner_message = None
        
    return jsonify({'board': board, 'winner': winner, 'player_one_score': player_one_score, 'player_two_score': player_two_score, 'winner_message': winner_message})
#######################################

if __name__ == "__main__":
    app.run(debug=True)
    