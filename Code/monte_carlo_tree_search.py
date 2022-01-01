from copy import copy
from datetime import datetime
from random import choice

from go_rules import GoRules
from node import Node


class MonteCarloTreeSearch:
    def __init__(self, board, **kwargs):
        seconds = kwargs.get('time', 30)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.board = board
        self.states = []
        self.max_moves = kwargs.get('max_moves', 100)

    def get_best_move_in_time(self, board, allowed_time):
        start_time = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - start_time < allowed_time:
            pass

    def update(self, state):
        self.states.append(state)

    def get_play(self):
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()

    def expansion(self, node: Node):
        n = copy(node)
        rules = GoRules()
        available_moves = rules.get_legal_spots_to_play(n.board)

    def run_simulation(self):
        states_copy = self.states[:]
        state = states_copy[-1]

        for t in range(self.max_moves):
            rules = GoRules(state, len(state))
            legal = rules.get_legal_spots_to_play(state)
            play = choice(legal)
            state = rules.next_state(state, play)
            states_copy.append(state)

            winner = rules.winner(state)
            if winner:
                break