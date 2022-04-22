import argparse
import random
from statistics import mean, median

import gym

# Arguments
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from collections import deque
import matplotlib.pyplot as plt
np.random.seed(0)

parser = argparse.ArgumentParser(description='Demo Go Environment')
parser.add_argument('--boardsize', type=int, default=19)
parser.add_argument('--komi', type=float, default=0)
args = parser.parse_args()

# Initialize environment
go_env = gym.make('gym_go:go-v0', size=args.boardsize, komi=args.komi, reward_method="heuristic")
go_env.reset()
# Game loop
done = False
goal_steps = 500
initial_games = 100000
generated_model = False


class DQN:
    """ Implementation of deep q learning algorithm """

    def __init__(self, action_space, state_space):

        self.action_space = action_space
        self.state_space = state_space
        self.epsilon = 1.0
        self.gamma = .99
        self.batch_size = 64
        self.epsilon_min = .01
        self.epsilon_decay = .996
        self.memory = deque(maxlen=1000000)
        self.model = self.build_model()
        print(self.model.summary())

    def build_model(self):
        """
        Creates all of the layers for the model, the model is created with 4 layers of 64,19,19,6 which is then flattened and compiled
        Returns the final generated model
        """
        model = tf.keras.Sequential()
        model.add(layers.Dense(6, input_dim=self.state_space, activation='relu'))
        model.add(layers.Dense(19, input_dim=self.state_space, activation='relu'))
        model.add(layers.Dense(19, input_dim=self.state_space, activation='relu'))
        model.add(layers.Dense(64, input_dim=self.state_space, activation='relu'))
        model.add(tf.keras.layers.Flatten())
        model.compile(loss='mse', optimizer='Adam')
        model.summary()
        return model

    def remember(self, state, action, reward, next_state, done):
        """
        adds the played move to the memory of the ai so that it is able to train on this data
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """
        Gets the model to predict what move should be played based on the state that was passed in
        """
        if np.random.rand() <= self.epsilon:
            return go_env.uniform_random_action()
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):

        if len(self.memory) < self.batch_size:
            return
        print("Minibatch")
        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])
        print("squeeze")
        states = np.squeeze(states)
        next_states = np.squeeze(next_states)
        print("Predict")
        targets_full = self.model.predict_on_batch(states)
        targets = rewards + self.gamma * (np.amax(self.model.predict_on_batch(next_states), axis=1)) * (
                     1 - dones)  # Update the q-value
        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets
        print("Fit")
        self.model.fit(states, targets_full, epochs=1, verbose=0)  # Train the network on the new q-values.
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(episode):
    loss = []
    agent = DQN(go_env.action_space.n, go_env.observation_space.shape[0])
    for e in range(episode):
        state = go_env.reset()
        state = np.reshape(state, (19,19,6))
        score = 0
        max_steps = 500

        for i in range(max_steps):
            action = agent.act(state)
            current_amount_of_retries = 0
            max_times_to_retry = 500
            picked_invalid_move = False
            if action not in go_env.valid_moves():
                picked_invalid_move = True
                action = go_env.uniform_random_action()
            next_state, reward, done, _ = go_env.step(action)
           
            score += reward
            next_state = np.reshape(next_state, (19,19,6))
            temp_state = np.reshape(state, (19,19,6))
            agent.remember(temp_state, action, reward, next_state, done)
            state = next_state
            agent.replay()
            if done:
                print("episode: {}/{}, score: {}".format(e, episode, score))
                break
            print("Step: {} Iteration: {}".format(i, e))
        loss.append(score)

        # Average score of last 100 episode
        is_solved = np.mean(loss[-100:])
        if is_solved > 200000:
            print('\n Task Completed! \n')
            # save model and architecture to single file
            generated_model = True
            agent.model.save("go_model.h5")
            break
        
        print("Average over last 100 episode: {0:.2f} \n".format(is_solved))
        print("Iteration: {}".format(e))
    print("Saving Model")
    agent.model.save("go_model.h5")
    return loss


if __name__ == '__main__':
    print(go_env.observation_space)
    print(go_env.action_space)
    episodes = 600
    loss = train_dqn(episodes)
    plt.plot([i + 1 for i in range(0, len(loss), 2)], loss[::2])
    plt.show()