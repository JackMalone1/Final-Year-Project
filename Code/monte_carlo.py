import datetime
from random import choice

from colours import Colour
from go_rules import GoRules


class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        seconds = kwargs.get("time", 30)
        self.calculation_time = datetime.timedelta(
            seconds=seconds
        )
        self.board = board
        self.states = []
        self.max_moves = kwargs.get("max_moves", 100)
        self.wins = {}
        self.plays = {}

    def update(self, state):
        self.states.append(state)

    def get_play(self):
        begin = datetime.datetime.utcnow()
        while (
            datetime.datetime.utcnow() - begin
            < self.calculation_time
        ):
            self.run_simulation()

    def run_simulation(self):
        visited_states = set()
        states_copy = self.states[:]
        state = states_copy[-1]
        player = Colour.BLACK

        expand = True
        for t in range(self.max_moves):
            rules = GoRules()
            available_moves = rules.get_legal_spots_to_play(
                self.board
            )
            play = choice(available_moves)
            state = rules.get_next_board_state(state, play)
            states_copy.append(state)

            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0
            visited_states.add((player, state))
            if player is Colour.BLACK:
                player = Colour.WHITE
            else:
                player = Colour.BLACK
            winner = rules.winner(states_copy)
            if winner:
                break
        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] += 1
