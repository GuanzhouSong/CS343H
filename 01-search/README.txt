Name: Xiaohui Chen
EID: xc2388

q1
This is a simple depth first search algorithm which uses Stack as the queue data structure. The structure of a node is (state,parent node,action,step cost). Solution function takes the goal node as input and returns a list of actions

q2
This is a simple breath first search algorithm which uses Queue as the queue data structure. The structure of a node is (state,parent node,action,step cost). Solution function takes the goal node as input and returns a list of actions

q3
This is a simple uniform cost search algorithm which uses Priority Queue as the queue data structure. The structure of a node is (state,parent node,action,step cost). Solution function takes the goal node as input and returns a list of actions

q4
This is a simple A-star search algorithm which uses Priority Queue with function as the queue data structure. The structure of a node is (state,parent node,action,step cost). Solution function takes the goal node as input and returns a list of actions. The helper function generateFunction returns a function which takes a node as input and returns the total cost from root plus the estimated cost to the goal nose.

q5
The state is defined as  (position,((corner1,visited),(corner2,visited),(corner3,visited),(corner4,visited))). The boolean variable visited indicate whether a corner has been visited. In isGoalState and getSucessor functions, the visited variables would be updated

q6
The heuristic is actually the minimal spamming tree of current position to the unvisited corners using Manhattan distance. Because minimal spamming tree is the shortest distance to all the unvisited corners, the heuristic is admissible. Total distance is calculated using Prime's algorithm.

q7
The heuristic also uses minimal spamming tree. However,the helper function optimizePositions only keep the food positions not in the same x direction or y direction of the current position as well as the furthest straightly reachable food (can approach the food in a stright line without hitting a wall) in North, South, West and East directions. This way the agent can avoid going back and forth while some food positions are in a straight line. Therefore this heuristic is also admissible.  

q8
The function findPathToClosestDot returns a list of actions using uniform cost search. In AnyFoodSearchProblem, a goal state is determined if there is food in current position.

Minicontest is not implemented.
