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
    def 
    # def move(self, board, old_move, flag):
test = Bot(1)
print test.available_moves[9112]