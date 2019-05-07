#!/usr/bin/env python3

import gym
import teamgrid
from teamgrid.wrappers import RGBImgObsWrapper

env = gym.make('TEAMGrid-FourRooms-v0')
env = RGBImgObsWrapper(env)

#env.render()

for i in range(20):
    actions = [0, 0, 0, 0]
    obss, rewards, done, info = env.step(actions)

    if done:
        break
