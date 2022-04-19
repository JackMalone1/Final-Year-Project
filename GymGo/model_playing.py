import gym
import random
import argparse
import tensorflow as tf
from tensorflow.keras import layers
from collections import deque
import matplotlib.pyplot as plt

import numpy as np
parser = argparse.ArgumentParser(description='Demo Go Environment')
parser.add_argument('--boardsize', type=int, default=19)
parser.add_argument('--komi', type=float, default=0)
args = parser.parse_args()

# Initialize environment
go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi, reward_method="heuristic")
state = go_env.reset()
# Game loop
done = False
goal_steps = 500
initial_games = 100000
generated_model = False
board_positions = []

def initialise_board_positions(board_size):
    """
    Sets up an array with tuples that represent the move for a given index
    """
    for row in range(board_size):
        for col in range(board_size):
            board_positions.append((row, col))
            
    for position in board_positions:
        print(position)

def act(state, model):
    """
    gets the model to predict the move and then return what it thinks will be the most likely move
    """
    act_values = model.predict(state)
    print(act_values)
    return np.argmax(act_values[0])
    
def index_to_board_position(index):
    """
    looks up what move should be done based on the index that the model predicted
    """
    return board_positions[index]
        
if __name__ == '__main__':
    """
    Loads in a model and then gets it to play against itself until the game is finished
    """
    board_size = 19
    initialise_board_positions(board_size)
    episodes = 20
    total_score = 0
    model = tf.keras.models.load_model("go_model.h5")
    while not done:
        index = act(np.reshape(state, (board_size,board_size,6)), model)
        action = index_to_board_position(index) 
        input("Enter to continue")
        print(action)

        state, reward, done, info = go_env.step(action)
        #state = np.reshape(state, (19,19,6))
        go_env.render('terminal')
        if go_env.game_ended():
            done = True
        index = act(np.reshape(state, (board_size,board_size,6)), model)
        action = index_to_board_position(index)
        input("Enter to continue")
        print(action)

        state, reward, done, info = go_env.step(action)
        go_env.render('terminal')
        #state = np.reshape(state, (19,19,6))