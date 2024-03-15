# This function is given:
#   - a position of the board ((x,y) that are the cols and rows respctively)
#   - the board
#   - the player
#   - the direction that is supposed to chack ((x_incr,y_incr) they the represent the vector that is going to search) 
#
# This function starts in the board position given and increments the positions according to the vector
# and checks if the position is the player or not the player, counting the number of player and not player
# posiotions in a token (line of four position in a direction(direction of the vector)), then gives points
# according to the qauntity of each

def check_token(board,x,y, x_incr, y_incr, player):
    if(x+4*x_incr>=len(board[0]) or x+4*x_incr<0 or y+4*y_incr>=len(board) or y+4*y_incr<0): # checks if the position given can be used to check the direction desired (if it isn't going to give error of array ot of index)
        return 0
    num_player=0
    num_not_player=0
    for i in range(4):                                                                       # moves in the token 
        if(board[y][x]!=player and board[y][x]!=' '):                                        # checks if the position is not a player
            num_not_player+=1                                                                # counting not players and players
        elif (board[y][x]==player):
            num_player+=1
        x+=x_incr
        y+=y_incr
    
    if((num_player>0 and num_not_player>0) or (num_player==0 and num_not_player==0)):                                                   # giving points according to the heuristic given by the professor
        return 0                                                                             # (depending on the ammount of players or not players on a token)
    elif(num_not_player>0):
        match(num_not_player):
            case(1):
                return -1
            case (2):
                return -10
            case (3):
                return -50
            case (4):
                return -512
    else:
        match(num_player):
            case(1):
                return 1
            case (2):
                return 10
            case (3):
                return 50
            case (4):
                return 512


# This function is the heuristic it is given
#   - the board
#   - the current player
#
# This function goes to all the positions in the board and calls check token in all directions necessary (down, right, down diagonals (only this 
# are necessary because if we check all positions in all directions we are going to check the same token more than once for example:
#                                                                                                               - - - - X
#                                                                                                               - - - X -
#                                                                                                               - - X - -
#                                                                                                               - X - - -
#                                                                                                               - - - - -
# this token would be checked twice once in the position [0,4] direction diagonal down left, and in the position [3,1] direction diagonal up right))
# After checking an token it adds it's value to the total value, that is going to be returned in the end as the value for the whole board     


def heuristic_1(board, player):
    total_value=0
    for row in range (len(board)):
        for col in  range (len(board[0])):
            total_value+=check_token(board,col,row,1,0,player)
            total_value+=check_token(board,col,row,0,1,player)
            total_value+=check_token(board,col,row,1,1,player)
            total_value+=check_token(board,col,row,-1,1,player)

    return total_value

# This function is given:
# - a copy of the current board
# - the col in which we want to play
# - the current player
#
# This function makes an move on the copy of the board so that it is used to calculate that said value would have if it was played on the real board.
# It goes up in rows in the chosen col until it has an open position to put the char representing the player, then it returns the copied board that was modified


def make_temp_move(board_temp, x, player):
    y=len(board_temp)-1
    while(board_temp[y][x]!=' ' and y>=0):
        y-=1
    if(y>=0):                                                                                           # if to ensure in case of full col that it doesn't
        board_temp[y][x]=player                                                                         # overwrite

    return board_temp

# This function is given:
#   - a list of values
#
# This function returns the index of the max value, which correspond to the col in which the AI is going to play


def max_val_index(values):
    max= values[0]
    index=0
    for i in range (1,len(values)):
        if(values[i]>max):
            max=values[i]
            index=i
    
    return index

# This function is given:
#   - the board
#   - the current player
#
# This function creates a copy of the board to each possible play (one for each col if the col is not full) so that to make the possible plays and evaluate
# them we don't modify the original board. It calls the make_temp_move to make the temporary boards and calls the heuristic to evaluate it, then finaly choses
# the best one and returns the corresponding col to that play/move
def best_move(board,player):
    values=[]
    for col in range (len(board[0])):
        board_cp=[row[:] for row in board]
        board_cp=make_temp_move(board_cp,col,player)
        values.append(heuristic_1(board_cp,player))
    
    print(values)
    
    return max_val_index(values)




    
