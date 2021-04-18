#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# what do I need to keep track of?
# game, players
# who starts first -- should be decided randomly
# find available moves


# define rules, i.e. if there is a mandatory jump


# # Checker's game simulation
# 

# In[134]:


# all the imports

from copy import deepcopy
import tabulate
import string


# In[185]:


class Checkers():
    
    def __init__(self, computer_turn, state = None):
        # use this representation because .... 
        # each list inside the list represents one row
        if state is not None:
            self.current_state = state
        else:
            self.current_state = self.create_board()
        #self.valid_moves = self.valid_moves()
        # at [0] value for maximizing and at [1] for minimizing player
        self.kings = [0,0]
        self.live_pieces_comp = 12
        self.live_pieces_hum = 12
        # changes at each iteration of the game
        # enable this one to be chosen at random at the beginning
        self.computer_turn = computer_turn
        # set to True if computer plays first and False otherwise
        if computer_turn:
            self.maximizing = True
        if not computer_turn:
            self.maximizing = False

    def create_board(self):
        # populate the board
        # do so in several steps to avoid overcomplicated list comprehension
        board = [[],[],[],[],[],[],[],[]]
        for row in board:
            for n in range(8):
                # '   ' serves as a placeholder for the 3 letter that stand for a position of any piece
                # will make the board easy to print (__str__ method)
                row.append('   ')
        
        # populate the board with pieces
        for r in range(3):
            for c in range(8):
                if (r + c) % 2 == 1:
                    # b stands for black; black is minimizing
                    board[r][c] = ("b" + str(r) + str(c))
        for r in range(5, 8, 1):
            for c in range(8):
                if (r + c) % 2 == 1:
                    # w stands for white; white is maxiimizing 
                    board[r][c] = ("w" + str(r) + str(c))
        return board
        
    
    def valid_moves(self):
    
        # essentially check all the possible moves for computer
        # dependning on whether it is maximizing in this game (plays white)
        # or whether it is minimizing in this game
        # differentiate cases when a certain piece is a king
        if self.maximizing:
            print('here')
            letters = ['w','W']
            return self.moves(letters)
        elif not self.maximizing:
            letters = ['b', 'B']
            return self.moves(letters)
        
    def moves(self, letters):
        # a list to store all the potential moves
        moves = []
        jumps = []
        # counter to keep track of number of pieces for computer
        count = 0
        
        if 'b' in letters:
            rows, cols = range(8), range(8)
        else:
            rows, cols = range(7, -1, -1), range(7, -1, -1)
        # iterate over relevant cubicles of the board 
        for row in rows:
            for col in cols:  
                if self.current_state[row][col] == '   ':
                    continue
                count += 1
                # check for necessary jumps
                # rule in the checkers I play is that if there is a jump opportunity, you must jump
                jump_ex, jumpz =  self.necessary_jump(row, col)
                if jump_ex:
                    jumps = jumps + jumpz
                
                if letters[1] in self.current_state[row][col]:
                    potential_list = [[row+1,col+1],[row+1,col-1], [row-1,col+1],[row-1,col-1]]
                else:
                    # alternatively an if statement
                    potential = {'b': [[row+1,col+1],[row+1,col-1]], 'w': [[row-1,col+1],[row-1,col-1]]}
                    potential_list = potential[letters[0]]
                
                for move in potential_list:
                    if self.valid_move(row, col, move[0], move[1]):
                        moves.append([self.current_state[row][col],[letters[0]+str(move[0])+str(move[1])]])
                # if count is at its limit, break out of the inner loop
                if count == self.live_pieces_comp:
                    break
            # do the same for the outer loop
            if count == self.live_pieces_comp:
                break
        if jumps:
            return jumps
        return moves
    
    # do I actually need the old row and col?
    def valid_move(self, old_row, old_col, row, col):
        if row <= 7 and row >= 0 and col <= 7 and col >= 0:
            if self.current_state[row][col] == '   ':
                return True
        return False
    
    # to decide how this one will work  
    #def winner(self):
    
    def king(self, move):
        # move is a list, first entry is the from index and second is to index
        # alternatively use letters
        if self.maximizing and move[1][1] == '0':
            return True
        elif not self.maximizing and move[1][1] == '7':
            return True
        return False
        
    def necessary_jump(self, row, col):
        # check whether there is a possibility to jump 
        # if there is, return only this move as a possibility
            # add posible moves to the list
        jumps = []
        # the 2 other conditions in case it is a king
        # valid_move check before the other conditions to see if such move is actually feasible
        # if a jump is not a valid move then we don't need to check the validity of a move to adjacent square
        if self.maximizing or self.current_state[row][col] == "W" or self.current_state[row][col] == "B":
            if self.valid_move(row,col, row-2, col+2):
                if 'b' in self.current_state[row-1][col+1] and self.current_state[row-2][col+2] == "   ":
                    jumps.append([self.current_state[row][col], self.current_state[row-2][col+2]])       
            if self.valid_move(row,col, row-2, col-2):
                if 'b' in self.current_state[row-1][col-1] and self.current_state[row-2][col-2] == "   ":
                    jumps.append([self.current_state[row][col], self.current_state[row-2][col+2]])
        elif not self.maximizing or self.current_state[row][col] == "W" or self.current_state[row][col] == "B":
            if self.valid_move(row,col, row+2, col+2):
                if 'w' in self.current_state[row+1][col+1] and self.current_state[row+2][col+2] == "   ":
                    jumps.append([self.current_state[row][col], self.current_state[row+2][col+2]])       
            if self.valid_move(row,col, row+2, col-2):
                if 'w' in self.current_state[row+1][col-1] and self.current_state[row+2][col-2] == "   ":
                    jumps.append([self.current_state[row][col], self.current_state[row+2][col-2]])
        if jumps:
            return True, jumps
        return False, None
        
    
    def play(self, move):
        # move will be a dictionary or, if easier, a list
        # erase the piece at certain index
        # put it at another index
        # check if a move makes the piece a king using seft.king()
        if self.king(move):
            old_row, old_col = move[0][1], move[0][2]
            row, col, letter = move[1][1], move[1][2], move[1][0]
            self.current_state[row][col] = upper(letter) + str(row) + str(col)
            self.current_state[old_row][old_col] = '   '
        else:
            old_row, old_col = move[0][1], move[0][2]
            row, col, letter = move[1][1], move[1][2], move[1][0]
            self.current_state[old_row][old_col] = '   '
            self.current_state[row][col] = letter + str(row) + str(col)
            self.current_state[old_row][old_col] = '   '
        return self
