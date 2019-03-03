import random
from copy import deepcopy
import time

class Bot:
    def __init__(self):
        #Flag => 1 = Max player (X), 2 = Min player (O)
        self.available_moves = [[self.find_available_moves(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.position_weight_small = [3, 4, 3, 3, 6, 3, 4, 3, 4]
        self.position_weight_big = [4, 3, 4, 3, 6, 3, 4, 3, 4]
        self.P = [[self.find_P(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.P_big = [[self.find_P_big(i, j+1) for i in xrange(262144)] for j in xrange(2)]
        self.is_abandon = [self.find_if_abandon(i) for i in xrange(19683)]
        self.big_abandon = [self.find_big_abandon(i) for i in xrange(262144)]
        self.board = [[int(0) for i in xrange(9)] for j in xrange(2)]
        self.big_state = [int(0), int(0)]
        self.who = -1
        self.flag = -1
        self.patterns = []
        self.start_time = 0
        self.patterns.append([0, 1, 2, 4])
        self.patterns.append([3, 4, 5, 5])
        self.patterns.append([6, 7, 8, 4])
        self.patterns.append([0, 3, 6, 4])
        self.patterns.append([1, 4, 7, 5])
        self.patterns.append([2, 5, 8, 4])
        self.patterns.append([0, 4, 8, 6])
        self.patterns.append([2, 4, 6, 6])
        return
    # Finds all possible moves and return in the for of 3^cell_number
    def find_available_moves(self, state, flag):
        j = int(1)
        possibilities = []
        for _ in xrange(9):
            state, value = divmod(state, 3)
            if value == 0:
                possibilities.append(int(flag*j))
            j *= 3
        return possibilities
    # Returns (a_0, a_1, b_0, b_1) for small board
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
    # Returns (a_0, a_1, b_0, b_1) for big board
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
    # Returns P for small board
    def find_P(self, state, flag):
        #Not tested, tread with caution!
        A_0, A_1, B_0, B_1 = self.find_pattern(state, flag)
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 3)
            if value == flag:
                sum_of_position_weights += self.position_weight_small[i]
            if value == 3 - flag:
                sum_of_position_weights -= self.position_weight_small[i]
        return (90 * A_0) + (20 * A_1) - (135 * B_0) - (30 * B_1) + sum_of_position_weights
    # Returns P for big board
    def find_P_big(self, state, flag):
        #Not tested, tread with caution!
        A_0, A_1, B_0, B_1 = self.find_big_pattern(state, flag)
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 4)
            if value == flag:
                sum_of_position_weights += self.position_weight_big[i]
            if value == 3 - flag:
                sum_of_position_weights -= self.position_weight_big[i]
        return (90 * A_0) + (20 * A_1) - (135 * B_0) - (30 * B_1) + sum_of_position_weights
    # Returns true if board is abandoned else False
    # Abandoned => Won, Draw
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
            if parse_board[pattern[0]] == parse_board[pattern[1]] and parse_board[pattern[1]] == parse_board[pattern[2]] and parse_board[pattern[0]] == 1:
                return 1
            elif parse_board[pattern[0]] == parse_board[pattern[1]] and parse_board[pattern[1]] == parse_board[pattern[2]] and parse_board[pattern[0]] == 2:
                return 2
        for mark in parse_board:
            if mark == 0:
                return 0
        return 3
    def find_big_abandon(self, state):
        parse_board = []
        for _ in xrange(9):
            state, value = divmod(state, 4)
            parse_board.append(value)
        patterns = []
        for i in xrange(3):
            patterns.append([i*3, i*3 +1, i*3 + 2])
            patterns.append([i, i + 3, i + 6])
        patterns.append([0, 4, 8])
        patterns.append([2, 4, 6])
        a = [0, 0, 0, 0]
        for pattern in patterns:
            if parse_board[pattern[0]] == parse_board[pattern[1]] and parse_board[pattern[1]] == parse_board[pattern[2]] and parse_board[pattern[0]] == 1:
                return 1
            elif parse_board[pattern[0]] == parse_board[pattern[1]] and parse_board[pattern[1]] == parse_board[pattern[2]] and parse_board[pattern[0]] == 2:
                return 2
        for mark in parse_board:
            if mark == 0:
                return 0
        return 3
    # Update board state based on move
    def make_move(self, board, direction, move):
        #Not tested, tread with caution!
        self.board[board][direction] += move
        state = self.board[board][direction]
        if self.is_abandon[state] != 0:
            m = self.is_abandon[state]
            for i in xrange(9):
                if i == direction:
                    self.big_state[board] += m
                    break
                m *= 4
        # print "Make move:", board, direction, move, "Bonus:", self.bonus, "Transition:", "True" if bonus_transition else "False", "New flag:", self.flag
        direction = -1
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                direction = i
                break
        return direction
    def undo_move(self, board, direction, move):
        #Not tested, tread with caution!
        state = self.board[board][direction]
        if self.is_abandon[self.board[board][direction]] != 0:
            m = self.is_abandon[state]
            for i in xrange(9):
                if i == direction:
                    self.big_state[board] -= m
                    break
                m *= 4
        self.board[board][direction] -= move
        # print "Undo move:", board, direction, move, "Bonus:", self.bonus, "Transition:", "True" if bonus_transition else "False", "New flag:", self.flag
        return
    # Updates board state and returns next move to simulator
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
        # Updates big_board state
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
            print old_move, "OUR MOVE", "Bonus: ", True if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == flag else False
            for j in xrange(2):
                print "Board", j+1, ":", self.P_big[self.who - 1][self.big_state[j]]
                for row in xrange(3):
                    for col in xrange(3):
                        print self.P[self.who-1][self.board[j][(3 * row) + col]], "\t",
                    print ""
            big_board, small_board, move = self.ai_move((3 * (old_move[1]%3)) + (old_move[2]%3), 1 if flag == 'x' else 2, True if board.big_boards_status[old_move[0]][old_move[1]][old_move[2]] == flag else False)
        small_position = -1
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                small_position = i
                break
        big_row, big_col = divmod(small_board, 3)
        small_row, small_col = divmod(small_position, 3)
        return (big_board, (big_row * 3) + small_row, (big_col * 3) + small_col)
    def get_heuristic(self):
        ans = -100000
        for pattern in self.patterns:
            ans = max(ans, (3*self.P_big[self.flag-1][self.big_state[0]])+pattern[3]*(self.P[self.who - 1][self.board[0][pattern[0]]] + self.P[self.who - 1][self.board[0][pattern[1]]] + self.P[self.who - 1][self.board[0][pattern[2]]]))
            ans = max(ans, (3*self.P_big[self.flag-1][self.big_state[1]])+pattern[3]*(self.P[self.who - 1][self.board[1][pattern[0]]] + self.P[self.who - 1][self.board[1][pattern[1]]] + self.P[self.who - 1][self.board[1][pattern[2]]]))
        return ans
    def find_valid_cells(self, direction):
        moves = []
        first_board = self.board[0][direction]
        second_board = self.board[1][direction]
        first_board_free = True if self.is_abandon[first_board] == 0 else False
        second_board_free = True if self.is_abandon[second_board] == 0 else False
        if first_board_free:
            moves.append((0, direction, first_board))
        if second_board_free:
            moves.append((1, direction, second_board))
        if not first_board_free and not second_board_free:
            for dir in xrange(9):
                first_board = self.board[0][dir]
                second_board = self.board[1][dir]
                first_board_free = True if self.is_abandon[first_board] == 0 else False
                second_board_free = True if self.is_abandon[second_board] == 0 else False
                if first_board_free:
                    moves.append((0, dir, first_board))
                if second_board_free:
                    moves.append((1, dir, second_board))
        return moves
    def minimax(self, alpha, beta, depth, direction, flag, bonus):
        # TODO: Check if the game ends (Terminal state)
        # if time.time() - self.start_time >= 20:
        #     return 100000, (-1, -1, -1)
        if self.big_abandon[self.big_state[0]] == self.who or self.big_abandon[self.big_state[1]] == self.who:
            return 100000, (-1, -1, -1)
        elif self.big_abandon[self.big_state[0]] == 3 - self.who or self.big_abandon[self.big_state[1]] == 3 - self.who:
            return - 100000, (-1, -1, -1)
        elif self.big_abandon[self.big_state[0]] == 3 and self.big_abandon[self.big_state[1]] == 3:
            return 100, (-1, -1, -1)  #Actually should return points
        cells = self.find_valid_cells(direction)
        if depth <= 0:
            return self.get_heuristic(), (-1, -1, -1)
        if self.flag == self.who:
            # We are the max player
            max_value = -10000000
            best_move = (-1, -1, -1)
            for cell in cells:
                for move in self.available_moves[self.flag - 1][cell[2]]:
                    # Cell = (board, direction, state)
                    new_direction = self.make_move(cell[0], cell[1], move)
                    if self.is_abandon[self.board[cell[0]][cell[1]]] == flag and not bonus:
                        value, _ = self.minimax(alpha, beta, depth - 1, new_direction, flag, True)
                    else:
                        value, _ = self.minimax(alpha, beta, depth - 1, new_direction, 3 - flag, True)
                    self.undo_move(cell[0], cell[1], move)
                    if value > max_value:
                        max_value = value
                        best_move = (cell[0], cell[1], move)
                    if max_value > alpha:
                        alpha = max_value
                    if alpha >= beta:
                        return max_value, best_move
            return max_value, best_move
        else:
            # We are the min player
            min_value = 10000000
            best_move = (-1, -1, -1)
            for cell in cells:
                for move in self.available_moves[self.flag - 1][cell[2]]:
                    new_direction = self.make_move(cell[0], cell[1], move)
                    if self.is_abandon[self.board[cell[0]][cell[1]]] == flag and not bonus:
                        value, _ = self.minimax(alpha, beta, depth - 1, new_direction, flag, True)
                    else:
                        value, _ = self.minimax(alpha, beta, depth - 1, new_direction, 3 - flag, True)
                    self.undo_move(cell[0], cell[1], move)
                    if value < min_value:
                        min_value = value
                        best_move = (cell[0], cell[1], move)
                    if min_value < beta:
                        beta = min_value
                    if alpha >= beta:
                        return min_value, best_move
            return min_value, best_move
    def ai_move(self, direction, flag, bonus):
        max_depth = 4
        self.start_time = time.time()
        while time.time() - self.start_time <= 20:
            self.who = flag
            max_depth += 1
            _, best_move_sofar = self.minimax(-1000000, 1000000, max_depth, direction, flag, bonus)
        if best_move_sofar[0] != -1:
            best_move = best_move_sofar
        return best_move