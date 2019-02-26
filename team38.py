import numpy as np

class Bot:
    def __init__(self, flag):
        self.flag = flag #1 = Max player (X), 2 = Min player (O)
        self.available_moves = [self.find_available_moves(i) for i in xrange(19683)]
        pass
    def find_available_moves(self, state):
        j = int(1)
        possibilities = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            if value == 0:
                possibilities.append(int(self.flag*j))
            j *= 3
        return possibilities
    def find_small_pattern(self, state):
        j = int(1)
        small_board = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            if value == 0:
            	small_board.append(0);
            elif value == 1:
            	small_board.append(1);
            else: 
            	small_board.append(2);
            j *= 3
        patterns = [];
        for i in xrange(3):
        	patterns.append([i*3, i*3 +1, i*3 + 2]);
        	patterns.append([i, i + 3, i + 6]);
        patterns.append([0, 4, 8]);
        patterns.append([2, 4, 6]);
        a = [0, 0];
        b = [0, 0];
        for pattern in patterns:
        	self.find_small_pattern_helper(small_board, pattern, a, b);
        return a,b;
    def find_small_pattern_helper(self, small_board, pattern, a, b):
    	player1 = 0
    	player2 = 0
    	for position in pattern:
    		if small_board[position] == self.flag:
    			player1 += 1
    		elif small_board[position] != 0:
    			player2 += 1;
  		# print(player2, player1)
    	for x in xrange(2):
    		if player1 == 3 - x and player2 == 0:
    			a[x] += 1
    		if player2 == 3 - x and player1 == 0:
    			b[x] += 1
    	return
    # def move(self, board, old_move, flag):
test = Bot(1)
print test.find_small_pattern(9760)
# print test.available_moves[9112]