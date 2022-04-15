import gym
import seaborn as sns
import numpy as np
import os
import datetime
import pickle



class stateCoverage(gym.core.Wrapper):

    def __init__(self, env, envSize=8, recordWhen=100000, nr_envs = 8, rank = 0, intr = 1, extr = 1):
        super().__init__(env)
        self.envSize = envSize
        self.rank = rank
        self.counts = {}
        self.numberTimesteps = 0
        try:
            self.recordWhen = recordWhen / nr_envs
        except:
            print(recordWhen)
            print(nr_envs)
                        
        self.file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
        if intr and extr:
            if not os.path.exists('./coverageData/both'):
                os.makedirs('./coverageData/both')
                self.filePath =  './coverageData/both' + self.file_name + ".pickle"
        if intr and not extr:
            if not os.path.exists('./coverageData/intrinsic'):
                os.makedirs('./coverageData/intrinsic')
                self.filePath =  './coverageData/intrinsic' + self.file_name + ".pickle"

        if extr and not intr:
            if not os.path.exists('./coverageData/extrinsic'):
                os.makedirs('./coverageData/extrinsic')
                self.filePath =  './coverageData/extrinsic' + self.file_name + ".pickle"

    
        
    def step(self, action):
        obs, reward, done, info = self.env.step(action)
        
        self.numberTimesteps += 1
        env = self.unwrapped
        tup = (tuple(env.agent_pos))

        # Get the count for this key
        pre_count = 0
        if tup in self.counts:
            pre_count = self.counts[tup]

        # Update the count for this key
        new_count = pre_count + 1
        self.counts[tup] = new_count

        if self.numberTimesteps % self.recordWhen == 0:
            grid = np.zeros((self.envSize, self.envSize))
            for key, value in self.counts.items():
                x = key[0]
                y = key[1]
                grid[y][x] = value
            grid_cropped = grid[1:-1,1:-1]
            data = [self.numberTimesteps, grid_cropped]
            with open(self.filePath,'ab+') as container:
                pickle.dump(data, container, protocol=pickle.HIGHEST_PROTOCOL)

        return obs, reward, done, info

    def reset(self, **kwargs):
        return self.env.reset(**kwargs)