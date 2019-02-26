
class Bot:
    def __init__(self, flag):
        self.flag = flag #1 = Max player (X), 2 = Min player (O)
        self.available_moves = [self.find_available_moves(i) for i in xrange(19683)]
        self.position_weight = [4, 3, 4, 3, 6, 3, 4, 3, 4]
        self.P = [self.P(i) for i in xrange(19683)]
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
    def find_P(self, state):
        # A_0, A_1, B_0, B_1 = 
        sum_of_position_weights = int(0)
        for i in xrange(9):
            state, value = divmod(state, 3)
            if value == self.flag:
                sum_of_position_weights += self.position_weight[i]
        return (50 * A_0) + (10 * A_1) + (25 * B_0) + (5 * B_1) + sum_of_position_weights
    # def move(self, board, old_move, flag):
test = Bot(1)
print test.available_moves[9112]