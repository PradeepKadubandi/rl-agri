import numpy as np
from enum import IntEnum


class StateValue(IntEnum):
    Empty = 0
    Bean = 1
    Corn = 2


# This class is a combination of individual grid cell in the farm and
# the current state of entire farm itself.
# The simulator reward implementation is also in this class though
# it can be easily separated to a different simulator class if there is a future need.
class farmcell:

    def __init__(self, farm_size, index, farm):
        self.n = farm_size
        self.index = index
        self.farm = farm

    def getPossibleActions(self):
        return [StateValue.Bean, StateValue.Corn]

    def isTerminal(self):
        return self.index == (self.n, 0)

    def takeAction(self, action):
        self.farm[self.index] = action
        nextIndex = (self.index[0], self.index[1] + 1) if self.index[1] < self.n - 1 else (self.index[0] + 1, 0)
        return farmcell(self.n, nextIndex, np.array(self.farm))

    def getReward(self):
        return sum([self._get_reward_for_cell((a, b)) for a in range(self.n) for b in range(self.n)])

    def __eq__(self, other):
        return self.index == other.index and np.array_equal(self.farm, other.farm)  # Should we check for type of other?

    # Should perhaps be methods on simulator from here
    def _get_adjacent(self, index):
        result = []
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if (a, b) != (0, 0):
                    nb = (index[0] + a, index[1] + b)
                    if 0 <= nb[0] < self.n and 0 <= nb[1] < self.n:
                        result.append(nb)

        return result

    def _get_reward_for_cell(self, index):
        neighbors = self._get_adjacent(index)

        if self.farm[index] == StateValue.Empty:
            return 0

        reward = 10
        if self.farm[index] == StateValue.Bean:
            for neighbor in neighbors:
                if self.farm[neighbor] == StateValue.Corn:
                    return 15

        if self.farm[index] == StateValue.Corn:
            for neighbor in neighbors:
                if self.farm[neighbor] == StateValue.Bean:
                    reward += 1

        return reward

