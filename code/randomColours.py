from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from operator import add
import random

class RandomColoursEnv(MiniGridEnv):
    """
    Environment with a door and key, sparse reward, colourful
    """

    def __init__(self, size=8, action_dependent = True):
        super().__init__(
            grid_size=size,
            max_steps=10*size*size
        )
        self.action_dependent = action_dependent

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.width = width
        self.height = height
        self.n_obstacles = (width -2) * (height -2) // 2
        
        self.colourOptions = [    
                'red',
                'blue',  
                'purple',
                'yellow',
                'grey'  
            ]  
        
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place a goal in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)

        # Create a vertical splitting wall
        splitIdx = self._rand_int(2, width-2)
        self.grid.vert_wall(splitIdx, 0)

        # Place the agent at a random position and orientation
        # on the left side of the splitting wall
        self.place_agent(size=(splitIdx, height))

        # Place a door in the wall
        doorIdx = self._rand_int(1, width-2)
        self.put_obj(Door('yellow', is_locked=True), splitIdx, doorIdx)

        # Place a yellow key on the left side
        self.place_obj(
            obj=Key('yellow'),
            top=(0, 0),
            size=(splitIdx, height)
        )
        # Place obstacles
        self.obstacles = []
        for i_obst in range(self.n_obstacles):
            c = random.choice(self.colourOptions)
            self.obstacles.append(CustomLava(color = c))
            self.place_obj(self.obstacles[i_obst], max_tries=400)

        self.mission = "use the key to open the door and then get to the goal"
        
    def step(self, action):
        if self.action_dependent:
            if action == 5:
                newObstacles = []
                for i_obst in range(len(self.obstacles)):
                    old_pos = self.obstacles[i_obst].cur_pos
                    self.grid.set(*old_pos, None)
                    c = random.choice(self.colourOptions)
                    newObstacles.append(CustomLava(color = c))
                    self.place_obj(self.obstacles[i_obst], max_tries=400)
        else:
            randomNumber = random.randint(0,9)
            randomWhen = [3,5,6]
            if randomNumber in randomWhen:
                newObstacles = []
                for i_obst in range(len(self.obstacles)):
                    old_pos = self.obstacles[i_obst].cur_pos
                    self.grid.set(*old_pos, None)
                    c = random.choice(self.colourOptions)
                    newObstacles.append(CustomLava(color = c))
                    self.place_obj(self.obstacles[i_obst], max_tries=400)
                
            
        # Update the agent's position/direction
        obs, reward, done, info = MiniGridEnv.step(self, action)
        return obs, reward, done, info

class CustomLava(WorldObj):
    def __init__(self, color):
        super().__init__('floor', 'red')
        self.color = color
        self.COLORS = {
            'red'   : np.array([255, 0, 0]),
            'green' : np.array([0, 255, 0]),
            'blue'  : np.array([0, 0, 255]),
            'purple': np.array([112, 39, 195]),
            'yellow': np.array([255, 255, 0]),
            'grey'  : np.array([100, 100, 100])
            }
    def can_overlap(self):
        return True

    def render(self, img):
        # c = (255, 128, 0)

        # Background color
        fill_coords(img, point_in_rect(0, 1, 0, 1), self.COLORS[self.color])

        # Little waves
        for i in range(3):
            ylo = 0.3 + 0.2 * i
            yhi = 0.4 + 0.2 * i
            fill_coords(img, point_in_line(0.1, ylo, 0.3, yhi, r=0.03), (0,0,0))
            fill_coords(img, point_in_line(0.3, yhi, 0.5, ylo, r=0.03), (0,0,0))
            fill_coords(img, point_in_line(0.5, ylo, 0.7, yhi, r=0.03), (0,0,0))
            fill_coords(img, point_in_line(0.7, yhi, 0.9, ylo, r=0.03), (0,0,0))
            
            
class RandomColoursEnv5x5(RandomColoursEnv):
    def __init__(self):
        super().__init__(size=5)

class RandomColoursEnv6x6(RandomColoursEnv):
    def __init__(self):
        super().__init__(size=6)

class RandomColoursEnv16x16(RandomColoursEnv):
    def __init__(self):
        super().__init__(size=16)

register(
    id='MiniGrid-RandomColours-5x5-v0',
    entry_point='gym_minigrid.envs:RandomColoursEnv5x5'
)

register(
    id='MiniGrid-RandomColours-6x6-v0',
    entry_point='gym_minigrid.envs:RandomColoursEnv6x6'
)

register(
    id='MiniGrid-RandomColours-8x8-v0',
    entry_point='gym_minigrid.envs:RandomColoursEnv'
)

register(
    id='MiniGrid-RandomColours-16x16-v0',
    entry_point='gym_minigrid.envs:RandomColoursEnv16x16'
)
