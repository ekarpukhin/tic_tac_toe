import random
from itertools import product, combinations


class Cell:
    def __init__(self, x=None, y=None):
        self.__value = 0
        self.x = x
        self.y = y

    def __eq__(self, other):
        if type(other) is int:
            return self.__value == other
        if type(other) is Cell:
            return self.__value == other.__value

    def __bool__(self):
        return self.__value == 0

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value in range(3):
            self.__value = value
        else:
            raise ValueError('value should be in (0, 1, 2)')

    def bool(self):
        return not self.__value


class TicTacToe:
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2

    def __init__(self):
        self.pole = tuple(tuple(Cell(i, j) for j in range(3)) for i in range(3))

    def __getitem__(self, item):
        if type(item[0]) == int and type(item[0]) == int:
            return self.pole[item[0]][item[1]]
        if type(item[0]) == int:
            return tuple(x.value for x in self.pole[item[0]])
        return tuple(self.pole[x][item[1]] for x in range(3))

    def __setitem__(self, key, value):
        self.pole[key[0]][key[1]].value = value

    def __bool__(self):
        return self.if_anybody_win() == 0

    def init(self):
        for row in self.pole:
            for el in row:
                el.value = self.FREE_CELL

    def get_field(self):
        s = 'TicTacToe\n'
        for row in self.pole:
            for el in row:
                if el.value == self.FREE_CELL:
                    symb = '.'
                elif el.value == self.COMPUTER_O:
                    symb = 'o'
                else:
                    symb = 'x'
                s += '{}    '.format(symb)
            s += '\n'
        return s

    def human_go(self, i, j):                         # smth wrong with recursion, ret None
        print('Choice cell in format {x y}')
        item = i, j
        if self[item]:
            self[item].value = self.HUMAN_X
            print(item)
            return item

    def computer_go(self):
        while True:
            i, j = random.randint(0, 2), random.randint(0, 2)
            if self[(i, j)]:
                self[(i, j)] = self.COMPUTER_O
                return i, j

    def if_anybody_win(self):
        horizontal = [row for row in self.pole]
        vertical = [tuple(self.pole[i][j] for i in range(3)) for j in range(3)]
        cross = [(self[0, 0], self[1, 1], self[2, 2]), (self[0, 2], self[1, 1], self[2, 0])]
        all_lines = horizontal + vertical + cross
        for line in all_lines:
            if line[0] == line[1] == line[2]:
                return line[0].value
        for line in all_lines:
            if line[0] or line[1] or line[2]:
                return 0
        return -1

    def computer_ii(self, step):
        if step == 1:
            positions = product(range(3), range(3))
            for i, j in positions:
                if self[i, j] == self.HUMAN_X:
                    if i == j == 1:
                        self[(0, 0)] = self.COMPUTER_O
                        return 0, 0
                    self[(1, 1)] = self.COMPUTER_O
                    return 1, 1

        ans_queue = []
        all_lines = [(self[i, :]) for i in range(3)] + \
                    [(self[:, i]) for i in range(3)] + \
                    [tuple(self[i, i] for i in range(3))] + \
                    [tuple(self[i, 2-i] for i in range(3))]
        positions = combinations(range(3), 2)
        for line, pos in product(all_lines, positions):
            line_ids = [0, 1, 2]
            if line[pos[0]] == line[pos[1]] and line[pos[0]].value in (1, 2):
                line_ids.remove(pos[0])
                line_ids.remove(pos[1])
                correct_el = line[line_ids[0]]
                if self[(correct_el.x, correct_el.y)]:
                    if line[pos[0]].value == self.COMPUTER_O:
                        self[(correct_el.x, correct_el.y)].value = self.COMPUTER_O
                        return correct_el.x, correct_el.y
                    ans_queue.append((correct_el.x, correct_el.y))

        if ans_queue:
            i, j = ans_queue.pop()
            self[(i, j)].value = self.COMPUTER_O
            return i, j
        return self.computer_go()

    @property
    def is_human_win(self):
        return self.if_anybody_win() == self.HUMAN_X

    @property
    def is_computer_win(self):
        return self.if_anybody_win() == self.COMPUTER_O

    @property
    def is_draw(self):
        return self.if_anybody_win() == -1


class Game:
    def __init__(self):
        self.step = 0
        self.engine = TicTacToe()

    def start(self):
        engine = self.engine
        self.step = 0
        engine.init()

    def show(self):
        return self.engine.get_field()

    def human_turn(self, i, j):
        self.engine.human_go(i, j)

    def computer_turn(self):
        self.engine.computer_ii(self.step)

    def get_result(self):
        if self.engine.is_human_win:
            return "You Win!"
        if self.engine.is_computer_win:
            return "You Lose :("
        else:
            return "Draft."
