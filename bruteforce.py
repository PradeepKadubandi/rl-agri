# This is just a brute force implementation to find out the optimal farm plan
# Should take too long with relatively short n as the runtime complexity is 2 ^ (n^2)
# P.S. Indeed - it's not practical to run this for n >= 5.

from simulator import farmcell
import numpy as np
import itertools

class bruteforce:
    def __init__(self, farm_size):
        self.n = farm_size

    def solve(self):
        best_reward = 0
        best_state = None
        i = 0
        for s in itertools.product([1, 2], repeat=self.n ** 2):
            i += 1
            farm = np.array(s).reshape((self.n, self.n))
            state = farmcell((self.n, 0), farm)
            reward = state.getReward()
            if best_reward < reward:
                best_reward = reward
                best_state = farm

        return best_reward, best_state, i
