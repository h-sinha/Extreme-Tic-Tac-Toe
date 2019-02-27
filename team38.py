
class Bot:
    def __init__(self, flag):
        self.flag = flag #1 = Max player (X), 2 = Min player (O)
        self.available_moves = [self.find_available_moves(i) for i in xrange(19683)]
        self.position_weight = [4, 3, 4, 3, 6, 3, 4, 3, 4]
        self.P = [self.find_P(i) for i in xrange(19683)]
        self.is_abandon = [self.find_if_abandon(i) for i in xrange(19683)]
        self.board = [[int(0)] * 9] * 2
        return
    def find_available_moves(self, state):
        j = int(1)
        possibilities = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            if value == 0:
                possibilities.append(int(self.flag*j))
            j *= 3
        return possibilities
    def find_pattern(self, state):
        j = int(1)
        small_board = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            if value == 0:
            	small_board.append(0)
            elif value == 1:
            	small_board.append(1)
            else: 
            	small_board.append(2)
            j *= 3
        patterns = []
        for i in xrange(3):
        	patterns.append([i*3, i*3 +1, i*3 + 2])
        	patterns.append([i, i + 3, i + 6])
        patterns.append([0, 4, 8])
        patterns.append([2, 4, 6])
        a = [0, 0, 0, 0]
        for pattern in patterns:
        	self.find_pattern_helper(small_board, pattern, a)
        return tuple(a)
    def find_pattern_helper(self, small_board, pattern, a):
    	player1 = 0
    	player2 = 0
    	for position in pattern:
    		if small_board[position] == self.flag:
    			player1 += 1
    		elif small_board[position] != 0:
    			player2 += 1
    	for x in xrange(2):
    		if player1 == 3 - x and player2 == 0:
    			a[x] += 1
    		if player2 == 3 - x and player1 == 0:
    			a[x + 2] += 1
    	return
    def find_P(self, state):
        A_0, A_1, B_0, B_1 = self.find_pattern(state)
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 3)
            if value == self.flag:
                sum_of_position_weights += self.position_weight[i]
        return (50 * A_0) + (10 * A_1) + (25 * B_0) + (5 * B_1) + sum_of_position_weights
    def find_if_abandon(self, state):
        parse_board = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            parse_board.append(value)
        patterns = [];
        for i in xrange(3):
            patterns.append([i*3, i*3 +1, i*3 + 2]);
            patterns.append([i, i + 3, i + 6]);
        patterns.append([0, 4, 8]);
        patterns.append([2, 4, 6]);
        a = [0, 0, 0, 0]
        for pattern in patterns:
            if parse_board[pattern[0]] == parse_board[pattern[1]] and parse_board[pattern[1]] == parse_board[pattern[2]] and parse_board[pattern[0]] != 0:
                return 1
        for mark in parse_board:
            if mark == 0:
                return 0;
        return 1
    # def move(self, board, old_move, flag):

    def move(self, board, old_move, flag):
        # We need to update our internal board from the board passed
        for big_board in xrange(2):
            for small_board in xrange(9):
                state = int(0)
                for position in xrange(8, -1, -1):
                    state *= 3
                    if board.big_boards_status[big_board][small_board][position] == 'x':
                        state += 1
                    elif board.big_boards_status[big_board][small_board][position] == 'o':
                        state += 2
                self.board[big_board][small_board] = state
        return self.ai_move(old_move[2])
test = Bot(2)
print test.find_pattern(14762)
# print test.available_moves[9112]