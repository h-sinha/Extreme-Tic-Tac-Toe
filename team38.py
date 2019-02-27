import random
class Bot:
    def __init__(self):
        #Flag => 1 = Max player (X), 2 = Min player (O)
        self.available_moves = [[self.find_available_moves(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.position_weight = [4, 3, 4, 3, 6, 3, 4, 3, 4]
        self.P = [[self.find_P(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.is_abandon = [self.find_if_abandon(i) for i in xrange(19683)]
        self.board = [[int(0) for i in xrange(9)] for j in xrange(2)]
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
    def find_P(self, state, flag):
        A_0, A_1, B_0, B_1 = self.find_pattern(state, flag)
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 3)
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
        # if not self.is_abandon[self.board[0][direction]] and not self.is_abandon[self.board[1][direction]]:
        #     big_board = random.randrange(2)
        #     move = self.available_moves[flag-1][self.board[big_board][direction]][random.randrange(len(self.available_moves[flag-1][self.board[big_board][direction]]))]
        #     print self.available_moves[flag - 1][self.board[big_board][direction]]
        #     print self.board[big_board][direction]
        #     return (big_board, direction, move)
        # elif not self.is_abandon[self.board[1][direction]]:
        #     move = self.available_moves[flag-1][self.board[1][direction]][random.randrange(len(self.available_moves[flag-1][self.board[1][direction]]))]
        #     return (1, direction, move)
        # elif not self.is_abandon[self.board[0][direction]]:
        #     move = self.available_moves[flag-1][self.board[0][direction]][random.randrange(len(self.available_moves[flag-1][self.board[0][direction]]))]
        #     return (0, direction, move)
        # else:
        #     return self.ai_move(random.randrange(9), flag)
        ret = self.alpha_beta(direction, 5, -2000, 2000, flag)[0:3]
        print ret
        return ret
    def alpha_beta(self, direction, depth, alpha, beta, flag):
        # if depth == 0:
        #     ret = 2000
        #     board_idx = 0 
        #     for i in xrange(2):
        #         if not self.is_abandon[self.board[i][direction]]:
        #             for move in self.available_moves[flag - 1][self.board[i][direction]]:
        #                 if self.P[flag - 1][self.board[i][direction] + move] < ret:
        #                     ret = self.P[flag - 1][self.board[i][direction] + move]
        #                     cur_move = move
        #                     board_idx = i
        #     # print(board_idx, direction,cur_move, ret)
        #     return (board_idx, direction , cur_move, ret)
        # board_idx = 0
        # cur_move = -1
        # new_direction = 0
        # if flag == 1:
        #     value = -2000
        #     for i in xrange(2):
        #         if alpha >= beta:
        #                 break
        #         for move in self.available_moves[flag - 1][self.board[i][direction]]:
        #             temp_move = move
        #             for idx in xrange(9):
        #                 move, value = divmod(move, 3)
        #                 if value != 0:
        #                     new_direction = idx
        #                     break
        #             ret = self.alpha_beta(new_direction, depth - 1, alpha, beta, 3 - flag)     
        #             if alpha < ret[3]:
        #                 board_idx = i
        #                 direction = new_direction
        #                 cur_move = temp_move
        #             alpha = max(ret[3], alpha)
        #             if alpha >= beta:
        #                 break
        # elif flag == 2:
        #     value = 2000
        #     new_direction = 0
        #     for i in xrange(2):
        #         if alpha >= beta:
        #                 break
        #         for move in self.available_moves[flag - 1][self.board[i][direction]]:
        #             temp_move = move
        #             for idx in xrange(9):
        #                 move, value = divmod(move, 3)
        #                 if value != 0:
        #                     new_direction = idx
        #                     break
        #             ret = self.alpha_beta(new_direction, depth - 1, alpha, beta, 3 - flag)     
        #             if beta > ret[3]:
        #                 board_idx = i
        #                 direction = new_direction
        #                 cur_move = temp_move
        #             beta = min(ret[3], beta)
        #             if alpha >= beta:
        #                 break
        # return (board_idx, direction , cur_move, ret)

        # (self.is_abandon(self.board[0][direction] and self.is_abandon(self.board[1][direction]))):
# test = Bot();
# print test.alpha_beta(0, 5, -1000, 1000, 1)