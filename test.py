
for position in xrange(8, -1, -1):
    state *= 3
    if board[position] == 'x':
        state += 1
    elif board[position] == 'o':
        state += 2