#!/usr/bin/env python
# -*- coding: utf-8 -*-

from teamgrid.minigrid import *
from teamgrid.register import register

class FourRoomsEnv(MiniGridEnv):
    """
    Classical 4 rooms gridworld environment.
    """

    def __init__(self, num_agents=4, num_objs=4):
        self.num_agents = num_agents
        self.num_objs = num_objs
        super().__init__(
            grid_size=19,
            max_steps=100
        )

        # Only allow turn left/turn right/forward movement actions
        self.action_space = spaces.Discrete(self.actions.forward+1)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.horz_wall(0, 0)
        self.grid.horz_wall(0, height - 1)
        self.grid.vert_wall(0, 0)
        self.grid.vert_wall(width - 1, 0)

        room_w = width // 2
        room_h = height // 2

        # For each row of rooms
        for j in range(0, 2):

            # For each column
            for i in range(0, 2):
                xL = i * room_w
                yT = j * room_h
                xR = xL + room_w
                yB = yT + room_h

                # Bottom wall and door
                if i + 1 < 2:
                    self.grid.vert_wall(xR, yT, room_h)
                    pos = (xR, self._rand_int(yT + 1, yB))
                    self.grid.set(*pos, None)

                # Bottom wall and door
                if j + 1 < 2:
                    self.grid.horz_wall(xL, yB, room_w)
                    pos = (self._rand_int(xL + 1, xR), yB)
                    self.grid.set(*pos, None)

        # Randomize the player start position and orientation
        for i in range(self.num_agents):
            self.place_agent()

        for i in range(self.num_objs):
            self.place_obj(Ball(self._rand_color()))

    def step(self, action):
        obs, reward, done, info = MiniGridEnv.step(self, action)






        return obs, reward, done, info


register(
    id='TEAMGrid-FourRooms-v0',
    entry_point='teamgrid.envs:FourRoomsEnv'
)
