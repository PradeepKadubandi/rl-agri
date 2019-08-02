# rl-agri

- [Problem Specification](#problem-specification)
- [Problem Setup](#problem-formulation)
- [State and Action space design](#design)
- [Future work](#todo)
- [References](#references)

## Problem Specification
You are building an simplistic AI agent that is responsible for planning a farm.  The job of the agent is to choose the locations at which to plant two crops, corn and beans.  The natural environment is modeled by a "simulator", which will for our toy exercise have very basic rules, and the agent interacts with the simulator to learn how to best plan the farm.

Simulator: the simulator models a farm that is n x n, where n is a configuration parameter.  In each of the n^2 cells, there can be either a corn plant, a bean plant, or empty soil.  The farm starts at time 0 completely empty.  The simulator simulates time ticking forward one day at a time while an agent (which is described next) can do actions each day such as planting a plant or harvesting a plant.  A corn plant in our simulation takes 90 days to grow from time of planting to time of harvest.  A bean plant in our simulation also takes 90 days.  At the 90 day mark, or thereafter, a plant can be harvested, producing 10 units of food (corn or beans), and the cell that the plant was in becomes empty again.  Since bean plants help corn be more productive, for every bean plant that is in one of the adjacent 8 cells to a corn plant, the corn plant produces one extra unit of food at time of harvest.  That is, if there are 3 bean plants directly adjacent to a corn plant, then the corn plant will produce 13 units of food upon harvest rather than 10.  A bean plant that is not next to a corn plant produces 10 units of food upon harvest, and a bean plant that is adjacent to one or more corn plants produces 15 units of food upon harvest.

Agent: the agent interacts with the simulator as a black box (it does not know the rules for how plants interact) and only is able to do the following: plant corn at (x,y), plant bean at (x,y), or harvest crop at (x,y).  It is told by the simulator if it cannot do an action (for example, if there is already a plant at (x,y) or the plant at that location is not ready for harvest), and if a harvest action is successful it is told how much food was produced.  It can perform zero or more actions on any day.  It must use these responses from the simulator as positive and negative rewards, and learn to pick the best plan it can for where to plant the various plants to maximize the food produced by the farm in 91 days.

Task for you to implement: implement a basic simulator that follows the rules above and a Monte-Carlo Tree Search agent that produces a farm plan that maximizes the food produced by the farm.  You may implement the simulator and agent in Python or C++.

Resource: Reinforcement Learning by Sutton and Barto (2nd edition, available for free online)

## Problem Formulation
The notion of time for the given problem specification is not too relevant or interesting given the available time period for agent is 91 days. Obviously agent can harvest (the only action that yields any reward) only once in this period on the last day and only those cells that it planted on first day. So, leaving any farm cell empty on first day does not also makes sense - becauce the agent will obviously get a better reward by planting either corn or bean in that cell instead.

So I am going to treat the problem slightly differently - the problem is to find a farm plan (that fills all the cells with either corn or bean on the first day) that maximizes the yield on 91st day. Once a complete farm plan (for the first day) is obtained, it can be treated as a terminal state and the reward is the effect of harvesting every cell on 91st day.

Though I changed the problem setup slightly (according to the nature of given farm model and requirement that agent has only 91 days), the agent still interacts with the environment (farm simulator) in a black box fashion, it queries at each step the available actions from environment and 'selects' an action and asks the environment to perform the selected action and environment makes the state transition.

However, note that in this problem formulation, the only actions for agent are plant a corn or bean at any given cell (harvesting is implicit in the terminal state and need not be considered as one of possible actions). Next, we will look at how do we design the state and action space for n x n farm plan.

## Design
The state/action space can be modeled or designed in several ways. Straight forward way would be to model the entire structure of the farm as the state and combinations of possible actions over the entire farm as set of available actions. However in this model, from the start state, there are 2^(n^2) possible actions to each possible state (total also 2^(n^2)) which is also a terminal state. The action space is too huge.

A simple way to reduce the action space would be to consider only one arbitrary cell at a time to plant - in this model, we first need to make a choice of cell (n^2 possibilities) and then choose an action (2 possibilities) giving raise to (2 x n^2) possible actions for a given state.

However a further simplication can be made: from the reward perspective, it does not matter in which order we pick two different cells as long as we plant the same things in both the choices. For example, if we first choose cell (0, 0) and plant corn and then choose (0,1) and plat bean, it's the same resulting farm plan as choosing (0, 1) first and planting bean and then choosing (0, 0)  planting corn. This means for arriving at a farm plan, we can just go in a fixed order of cells and make a choice independenly to plant corn or bean at each cell. 

The final form is the state and action space design I have chosen. The cells are chosen in natural sequence (cells in top row from left to right and then cells in second row and so on till the last row) - however each final farm plan is a different state (as it should be because each one yields a different reward). So the state is a combination of 'current index' and 'farm state' , action space contains only 2 actions - plant corn or bean. From a given state, when one of actions is performed, the cell in 'current index' is modified according to action and the envirnment chooses next state to be 'next index' and 'new farm state' (obtained by updating the action selection in current index). In this model, the branching factor of state transitions is just 2 making the problem computationally efficient.

## Todo
- Try different exploration constants
- Try increasing the timeLimit for agent to see how it behaves (theoritically it should be same as running multiple epochs with persistent agent, so it should not improve a lot)
- Try a different simulator model where you start with cell in center and try a combination of all adjacent cell plants as next states. In this the branching factor is still a constant (2^8 = 256) though it's lot more than 2.
  - Or we can keep the branching factor as 2 and try the states in a pre-defined spiral order (say clock wise) from center cell as well. The basis for these ideas is the nature of reward system where cells are impacted by adjacent cells. But I will know how it performs only after implementing it. 

## References
- https://github.com/pbsinclair42/MCTS/blob/master/mcts.py
