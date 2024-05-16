
# knowledge representation of the game state.
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
space = '-'
white = 'W'
black = 'B'
boarder = '!'
disks = (space, black, white, boarder)
PLAYERS = {black: 'Black', white: 'White'}

# All possible moves
right=1
left=-1
up=-10
down=10
directions = (up, right, down, left)

# create the board

def first_board():
    board = [boarder] * 100
    for i in playable_spaces():
        board[i] = space
    board[44]=white
    board[45]=black
    board[54]=black
    board[55]=white
    return board

# to fill the board by index 
def playable_spaces():
  result=[ i for i in range(11,89) if 1<=(i % 10) <=8 ]
  return result

#print the board as string 
def display_board(board):
    board_element = ''
    
    # Add column numbers
    board_element = board_element + '  ' + ' '.join(map(str, range(1, 9))) + '\n'
    
    # Add rows with piece symbols
    for row in range(1, 9):
        row_begin = 10 * row + 1  #  first element of the row
        row_finish = 10 * row + 9  #  last element of the row
        row_elements = ' '.join(board[row_begin:row_finish]) # put row elements in row_elements veraibles and put spaces 
        board_element = board_element + f'{row} {row_elements}\n'  # put each row in the rep var
    
    return board_element

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Game controller

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Function to determine the opponent's color
def opponent(player):
    if player is white: 
        opp=black
    else:
        opp=white
    return opp

# Switch between players each move 
def switch_player( player, board):
    opp = opponent(player)
    if check_player_moves(opp, board):
        return opp
    elif check_player_moves(player, board):
        return player
    return None


# Function to check if a move is valid
def valid(moving_position):
    result=isinstance(moving_position, int) and moving_position in playable_spaces()
    return result


def all_possible_moves(player, board):
    result=[i for i in playable_spaces() 
        if legal_move(i, player, board)]
    return result

def check_player_moves(player, board):
    result =[any(legal_move(i, player, board)
        for i in playable_spaces())]
    return result

def legal_move(moving_position, player, board):
    if board[moving_position] != space:  # Check if the move is not an empty square
        return False
    for direction in directions:  # Assuming DIRECTIONS is a list of directions to check
            opp = opponent(player)
            temp=moving_position + direction
            if board[temp] is player:
                continue
            while board[temp] is opp:
                temp = temp+ direction
            if board[temp] is player:
                return True
            else:
                continue  # If at least one direction has a bracket, the move is legal
    return False



#///////////////////////////////////////////////////////////////////////////////////////////////////


def find_valiable_position(position, player, board, direction):
        valid_position = position + direction
        opp = opponent(player)
        if board[valid_position] is player:
            return None
        while board[valid_position] == opp:
            valid_position =valid_position+ direction
        if board[valid_position] == boarder or board[valid_position] == space:
            return None
        else:
            return valid_position


def make_flips(position, player, board, direction):
    valid_position = find_valiable_position(position, player, board, direction)
    if not valid_position:
        return
    temp = position + direction
    while temp != valid_position:
        board[temp] = player
        temp = temp + direction
        
    

def make_move(new, player, board):
    f=0
    opp=opponent(player)
    for direction in directions:
        if board[new + direction] ==opp:
            f=1
    if f==1 and board[new]==space:
        board[new] = player
        for direction in directions :
            make_flips(new, player, board, direction)
        return board
    return board

def next_move(player, board,depth):
    move = alpha_beta_strategy(player,board,depth)
    if move is None:
        move = 99  
    return move

#///////////////////////////////////////////////////////////////////////////////////////////////


def alpha_beta(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or not check_player_moves(player, board):
        return utility_function( player, board)
    if maximizing_player:
        max_eval = float('-inf')
        for move in all_possible_moves(player, board):
            new_board = make_move(move, player,  board.copy())
            eval = alpha_beta(new_board, depth - 1, alpha, beta, False, opponent(player))
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  
        return max_eval
    else:
        min_eval = float('inf')
        for move in all_possible_moves(player, board):
            new_board = make_move(move, player,  board.copy())
            eval = alpha_beta(new_board, depth - 1, alpha, beta, True, opponent(player))
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break 
        return min_eval

def alpha_beta_strategy(player, board, depth):
    legal_moves_list = all_possible_moves(player, board)
    if not legal_moves_list:
        return 99
    best_move = None
    if player==black:
        best_value = float("-inf")
    else:
        best_value=float('inf')

    for move in all_possible_moves(player, board):
        new_board = make_move(move, player,  board.copy())
        board_value = alpha_beta(new_board, depth, float('-inf'), float('inf'), False, opponent(player))
        if (player == black and board_value > best_value) or (player == white and board_value < best_value):
            best_value = board_value
            best_move = move
    return best_move

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#utitity_function 

def utility_function(player,board):
    opp = opponent(player)
    first= 0
    second = 0
    for index in playable_spaces():
        if board[index] == player:
            first =first + 1
        elif board[index] == opp:
            second = second + 1
            
    return first - second



def players_score(player, board):
    opp = opponent(player)
    second = 0 
    first = 0
    for i in playable_spaces():
        value = board[i]
        if value == player:
            first = first + 1
        elif value == opp:
            second = second+1
    print("black: "+str(first) +"  white: "+str(second))



#///////////////////////////////////////////////////////////////////

board=[ '!', '!', '!', '!', '!', '!', '!', '!', '!', '!',
        '!', '-', '-', '-', '-', '-', '-', '-', '-', '!',
        '!', '-', '-', '-', '-', '-', '-', '-', '-', '!',
        '!', '-', '-', '-', '-', '-', '-', '-', '-', '!',
        '!', '-', '-', '-', 'W', 'B', '-', '-', '-', '!',
        '!', '-', '-', '-', 'B', 'W', '-', '-', '-', '!',
        '!', '-', '-', '-', '-', '-', '-', '-', '-', '!',
        '!', '-', '-', '-', '-', '-', '-', '-', '-', '!',
        '!', '-', '-', '-', '-', '-', '-', '-', '-', '!',
        '!', '!', '!', '!', '!', '!', '!', '!', '!', '!']

# handle strateges

new_board =first_board()
player=black
depth=0
difficulty=input("choose which difficulty do you want easy, medium or hard ")

if difficulty == 'easy':
    depth = 1
elif difficulty == 'medium':
    depth = 3
elif difficulty == 'hard':
    depth = 5


while  player is not None and check_player_moves(white,new_board) and check_player_moves(black,new_board):
    print(display_board(new_board))
    print("All possible moves for player "+player)
    print(all_possible_moves(player, new_board))
    if not all_possible_moves(black,new_board) and not all_possible_moves(white,new_board):
        break
    if player==black:
        if not all_possible_moves(player,new_board):
            print("Skipped")
            player=switch_player(player,new_board)
            continue
        user_input=int(input("choose one of possible moves "))
        if user_input not in all_possible_moves(player,new_board):
            print("Please enter number form the possible moves")
            continue
        make_move(user_input,player,new_board)
        
    elif player==white:
        computer_move= int(next_move(player,new_board,depth))
        if computer_move == 99:
            player=switch_player(player,new_board)
            print("Skipped")
            continue
        print("computr play: "+ str(computer_move))
        make_move(computer_move,player,new_board)
    print("\n")
    players_score(black,new_board)
    player = switch_player(player,new_board)
    

print("Final board \n")
print(display_board(new_board))
players_score(black,new_board)
print("\n")

