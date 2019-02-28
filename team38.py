import random
class Bot:
    def __init__(self):
        #Flag => 1 = Max player (X), 2 = Min player (O)
        self.available_moves = [[self.find_available_moves(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.position_weight = [4, 3, 4, 3, 6, 3, 4, 3, 4]
        self.P = [[self.find_P(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.P_big = [[self.find_P_big(i, j+1) for i in xrange(262144)] for j in xrange(2)]
        self.is_abandon = [self.find_if_abandon(i) for i in xrange(19683)]
        self.board = [[int(0) for i in xrange(9)] for j in xrange(2)]
        self.big_state = [int(0), int(0)]
        return
    def find_available_moves(self, state, flag):
        j = int(1)
        possibilities = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            if value == 0:
                possibilities.append(int(flag*j))
            j *= 3
        return possibilities
    def find_pattern(self, state, flag):
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
        	self.find_pattern_helper(small_board, pattern, a, flag)
        return tuple(a)
    def find_pattern_helper(self, small_board, pattern, a, flag):
    	player1 = 0
    	player2 = 0
    	for position in pattern:
    		if small_board[position] == flag:
    			player1 += 1
    		elif small_board[position] != 0:
    			player2 += 1
    	for x in xrange(2):
    		if player1 == 3 - x and player2 == 0:
    			a[x] += 1
    		if player2 == 3 - x and player1 == 0:
    			a[x + 2] += 1
    	return
    def find_big_pattern(self, state, flag):
        #Not tested, tread with caution!
        small_board = []
        for _ in xrange(9):
            state, value = divmod(state, 4)
            if value == 0:
                small_board.append(0) #free
            elif value == 1:
                small_board.append(1)
            elif value == 2:
                small_board.append(2)
            else: 
                small_board.append(3)  #draw
        patterns = []
        for i in xrange(3):
            patterns.append([i*3, i*3 +1, i*3 + 2])
            patterns.append([i, i + 3, i + 6])
        patterns.append([0, 4, 8])
        patterns.append([2, 4, 6])
        a = [0, 0, 0, 0]
        for pattern in patterns:
            self.find_big_pattern_helper(small_board, pattern, a, flag)
        return tuple(a)
    def find_big_pattern_helper(self, small_board, pattern, a, flag):
        #Not tested, tread with caution!
        player1 = 0
        player2 = 0
        for position in pattern:
            if small_board[position] == flag:
                player1 += 1
            elif small_board[position] == 3 - flag:
                player2 += 1
            elif small_board[position] == 3:
                return
        for x in xrange(2):
            if player1 == 3 - x and player2 == 0:
                a[x] += 1
            if player2 == 3 - x and player1 == 0:
                a[x + 2] += 1
        return
    def find_P(self, state, flag):
        #Not tested, tread with caution!
        A_0, A_1, B_0, B_1 = self.find_pattern(state, flag)
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 3)
            if value == flag:
                sum_of_position_weights += self.position_weight[i]
        return (50 * A_0) + (10 * A_1) + (25 * B_0) + (5 * B_1) + sum_of_position_weights
    def find_P_big(self, state, flag):
        #Not tested, tread with caution!
        A_0, A_1, B_0, B_1 = self.find_big_pattern(state, flag)
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 4)
            if value == flag:
                sum_of_position_weights += self.position_weight[i]
        return (50 * A_0) + (10 * A_1) + (25 * B_0) + (5 * B_1) + sum_of_position_weights
    def find_if_abandon(self, state):
        parse_board = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            parse_board.append(value)
        patterns = []
        for i in xrange(3):
            patterns.append([i*3, i*3 +1, i*3 + 2])
            patterns.append([i, i + 3, i + 6])
        patterns.append([0, 4, 8])
        patterns.append([2, 4, 6])
        a = [0, 0, 0, 0]
        for pattern in patterns:
            if parse_board[pattern[0]] == parse_board[pattern[1]] and parse_board[pattern[1]] == parse_board[pattern[2]] and parse_board[pattern[0]] != 0:
                return True
        for mark in parse_board:
            if mark == 0:
                return False
        return True
    def make_move(self, board, direction, move):
        self.board[board][direction] += move
        if self.is_abandon[self.board[board][direction]] != 0:
            m = self.is_abandon[state]
            for i in xrange(9):
                if i == direction:
                    self.big_board[board] += m
                    break
                m *= 4
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                direction = i
                break
        return direction
    def undo_move(self, board, direction, move):
        if self.is_abandon[self.board[board][direction]] != 0:
            m = self.is_abandon[state]
            for i in xrange(9):
                if i == direction:
                    self.big_board[board] -= m
                    break
                m *= 4
        self.board[board][direction] -= move
        return
    def move(self, board, old_move, flag):
        # We need to update our internal board from the board passed
        for big_board in xrange(2):
            for small_board in xrange(9):
                state = int(0)
                big_row, big_col = divmod(small_board, 3)
                for position in xrange(8, -1, -1):
                    small_row, small_col = divmod(position, 3)
                    # print big_board, small_board, board.big_boards_status[big_board][(3*big_row)+small_row][(3*big_col)+small_col]
                    state *= 3
                    if board.big_boards_status[big_board][(3*big_row)+small_row][(3*big_col)+small_col] == 'x':
                        state += 1
                    elif board.big_boards_status[big_board][(3*big_row)+small_row][(3*big_col)+small_col] == 'o':
                        state += 2
                self.board[big_board][small_board] = state
        #Not tested, tread with caution!
        for big_board in xrange(2):
            state = int(0)
            for cell in xrange(8, -1, -1):
                state *= 4
                row, col = divmod(cell, 3)
                if board.small_boards_status[big_board][row][col] == 'x':
                    state += 1
                elif board.small_boards_status[big_board][row][col] == 'o':
                    state += 2
                elif board.small_boards_status[big_board][row][col] == 'd':
                    state += 3
            self.big_state[big_board] = state
        #We need specify the next possible smallboard position
        #in terms of 0-9
        if old_move[0] == -1:
            #First move if we get the chance
            return (0,4,4)
        else:
            print old_move
            big_board, small_board, move = self.ai_move((3 * (old_move[1]%3)) + old_move[2]%3, 1 if flag == 'x' else 2)
        small_position = -1
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                small_position = i
                break
        big_row, big_col = divmod(small_board, 3)
        small_row, small_col = divmod(small_position, 3)
        return (big_board, (big_row * 3) + small_row, (big_col * 3) + small_col)
    def ai_move(self, direction, flag):
      
   