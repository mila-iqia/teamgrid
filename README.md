# TEAMGrid

Multiagent gridworld environment for the TEAM project: Temporal abstraction in cooperative multi-agent systems.

Requirements:
- Python 3.5+
- OpenAI Gym
- NumPy
- PyQT 5 for graphics

This environment has been built as part of work done at the [Mila](https://mila.quebec/en/).

## Installation

Clone this repository and install the dependencies with `pip3`:

```
git clone https://github.com/maximecb/teamgrid.git
cd teamgrid
pip3 install -e .
```

## Basic Usage

There is a UI application which allows you to manually control the agent with the arrow keys:

```
./manual_control.py
```

The environment being run can be selected with the `--env-name` option, eg:

```
./manual_control.py --env-name TEAMGrid-FourRooms-v0
```

## Included Environments

The environments listed below are implemented in the [teamgrid/envs](/teamgrid/envs) directory.
Each environment provides one or more configurations registered with OpenAI gym. Each environment
is also programmatically tunable in terms of size/complexity, which is useful for curriculum learning
or to fine-tune difficulty.

### Four rooms

Registered ids:
- `TEAMGrid-FourRooms-v0`

Four room environment. N agents and M goals are randomly placed in any of the rooms. The agents get +1 reward for stepping over a goal object. All M objects must be collected for the episode to terminate.

### Switch

Registered ids:
- `TEAMGrid-Switch-v0`
- `TEAMGrid-SwitchNoneAll-v0`
- `TEAMGrid-SwitchOneOne-v0`
- `TEAMGrid-SwitchOneAll-v0`
- `TEAMGrid-SwitchAllAll-v0`

Two agents are placed in a two room environment. There is a goal object in the room on the right. The room on the right is dark until the switch in the room on the left is turned on. To maximize efficiency, one agent should go in the room on the right while the other turns on the switch in the room on the left. In the `TEAMGrid-Switch-v0` variant, only the agent who reaches the goal object gets a +1 reward. In the other variants, either none, one, or all the agents get a reward for toggling the switch and reaching the goal. For instance, in `TEAMGrid-SwitchOneAll-v0`, one agent gets rewarded for toggling the switch, but all the agents get rewarded when anyone reaches the goal.

## Design

MiniGrid is built to support tasks involving natural language and sparse rewards.
The observations are dictionaries, with an 'image' field, partially observable
view of the environment, a 'mission' field which is a textual string
describing the objective the agent should reach to get a reward, and a 'direction'
field which can be used as an optional compass. Using dictionaries makes it
easy for you to add additional information to observations
if you need to, without having to force everything into a single tensor.

Structure of the world:
- The world is an NxM grid of tiles
- Each tile in the grid world contains zero or one object
  - Cells that do not contain an object have the value `None`
- Each object has an associated discrete color (string)
- Each object has an associated type (string)
  - Provided object types are: wall, floor, lava, door, key, ball, box and goal
- The agent can pick up and carry exactly one object (eg: ball or key)
- To open a locked door, the agent has to be carrying a key matching the door's color

Actions in the basic environment:
- Turn left
- Turn right
- Move forward
- Pick up an object
- Drop the object being carried
- Toggle (open doors, interact with objects)
- Done (task completed, optional)

By default, sparse rewards are given for reaching a green goal tile. A
reward of 1 is given for success, and zero for failure. There is also an
environment-specific time step limit for completing the task.
You can define your own reward function by creating a class derived
from `MiniGridEnv`. Extending the environment with new object types or action
should be very easy. If you wish to do this, you should take a look at the
[teamgrid/minigrid.py](teamgrid/minigrid.py) source file.
