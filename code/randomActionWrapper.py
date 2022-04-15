import random 
import gym

class RandomActionWrapper(gym.ActionWrapper):
    
    def __init__(self, env, ra_dependent = False):
        super().__init__(env)
        self.ra_dependent = ra_dependent
    
    def action(self, action):
        if not self.ra_dependent:
            actions = [0,1,2,3,4,5]
            randomNumber = random.randint(0,9)
            randomWhen = 3
            if randomNumber == randomWhen:
                action = random.choice(actions)
            return action
        else:
            if action == 5:
                actions = [0,1,2,3,4,5]
                action = random.choice(actions)
            return action
                


