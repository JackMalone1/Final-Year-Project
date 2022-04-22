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
model.learn(total_timesteps=80000)
model.save("ppo_go")

