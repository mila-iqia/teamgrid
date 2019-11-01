from teamgrid.minigrid import *
from teamgrid.register import register

class SwitchEnv(MiniGridEnv):
    """
    Environment with a light switch to turn lights on/off
    """

    def __init__(
        self,
        num_agents=2,
        num_goals=1,
        reward_switch=False,
        reward_all=False,
    ):
        self.num_agents = num_agents
        self.num_goals = num_goals
        self.reward_switch = reward_switch
        self.reward_all = reward_all

        super().__init__(
            width=21,
            height=11,
            max_steps=100
        )

        # Only allow turn left/right/forward/toggle actions
        self.action_space = spaces.Discrete(self.actions.toggle+1)

    def _gen_grid(self, width, height):
        # Create the grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Middle wall with a gap
        self.grid.vert_wall(width // 2, 0, height//2)
        self.grid.vert_wall(width // 2, height//2 + 1)

        # Light switch in the left room
        self.grid.set(
            0, height//2,
            Switch(
                'yellow',
                is_on=False,
                env=self,
                left=width//2 + 1,
                top=0,
                width=width//2,
                height=height,
            )
        )

        # Place the goal objects randomly, on the right side
        self.goals = []
        for i in range(self.num_goals):
            obj = Ball('green')
            self.place_obj(obj, top=(width//2, 0), size=(width//2, height))
            self.goals.append(obj)

        # Randomize the player start positions and orientations
        for i in range(self.num_agents):
            self.place_agent()

        # Switch previously toggled
        self.toggled = False

    def step(self, actions):
        rewards = [0] * len(self.agents)

        # For each agent
        for agent_idx, agent in enumerate(self.agents):
            # Get the contents of the cell in front of the agent
            fwd_pos = agent.front_pos
            fwd_cell = self.grid.get(*fwd_pos)

            # If the agent has reached a ball
            if actions[agent_idx] == self.actions.forward:
                if fwd_cell and fwd_cell.type == 'ball':
                    self.goals.remove(fwd_cell)
                    self.grid.set(*fwd_pos, None)

                    if self.reward_all:
                        rewards = [1] * len(self.agents)
                    else:
                        rewards[agent_idx] = 1

            # If the agent has toggled a switch for the first time
            if self.reward_switch and not self.toggled:
                if actions[agent_idx] == self.actions.toggle:
                    if fwd_cell and fwd_cell.type == 'switch':
                        rewards[agent_idx] = 1
                        self.toggled = True

        obss, _, done, info = MiniGridEnv.step(self, actions)

        # When all goals are reached, the episode ends
        if len(self.goals) == 0:
            done = True

        return obss, rewards, done, info

class SwitchRSwitch(SwitchEnv):
    def __init__(self):
        super().__init__(reward_switch=True)

class SwitchRAll(SwitchEnv):
    def __init__(self):
        super().__init__(reward_all=True)

register(
    id='TEAMGrid-Switch-v0',
    entry_point='teamgrid.envs:SwitchEnv'
)

register(
    id='TEAMGrid-SwitchRSwitch-v0',
    entry_point='teamgrid.envs:SwitchRSwitch'
)

register(
    id='TEAMGrid-SwitchRAll-v0',
    entry_point='teamgrid.envs:SwitchRAll'
)