#
    def __str__(self):
        current_state = deepcopy(self.current_state)
        for i in range(8):
            current_state[i].insert(0, ' {pl} '.format(pl=i))
        headers = [ ' ']+[ str(n) for n in range(8)]
        return tabulate.tabulate(current_state, headers = headers, tablefmt='grid')


# In[186]:


m = Checkers(True)
print(m)
print(m.valid_moves())


# In[172]:


m = range(8, -1, -1)
for n in m:
    print(n)


# In[122]:


# evaluation functions
# inside the function decide which evaluation method to use
def evaluate():
    return True


# In[106]:


# minimax algorithm
terminal_states = []

# change the game and board stuff because the game class has been removed
def minimax(board, depth, alpha = float('inf'), beta = float('-inf')):
    """ minimax algorithm"""
    
    # if winner return 
    if game.winner():
        # here add stuff that should be returned
        return 
    
    moves = board.get_valid_moves()
    if board_state in terminal_states or not moves or depth == depth_limit:
        return evaluate()
    
    if game.maximizing:
        best_value = float('-inf')
        for move in moves:
            # check whether this works
            # if not, check this oout:
            # https://stackoverflow.com/questions/48338847/how-to-copy-a-class-instance-in-python
            new_board = copy.deepcopy(board).play(move)
            value = minimax(new_board, depth+1,alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_val
    else:
        best_value = float('inf')
        for move in moves:
            new_board = copy.deepcopy(board).play(move)
            value = minimax(new_board, depth+1,alpha, beta)
            best_value = min(best_value, value)
            beta = max(beta, best_value)
            if beta <= alpha:
                break
        return best_val


# In[ ]:


# play the game here and print out what is needed and ask for user's input
def main():
    # use play function


# In[ ]:


# potentially fancy UI


# In[ ]:




