from tabnanny import verbose
import gym
import argparse
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

parser = argparse.ArgumentParser(description='Demo Go Environment')
parser.add_argument('--boardsize', type=int, default=19)
parser.add_argument('--komi', type=float, default=0)
args = parser.parse_args()

env = gym.make("gym_go:go-v0", size=args.boardsize, komi=args.komi)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=25000)
model.save("ppo_go")

del model

model = PPO.load("ppo_go")

obs = env.reset()


done = False
while not done:
    action = env.render(mode="human")
    state, reward, done, info = env.step(action)
    if env.game_ended():
        break
    action, _states = model.predict(obs)
    state, reward, done, info = env.step(action)

env.render(mode="human")