Name: Xiaohui Chen
EID: xc2388

q1:
The evaluation function first gets the next state according to current game state and action. This evaluation function evaluates several factors: score, nearest food, and food on new position. If the distance between any ghost and pacman is less than 2, the return value will decrease 1000. Also it will evaluate food distance and the evaluation value will increase 1.0 over nearest food distance. If new position has food, the evaluation value will increase 50. The evaluation value will then add up the score value

q2:
Function utility and terminalTest are implemented in MultiAgentSearchAgent class. Function getAction uses a dictionary whose key is the evluation value and data is the action. For all the possible action of pacman, function miniMax is called. It calls terminal test according to the current depth. Then it calls either maxValue or minValue according to the current agent. At last getActions returns the action with maximum value

q3:
This is similar to q2 but variable alpha and beta are added. Also I use a new object called ActionObject, which stores the evaluation value and action. Instead of processing first pacman state in getActions, it pass the root state to alphaBetaMiniMax to process. Functions maxValue and minValue are implemented according to textbook

q4:
It is very similar to q2 but function exMinValue calculates the value according to the probability. Here each possible action has equal probability. 

q5:
The evaluation function is similar to q1. This evaluation function evaluates several factors: score, nearest food, food on current position, and ghost scared times. If the distance between any ghost and pacman is less than 2, the return value will decrease 1000 unless the minimum ghost panic time is greater than that distance. Also it will evaluate food distance and the evaluation value will increase 1.0 over nearest food distance. If current position has food, the evaluation value will increase 50. The evaluation value will then add up the score value
