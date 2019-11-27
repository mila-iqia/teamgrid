from teamgrid.minigrid import *
from teamgrid.register import register

class DoorBallEnv(MiniGridEnv):
    """
    """

    def __init__(
        self,
    ):
        super().__init__(
            width=13,
            height=7,
            max_steps=160
        )

        # Only allow turn left/right/forward/toggle actions
        self.action_space = spaces.Discrete(self.actions.toggle+1)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Middle wall
        self.grid.vert_wall(width // 2, 0, height)

        # Switch in the right room
        self.grid.set(
            width - 1, height//2,
            Switch(
                'blue',
                is_on=False,
                env=self,
                left=0,
                top=0,
                width=0,
                height=0,
            )
        )

        # Door in the left room
        self.blue_door = Door('blue', is_locked=True)
        self.grid.set(width//2, height//2, None)
        self.place_obj(self.blue_door, top=(width//2, height//2), size=(1,1))

        # Ball in the right room
        self.red_ball = Ball('red')
        self.place_obj(self.red_ball, top=(width//2, 0), size=(width//2, height))

        # Place one agent in each room
        self.place_agent(top=(0, 0), size=(width//2, height), color='red')
        self.place_agent(top=(width//2, 0), size=(width//2, height), color='blue')

        self.toggled = False

    def step(self, actions):
        obss, _, done, info = MiniGridEnv.step(self, actions)

        rewards = [0] * len(self.agents)

        # For each agent
        for agent_idx, agent in enumerate(self.agents):
            # Get the contents of the cell in front of the agent
            fwd_pos = agent.front_pos
            fwd_cell = self.grid.get(*fwd_pos)

            # If the agent has reached a ball
            if actions[agent_idx] == self.actions.forward:
                if fwd_cell and fwd_cell.type == 'ball' and self.agents[agent_idx].color == 'red':
                    rewards[agent_idx] = 1
                    done = True

            # If the agent has toggled a switch for the first time
            if actions[agent_idx] == self.actions.toggle:
                if fwd_cell and fwd_cell.type == 'switch' and not self.toggled:
                    # Toggle the corresponding door
                    self.grid.set(*self.blue_door.init_pos, None)
                    self.toggled = True
                    rewards[agent_idx] = 1

        return obss, rewards, done, info

register(
    id='TEAMGrid-DoorBall-v0',
    entry_point='teamgrid.envs:DoorBallEnv'
)
