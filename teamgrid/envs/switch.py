from teamgrid.minigrid import *
from teamgrid.register import register

class SwitchEnv(MiniGridEnv):
    """
    Environment with a light switch to turn lights on/off
    """

    def __init__(self, num_agents=2, num_goals=1):
        self.num_agents = num_agents
        self.num_goals = num_goals

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

    def step(self, actions):
        rewards = [0] * len(self.agents)

        # For each agent
        for agent_idx, agent in enumerate(self.agents):
            if actions[agent_idx] == self.actions.forward:
                # Get the contents of the cell in front of the agent
                fwd_pos = agent.front_pos
                fwd_cell = self.grid.get(*fwd_pos)

                # If the agent has reached a ball
                if fwd_cell and fwd_cell.type == 'ball':
                    self.goals.remove(fwd_cell)
                    self.grid.set(*fwd_pos, None)
                    rewards[agent_idx] = 1

        obss, _, done, info = MiniGridEnv.step(self, actions)

        # When all goals are reached, the episode ends
        if len(self.goals) == 0:
            done = True

        return obss, rewards, done, info

register(
    id='TEAMGrid-Switch-v0',
    entry_point='teamgrid.envs:SwitchEnv'
)
