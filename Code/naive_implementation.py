import itertools
from collections import namedtuple

N = 19
NN = 19 * 19
WHITE, BLACK, EMPTY = "O", "X", "."


def swap_colors(color):
    if color == BLACK:
        return WHITE
    elif color == WHITE:
        return BLACK
    else:
        return color


EMPTY_BOARD = EMPTY * NN


def flatten(c):
    return N * c[0] + c[1]


def unflatten(fc):
    return divmod(fc, N)


def is_on_board(c):
    return c[0] % N == c[0] and c[1] % N == c[1]


def get_valid_neighbours(fc):
    x, y = unflatten(fc)
    possible_neighbours = (
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    )
    return [flatten(n) for n in possible_neighbours if is_on_board(n)]


NEIGHBOURS = [get_valid_neighbours(fc) for fc in range(NN)]
assert sorted(NEIGHBOURS[0]) == [1, N]
assert sorted(NEIGHBOURS[1]) == [0, 2, N + 1]
assert sorted(NEIGHBOURS[N + 1]) == [1, N, N + 2, 2 * N + 1]


def find_reached(board, fc):
    colour = board[fc]
    chain = set([fc])
    reached = set()
    frontier = [fc]
    while frontier:
        current_fc = frontier.pop()
        chain.add(current_fc)
        for fn in NEIGHBOURS[current_fc]:
            if board[fn] == colour and not fn in chain:
                frontier.append(fn)
            elif board[fn] != colour:
                reached.add(fn)
    return chain, reached


class IllegalMove(Exception):
    pass


def place_stone(colour, board, fc):
    return board[:fc] + colour + board[fc + 1 :]


def bulk_place_stones(colour, board, stones):
    byteboard = bytearray(board, encoding="ascii")
    colour = ord(colour)
    for fstone in stones:
        byteboard[fstone] = colour
    return byteboard.decode("ascii")


def maybe_capture_stones(board, fc):
    chain, reached = find_reached(board, fc)
    if not any(board[fr] == EMPTY for fr in reached):
        board = bulk_place_stones(EMPTY, board, chain)
        return board, chain
    else:
        return board, []


def play_move_incomplete(board, fc, colour):
    if board[fc] != EMPTY:
        raise IllegalMove
    board = place_stone(colour, board, fc)

    opp_colour = swap_colors(colour)
    opp_stones = []
    my_stones = []

    for fn in NEIGHBOURS[fc]:
        if board[fn] == colour:
            my_stones.append(fn)
        elif board[fn] == opp_colour:
            opp_stones.append(fn)

    for fs in opp_stones:
        board, _ = maybe_capture_stones(board, fs)

    for fs in my_stones:
        board, _ = maybe_capture_stones(board, fs)

    return board


def is_koish(board, fc):
    if board[fc] != EMPTY:
        return None
    neighbour_colours = {board[fn] for fn in NEIGHBOURS[fc]}
    if len(neighbour_colours) == 1 and not EMPTY in neighbour_colours:
        return list(neighbour_colours)[0]
    else:
        return None


class Position(namedtuple("Position", ["board", "ko"])):
    @staticmethod
    def initial_state():
        return Position(board=EMPTY_BOARD, ko=None)

    def get_board(self):
        return self.board

    def __str__(self):
        import textwrap

        return "\n".join(textwrap.wrap(self.board, N))

    def play_move(self, fc, color):
        board, ko = self
        if fc == ko:
            raise IllegalMove("%s\n Move at %s illegally retakes ko." % (self, fc))

        if board[fc] != EMPTY:
            raise IllegalMove("%s\n Stone exists at %s." % (self, fc))

        possible_ko_color = is_koish(board, fc)
        new_board = place_stone(color, board, fc)

        opp_color = swap_colors(color)
        opp_stones = []
        my_stones = []
        for fn in NEIGHBOURS[fc]:
            if new_board[fn] == color:
                my_stones.append(fn)
            elif new_board[fn] == opp_color:
                opp_stones.append(fn)

        opp_captured = 0
        for fs in opp_stones:
            new_board, captured = maybe_capture_stones(new_board, fs)
            opp_captured += len(captured)

        # Check for suicide
        new_board, captured = maybe_capture_stones(new_board, fc)
        if captured:
            raise IllegalMove("\n%s\n Move at %s is suicide." % (self, fc))

        if opp_captured == 1 and possible_ko_color == opp_color:
            new_ko = list(opp_captured)[0]
        else:
            new_ko = None

        return Position(new_board, new_ko)

    def score(self):
        board = self.board
        while EMPTY in board:
            fempty = board.index(EMPTY)
            empties, borders = find_reached(board, fempty)
            possible_border_color = board[list(borders)[0]]
            if all(board[fb] == possible_border_color for fb in borders):
                board = bulk_place_stones(possible_border_color, board, empties)
            else:
                # if an empty intersection reaches both white and black,
                # then it belongs to neither player.
                board = bulk_place_stones("?", board, empties)
        return board.count(BLACK) - board.count(WHITE)

    def get_liberties(self):
        board = self.board
        liberties = bytearray(NN)
        for color in (WHITE, BLACK):
            while color in board:
                fc = board.index(color)
                stones, borders = find_reached(board, fc)
                num_libs = len([fb for fb in borders if board[fb] == EMPTY])
                for fs in stones:
                    liberties[fs] = num_libs
                board = bulk_place_stones("?", board, stones)
        return list(liberties)
