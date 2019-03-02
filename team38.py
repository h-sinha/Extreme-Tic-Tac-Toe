import random
from copy import deepcopy

class Bot:
    def __init__(self):
        #Flag => 1 = Max player (X), 2 = Min player (O)
        self.available_moves = [[self.find_available_moves(i, j + 1) for i in xrange(19683)] for j in xrange(2)]
        self.position_weight = [4, 3, 4, 3, 6, 3, 4, 3, 4]
        self.is_abandon = [self.find_if_abandon(i) for i in xrange(19683)]
        self.distance = [(int(-1), int(-1)) for i in xrange(19683)]
        for i in xrange(19683):
            self.find_distance(i)
        self.board = [[int(0) for i in xrange(9)] for j in xrange(2)]
        self.big_state = [int(0), int(0)]
        self.bonus = False
        self.who = -1
        self.flag = -1
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
    def find_distance(self, state):
        # Returns pair  of shortest distance to victory for player 1, player 2
        if self.distance[state] != (-1, -1):
            return self.distance[state]
        distance_player1 = 100000
        distance_player2 = 100000
        status = self.is_abandon[state]
        if status == 1:
            distance_player1 = 0
            #distance_player2 = 100000 Infinity as the second player can never get this board back
        elif status == 2:
            #distance_player1 = 100000 Infinity as the first player can never get this board back
            distance_player2 = 0
        elif status == 0:
            for move in self.available_moves[0][state]:
                dist,_ = self.find_distance(state + move)
                distance_player1 = min(distance_player1, dist+1)
            for move in self.available_moves[1][state]:
                _, dist = self.find_distance(state + move)
                distance_player2 = min(distance_player2, dist+1)
        self.distance[state] = (distance_player1, distance_player2)
        return self.distance[state]
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
      # Abandoned => Won, Draw
    def find_if_abandon_big(self, state):
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
        return 0
    # Update board state based on move
    def make_move(self, board, direction, move):
        #Not tested, tread with caution!
        bonus_transition = False
        self.board[board][direction] += move
        state = self.board[board][direction]
        if self.is_abandon[state] != 0:
            m = self.is_abandon[state]
            if not self.bonus and m == self.flag:
                self.bonus = True
            for i in xrange(9):
                if i == direction:
                    self.big_state[board] += m
                    break
                m *= 4
        else:
            self.flag = 3 - self.flag
            if self.bonus == True:
                self.bonus = False
                bonus_transition = True
        # print "Make move:", board, direction, move, "Bonus:", self.bonus, "Transition:", "True" if bonus_transition else "False", "New flag:", self.flag
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                direction = i
                break
        return direction, bonus_transition
    def undo_move(self, board, direction, move, bonus_transition):
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
        if not self.bonus:
            self.flag = 3 - self.flag
        if bonus_transition:
            self.bonus = True
        else:
            self.bonus = False
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
            print old_move
            big_board, small_board, move = self.ai_move((3 * (old_move[1]%3)) + (old_move[2]%3), 1 if flag == 'x' else 2)
        small_position = -1
        for i in xrange(9):
            move, value = divmod(move, 3)
            if value != 0:
                small_position = i
                break
        big_row, big_col = divmod(small_board, 3)
        small_row, small_col = divmod(small_position, 3)
        return (big_board, (big_row * 3) + small_row, (big_col * 3) + small_col)
    def get_heuristic(self, cells):
        ans = 100000
        for cell in cells:
            ans = min(ans, self.distance[cell[2]][self.flag-1])
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
    def minimax(self, alpha, beta, depth, direction):
        # TODO: Check if the game ends (Terminal state)
        cells = self.find_valid_cells(direction)
        if depth <= 0:
            return self.get_heuristic(cells), (-1, -1, -1)
        # We are the max player
        min_value = 100000
        best_move = (-1, -1, -1)
        for cell in cells:
            for move in self.available_moves[self.flag - 1][cell[2]]:
                # Cell = (board, direction, state)
                tmp_bonus = self.bonus
                new_direction, bonus_transition = self.make_move(cell[0], cell[1], move)
                value, _ = self.minimax(alpha, beta, depth - 1, new_direction)
                self.undo_move(cell[0], cell[1], move, bonus_transition)
                self.bonus = tmp_bonus
                # print value
                if value < min_value:
                    min_value = value
                    best_move = (cell[0], cell[1], move)
        return min_value, best_move
    def ai_move(self, direction, flag):
        self.who = flag
        self.flag = flag
        _, best_move = self.minimax(-1000000, 1000000, 4, direction)
        return best_move
# test=Bot()
# print test.find_distance(15436)