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
go_env.reset()
# Game loop
done = False
goal_steps = 500
initial_games = 100000
generated_model = False

def act(state, model):

    act_values = model.predict(state)
    return np.argmax(act_values[0])
        
if __name__ == '__main__':

    episodes = 20
    total_score = 0
    model = tf.keras.models.load_model("go_model.h5")
    while not done:
        action = go_env.render(mode="human")
        state, reward, done, info = go_env.step(action)
        state = np.reshape(state, (19,19,6))

        if go_env.game_ended():
            break
        action = act(state, model)
        print(action)
        if action not in go_env.valid_moves():
            action = go_env.uniform_random_action()
        state, reward, done, info = go_env.step(action)
        #state = np.reshape(state, (19,19,6))