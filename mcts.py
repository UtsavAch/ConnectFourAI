import time
import math
import copy
import random


# class node is going to be the base for the mcts, since we neeed statistics tree, the nodes are going to represent the state of the game 
#as well as its structure meaning the child nodes of an node are the possible plays from said node 
class Node:
    def __init__(self,state,father_node):
        self.state=state
        self.n_visits=0
        self.n_victories=0
        self.father_node=father_node
        self.childs=[]
        
    
    def __str__(self):
        return f'''Board: {self.state[0]}
       {self.state[1]}
       {self.state[2]}
       {self.state[3]}
       {self.state[4]}
       {self.state[5]}

        Number of visits: {self.n_visits} 
        Number of victories: {self.n_victories}
        Number of childs nodes: {len(self.childs)}'''
    
class Tree:


    def __init__(self,state):
        self.root=Node(state,None)


#recursive functions to find the lefs of a specific node in a tree or the entire tree
    def find_leaf(self,node,leafs):
        if(node.childs==[]):
            leafs.extend([node])
            return
        
        for child in node.childs:
            self.find_leaf(child,leafs)
            
    
    def find_leafs(self):
        current_node=self.root
        leafs=[]
        self.find_leaf(current_node,leafs)
        return leafs
        
    
# this function recives the entire tree and chooses and leaf node to exapand
# it chooses the node to expand having the ucb1 formula into consederation
# we did alter it in comparation to the given in class, since it was not giving the expected results
# after some debbuging we came to the conclusion that this formula suits our algorithm better  
def select_node_to_expand(tree):
    not_expanded_nodes=tree.find_leafs()
    ucb1_best=-float("inf")
    node_to_expand=None
    for node in not_expanded_nodes:
        if (node==tree.root):
            return node#divisions by 0 only happen when the only leaf at the moment is the root (this is because in the first selection none simulation has occured, however in the following selections every leafs(expanded node) will be simulated as well as visited)
        if(node.father_node==tree.root):#we want all initial ways to be expanded atleast one time
            ucb1=float("inf")
            if(ucb1>ucb1_best):
                node_to_expand=node
                ucb1_best=ucb1
        elif(check_winner(node.state)==-1): # we don't want terminal nodes being expanded since that woudn't make sense and only waist computational power to do so
            ucb1=node.n_victories/node.n_visits+ 1.41*math.sqrt(2*node.n_visits/math.log(node.father_node.n_visits)) # changed so that the exploration part actualy gives a bigger number to nodes that were explored less times
            if(ucb1>ucb1_best):
                node_to_expand=node
                ucb1_best=ucb1
        
    return node_to_expand

def is_board_full(board):
    for col in board[0]:
        if(col==' '):
            return False
    return True

def make_move(state, col,player):
    count=len(state)-1
    while(state[count][col]!=' ' and count>=0):
        count-=1
    if(count<0):#check if the colum is full we can't make an move in that col
        return -1#alert the expand_node func that that col cannot be played so an node corresponding to that move will not be created ( others funcs that use this make_move will also be alerted) 
    state[count][col]=player
    return 0


#this function works by creating a node to each possible AI play,then it choses an random player for the human player 
#so that the state of the node that is appended is always an board in which the next player is the IA 
def expand_node(node):
    #first we have expand the node with the possible plays that the AI can do from the given state
    for i in range (7):
        new_state= copy.deepcopy(node.state)
        if(make_move(new_state,i,"O")==0):
            while True:
                col = random.randint(0, 6)
                if (make_move(new_state, col, "X") == 0) or is_board_full(new_state):
                    break
            node.childs.append(Node(new_state,node))

#this function checks if an specif part of the board has 4 X's or O's, it is an auxiliary function to the check_winner 
def check_token(board,x,y, x_incr, y_incr, player):
    if(x+3*x_incr>=len(board[0]) or x+3*x_incr<0 or y+3*y_incr>=len(board) or y+3*y_incr<0): # checks if the position given can be used to check the direction desired (if it isn't going to give error of array ot of index)
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

    if(num_not_player==4):
        return -1
    elif (num_player==4):
        return 1
    else:
        return 0

#this function verifys if the board is an terminal state, meaning if either the AI or the human player won, or if the board is full
def check_winner(board):
    for row in range (len(board)):
        for col in  range (len(board[0])):
            result=check_token(board,col,row,1,0,"O")
            if(result==1):
                return 1
            elif(result==-1):
                return 0
            result=check_token(board,col,row,0,1,"O")
            if(result==1):
                return 1
            elif(result==-1):
                return 0
            result=check_token(board,col,row,1,1,"O")
            if(result==1):
                return 1
            elif(result==-1):
                return 0
            result=check_token(board,col,row,-1,1,"O")
            if(result==1):
                return 1
            elif(result==-1):
                return 0   

    if(is_board_full(board)):
        return 0
     
    return -1
    
    
#this function simulates an game with random moves until it reaches an terminal state, then returns the results as an win for the AI or not
def simulate(node):
    board=copy.deepcopy(node.state)
    result=check_winner(board)
    player="O"
    while (result==-1):
        random.seed(time.time())
        num=random.randint(0,6)
        if(make_move(board,num,player)==0):# it was possible to actualy make the move so we change the player
            if(player=="O"):
                player="X"
            elif(player=="X"):
                player="O"
        result=check_winner(board)

    return result

# this function updates the statistics tree with the information from the function simulate
def backpropagate(node, result):
    if (node==None):
        return
    node.n_visits+=1
    node.n_victories+=result
    backpropagate(node.father_node,result)


# this function basicly takes the child nodes from the node_to_expand and simulates and 100 games from the state saved in the node
# we choose to run 100 simulation on each node so that each time we have to select a new node to expand we have more reliable infomation
def simulate_and_backpropagate(nodes):
    for node in nodes:
        for _ in range(100):
            result=simulate(node)
            backpropagate(node,result)

# this function serves to find where the AI played without having to always have that information stored,
# as the board is small and this function is only run once every time the mcts is called, we considered that
# it wouldn't impact the performance 
def find_col(current_board, board_2):
    for row in range(len(current_board)):
        for col in range(len(current_board[0])):
            if(current_board[row][col]!=board_2[row][col] and board_2[row][col]=="O"):
                return col

#mcst algorithm that chooses the best play based on a statitics tree, it has 5 sec to do the simulation then it chooses the most likely play to lead to a win
# since in the expand node the human player is considered to be making random plays it is expected that sometimes it is going to make thw worng play
# mainly when the board is fuller, could be correted with the use of the a* algorithm to make does plays instead of random  
def best_move (state, _):
    current_board=Tree(state)
    timeout=5
    start_time=time.time()
    while(time.time()-start_time<timeout):
        node_to_expand=select_node_to_expand(current_board)
        if(node_to_expand==None):# if all the leafs are not selectable that means that the all of them are in a terminal state, so we can't expand them nor simulate them
            break    
        expand_node(node_to_expand) #expands the choosen node and grows the tree to have information about new states of the game that are not only possible but always represent the next player as the AI(meaning it's AI turn to play)
        nodes_to_simulate=[]
        current_board.find_leaf(node=node_to_expand,leafs=nodes_to_simulate)
        simulate_and_backpropagate(nodes_to_simulate)
        print(time.time()-start_time)
        if(time.time()-start_time>timeout):
            break
    
    max=-1
    max_child=None
    for child in current_board.root.childs:
        value=child.n_victories/child.n_visits
        if value>max:
            max=value
            max_child=child
    
    return find_col(current_board.root.state,max_child.state)
    








