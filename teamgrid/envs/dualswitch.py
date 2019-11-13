from teamgrid.minigrid import *
from teamgrid.register import register

class DualSwitchEnv(MiniGridEnv):
    """
    Environment with two switches that need to be engaged by two agents
    """

    def __init__(
        self,
    ):
        super().__init__(
            width=17,
            height=9,
            max_steps=100
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

        # Light switch in the left room
        self.grid.set(
            0, height//2,
            Switch(
                'yellow',
                is_on=False,
                env=self,
                left=0,
                top=0,
                width=0,
                height=0,
            )
        )

        # Light switch in the right room
        self.grid.set(
            width - 1, height//2,
            Switch(
                'yellow',
                is_on=False,
                env=self,
                left=0,
                top=0,
                width=0,
                height=0,
            )
        )

        # Place the goal objects randomly, on the right side
        self.goals = [Ball('green'), Ball('green')]

        # Place one agent in each room
        self.place_agent(top=(0, 0), size=(width//2, height))
        self.place_agent(top=(width//2, 0), size=(width//2, height))

        # Switches toggled indicator
        self.toggled = [False] * 2

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
                    self.goals[agent_idx] = None
                    self.grid.set(*fwd_pos, None)
                    rewards[agent_idx] = 1

            # If the agent has toggled a switch for the first time
            if actions[agent_idx] == self.actions.toggle:
                if fwd_cell and fwd_cell.type == 'switch' and not self.toggled[agent_idx]:
                    print('PLACING GOAL', agent_idx)

                    # Make the goal appear for the other agent
                    goal = self.goals[(agent_idx+1)%2]
                    if agent_idx == 0:
                        self.place_obj(obj=goal, top=(self.width//2, 0), size=(self.width//2, self.height))
                    else:
                        self.place_obj(obj=goal, top=(0, 0), size=(self.width//2, self.height))

                    self.toggled[agent_idx] = True
                    rewards[agent_idx] = 1

        obss, _, done, info = MiniGridEnv.step(self, actions)

        # When all goals are reached, the episode ends
        if not self.goals[0] and not self.goals[1]:
            done = True

        return obss, rewards, done, info

register(
    id='TEAMGrid-DualSwitch-v0',
    entry_point='teamgrid.envs:DualSwitchEnv'
)
