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
        #Not tested, tread with caution!
        bonus_transition = False
        self.board[board][direction] += move
        if self.is_abandon[self.board[board][direction]] != 0:
            m = self.is_abandon[state]
            if not is_bonus and m == self.flag:
                self.bonus = True
            for i in xrange(9):
                if i == direction:
                    self.big_board[board] += m
                    break
                m *= 4
        else:
            self.flag = 3 - self.flag
            if self.bonus = True:
                self.bonus = False
                bonus_transition = True
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                direction = i
                break
        return direction, bonus_transition
    def undo_move(self, board, direction, move, bonus_transition):
        #Not tested, tread with caution!
        if self.is_abandon[self.board[board][direction]] != 0:
            m = self.is_abandon[state]
            for i in xrange(9):
                if i == direction:
                    self.big_board[board] -= m
                    break
                m *= 4
        self.board[board][direction] -= move
        if not self.bonus:
            self.flag = 3 - self.flag
        if bonus_transition:
            self.bonus = True
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
    def minimax(self, alpha, beta, depth, direction):
        if depth == 0:
            return - self.get_heuristic()
        first_board = self.board[0][direction]
        second_board = self.board[1][direction]
        first_board_free = True if self.is_abandon[first_board] else False
        second_board_free = True if self.is_abandon[second_board] else False
        big_board_to_play = -1
        move_to_play = -1
        direction_to_play = direction
        value = -1000000
        if self.flag == 2:
            #We are the min player but acting as max player
            if first_board_free:
                for mov in self.available_moves[first_board]:
                    new_direction, bonus_transition = self.make_move(0, direction, mov)
                    child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                    self.undo_move(0, direction, move, bonus_transition)
                    if child_value > value:
                        value = child_value
                        big_board_to_play = 0
                        move_to_play = mov
                    if value > alpha:
                        alpha = value
                        if alpha >= beta:
                            return value, big_board_to_play, move_to_play, direction_to_play
            if second_board_free:
                for mov in self.available_moves[second_board]:
                    new_direction, bonus_transition = self.make_move(1, direction, mov)
                    child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                    self.undo_move(1, direction, move, bonus_transition)
                    if child_value > value:
                        value = child_value
                        big_board_to_play = 1
                        move_to_play = mov
                    if value > alpha:
                        alpha = value
                        if alpha >= beta:
                            return value, big_board_to_play, move_to_play, direction_to_play
            if big_board_to_play == -1:
                # Open Move
                for new_direction in xrange(9):
                    first_board = self.board[0][direction]
                    second_board = self.board[1][direction]
                    first_board_free = True if self.is_abandon[first_board] else False
                    second_board_free = True if self.is_abandon[second_board] else False
                    if first_board_free:
                        for mov in self.available_moves[first_board]:
                            new_direction, bonus_transition = self.make_move(0, direction, mov)
                            child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                            self.undo_move(0, direction, move, bonus_transition)
                            if child_value > value:
                                value = child_value
                                big_board_to_play = 0
                                move_to_play = mov
                            if value > alpha:
                                alpha = value
                                if alpha >= beta:
                                    return value, big_board_to_play, move_to_play, direction_to_play
                    if second_board_free:
                        for mov in self.available_moves[second_board]:
                            new_direction, bonus_transition = self.make_move(1, direction, mov)
                            child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                            self.undo_move(1, direction, move, bonus_transition)
                            if child_value > value:
                                value = child_value
                                big_board_to_play = 1
                                move_to_play = mov
                            if value > alpha:
                                alpha = value
                                if alpha >= beta:
                                    return value, big_board_to_play, move_to_play, direction_to_play
        elif self.flag == 1:
            #We are the max player but acting as min player
            value = 1000000
            if first_board_free:
                for mov in self.available_moves[first_board]:
                    new_direction, bonus_transition = self.make_move(0, direction, mov)
                    child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                    self.undo_move(0, direction, move, bonus_transition)
                    if child_value < value:
                        value = child_value
                        big_board_to_play = 0
                        move_to_play = mov
                    if value < beta:
                        beta = value
                        if alpha >= beta:
                            return value, big_board_to_play, move_to_play, direction_to_play
            if second_board_free:
                for mov in self.available_moves[second_board]:
                    new_direction, bonus_transition = self.make_move(1, direction, mov)
                    child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                    self.undo_move(1, direction, move, bonus_transition)
                    if child_value < value:
                        value = child_value
                        big_board_to_play = 1
                        move_to_play = mov
                    if value < beta:
                        beta = value
                        if alpha >= beta:
                            return value, big_board_to_play, move_to_play, direction_to_play
            if big_board_to_play == -1:
                # Open Move
                for new_direction in xrange(9):
                    first_board = self.board[0][direction]
                    second_board = self.board[1][direction]
                    first_board_free = True if self.is_abandon[first_board] else False
                    second_board_free = True if self.is_abandon[second_board] else False
                    if first_board_free:
                        for mov in self.available_moves[first_board]:
                            new_direction, bonus_transition = self.make_move(0, direction, mov)
                            child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                            self.undo_move(0, direction, move, bonus_transition)
                            if child_value < value:
                                value = child_value
                                big_board_to_play = 0
                                move_to_play = mov
                            if value < beta:
                                beta = value
                                if alpha >= beta:
                                    return value, big_board_to_play, move_to_play, direction_to_play
                    if second_board_free:
                        for mov in self.available_moves[second_board]:
                            new_direction, bonus_transition = self.make_move(1, direction, mov)
                            child_value, _, _, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                            self.undo_move(1, direction, move, bonus_transition)
                            if child_value < value:
                                value = child_value
                                big_board_to_play = 1
                                move_to_play = mov
                            if value < beta:
                                beta = value
                                if alpha >= beta:
                                    return value, big_board_to_play, move_to_play, direction_to_play
        return value, big_board_to_play, move_to_play
    def ai_move(self, direction, flag):
        self.flag = flag
        _, big_board, move, direction = self.minimax(-1000000, 1000000, 5, direction)
        return big_board, direction, move