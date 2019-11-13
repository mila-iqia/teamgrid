import numpy as np
import gym
from gym import error, spaces, utils
from .minigrid import OBJECT_TO_IDX, COLOR_TO_IDX
from .minigrid import CELL_PIXELS

class RGBImgObsWrapper(gym.core.ObservationWrapper):
    """
    Wrapper to use partially observable RGB image as the observation input.
    This can be used to have the agent to solve the gridworld in pixel space.
    """

    def __init__(self, env):
        self.__dict__.update(vars(env))  # Pass values to super wrapper
        super().__init__(env)

        self.tile_size = CELL_PIXELS // 2

        view_sz = self.env.agent_view_size
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(view_sz*self.tile_size, view_sz*self.tile_size, 3),
            dtype='uint8'
        )

    def observation(self, obss):
        env = self.unwrapped
        return [
            env.get_obs_render(
                o,
                env.agents[i].color,
                tile_pixels=self.tile_size,
                mode='rgb_array'
            )
            for i, o in enumerate(obss)
        ]
