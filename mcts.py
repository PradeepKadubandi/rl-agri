# Copied from https://github.com/pbsinclair42/MCTS/blob/master/mcts.py
# and some modifications (mostly adding stuff needed for my problem setup) are done.
import time
import math
import random


def randomPolicy(state):
    while not state.isTerminal():
        try:
            action = random.choice(state.getPossibleActions())
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()


# Added by me
def firstActionPolicy(state):
    while not state.isTerminal():
        try:
            action = state.getPossibleActions()[0]
        except IndexError:
            raise Exception("Non-terminal state has no possible actions: " + str(state))
        state = state.takeAction(action)
    return state.getReward()


class treeNode():
    def __init__(self, state, parent):
        self.state = state
        self.isTerminal = state.isTerminal()
        self.isFullyExpanded = self.isTerminal
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.children = {}


class mcts():
    def __init__(self, timeLimit=None, iterationLimit=None, explorationConstant=1 / math.sqrt(2),
                 rolloutPolicy=randomPolicy, initialState=None):
        if timeLimit != None:
            if iterationLimit != None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            # time taken for each MCTS search in milliseconds
            self.timeLimit = timeLimit
            self.limitType = 'time'
        else:
            if iterationLimit == None:
                raise ValueError("Must have either a time limit or an iteration limit")
            # number of iterations of the search
            if iterationLimit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.searchLimit = iterationLimit
            self.limitType = 'iterations'
        self.explorationConstant = explorationConstant
        self.rollout = rolloutPolicy

        # Changes by me
        self.root = None
        if initialState is not None:
            self.root = treeNode(initialState, None)

    # Modifications : If you want to persist tree between searches,
    # pass the intialState at construction time and do not pass a value for initialState in search.
    def search(self, initialState=None):
        if initialState is not None:
            self.root = treeNode(initialState, None)

        if self.root is None:
            raise ValueError('The initial state parameter must be used either with the constructor or search method')

        if self.limitType == 'time':
            # i = 0
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
                # i += 1
            # print (str.format("Number of iterations run before time : {}", i))
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        return self.getAction(self.root, bestChild)

    # Method that I added, can be used once the training is done.
    # The method selects a sample trajectory optimally as long as the
    # tree policy is built and then after that will select randomly to
    # generate a sample.
    def optimal_rollout(self):
        curr = self.root
        full_tree = True
        while not curr.isTerminal:
            if len(curr.children) == 0:
                action = random.choice(curr.state.getPossibleActions())
                curr = treeNode(curr.state.takeAction(action), curr)
                full_tree = False
            else:
                curr = self.getBestChild(curr, 0)
        return curr, full_tree

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.rollout(node.state)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = treeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            node.totalReward += reward
            node = node.parent

    def getBestChild(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def getAction(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action
