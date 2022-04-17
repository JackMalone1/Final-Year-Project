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
go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi)
state = go_env.reset()
# Game loop
done = False
goal_steps = 500
initial_games = 100000
generated_model = False
board_positions = []

def initialise_board_positions(board_size):
    for row in range(board_size):
        for col in range(board_size):
            board_positions.append((row, col))
            
    for position in board_positions:
        print(position)

def act(state, model):
    act_values = model.predict(state)
    return np.argmax(act_values[0])
    
def index_to_board_position(index):
    return (1,1)
        
if __name__ == '__main__':
    board_size = 19
    initialise_board_positions(board_size)
    episodes = 20
    total_score = 0
    model = tf.keras.models.load_model("go_model.h5")
    while not done:
        index = act(np.reshape(state, (board_size,board_size,6)), model)
        action = index_to_board_position(index) 
        print(action)

        state, reward, done, info = go_env.step(action)
        #state = np.reshape(state, (19,19,6))
        go_env.render('terminal')
        if go_env.game_ended():
            done = True
        index = act(np.reshape(state, (board_size,board_size,6)), model)
        action = index_to_board_position(index)
        print(action)

        state, reward, done, info = go_env.step(action)
        go_env.render('terminal')
        #state = np.reshape(state, (19,19,6))