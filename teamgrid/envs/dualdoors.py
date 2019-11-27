from teamgrid.minigrid import *
from teamgrid.register import register

class DualDoorsEnv(MiniGridEnv):
    """
    Each agent must toggle a switch that opens a door to let the other
    agent through. The agents complete the episode when they meet and face
    one another.
    """

    def __init__(
        self,
    ):
        super().__init__(
            width=19,
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

        # Leftmost wall
        self.grid.vert_wall(width // 3, 0, height)

        # Rightmost wall
        self.grid.vert_wall((2 * width) // 3, 0, height)

        # Switch in the left room
        self.grid.set(
            0, height//2,
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

        # Switch in the right room
        self.grid.set(
            width - 1, height//2,
            Switch(
                'red',
                is_on=False,
                env=self,
                left=0,
                top=0,
                width=0,
                height=0,
            )
        )

        # Door in the left room
        self.red_door = Door('red', is_locked=True)
        self.grid.set(width//3, height//2, None)
        self.place_obj(self.red_door, top=(width//3, height//2), size=(1,1))

        # Door in the right room
        self.blue_door = Door('blue', is_locked=True)
        self.grid.set((2*width)//3, height//2, None)
        self.place_obj(self.blue_door, top=((2*width)//3, height//2), size=(1,1))

        # Place one agent in each room
        self.place_agent(top=(0, 0), size=(width//3, height), color='red')
        self.place_agent(top=((2*width)//3, 0), size=(width//3, height), color='blue')

        self.toggled = [False] * 2

    def step(self, actions):
        obss, _, done, info = MiniGridEnv.step(self, actions)

        rewards = [0] * len(self.agents)

        # For each agent
        for agent_idx, agent in enumerate(self.agents):
            # Get the contents of the cell in front of the agent
            fwd_pos = agent.front_pos
            fwd_cell = self.grid.get(*fwd_pos)

            # If the agent has toggled a switch for the first time
            if actions[agent_idx] == self.actions.toggle:
                if fwd_cell and fwd_cell.type == 'switch' and not self.toggled[agent_idx]:
                    # Toggle the corresponding door
                    if fwd_cell.color == 'red':
                        self.grid.set(*self.red_door.init_pos, None)
                    else:
                        self.grid.set(*self.blue_door.init_pos, None)

                    self.toggled[agent_idx] = True
                    rewards[agent_idx] = 1

        # If the agents are facing one another
        if np.array_equal(self.agents[0].front_pos, self.agents[1].cur_pos):
            if np.array_equal(self.agents[1].front_pos, self.agents[0].cur_pos):
                done = True
                rewards = [1, 1]

        return obss, rewards, done, info

register(
    id='TEAMGrid-DualDoors-v0',
    entry_point='teamgrid.envs:DualDoorsEnv'
)
