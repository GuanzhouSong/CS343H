Name: Xiaohui Chen
EID: xc2388

q1:
Utility values are updated in initialization. It calls getQValue, which is a helper function computes the q-value using state-action pair. The Utility value is the max of the q values

Also, I had to implement computeQValueFromValues and computeActionFromValues, the first of which computes the Q value and the other get the action that yields to maximum q-value

q2:
Changing noise to 0.0 solves this problem

q3:
The answers are in analysis.py. 

q4:
I added a counter named qValues, which stores the q-values for state-action pairs. Function getQValue returns the q-value accoding to the state-action pair, computeValueFromQValues computes the maximum Q value for a certain state, computeActionFromQValues gets the action yields to maximum q-value, and update function updates the q-value according to the dormula in lecture slides

q5:
Function getAction slects the action according to the exploration rate and q-values

q6:
It is impossible to get a optimal policy by varying the learning rate and exploration rate

q7:
Called the functions previously implemented

q8:
Implement the approximate q-values using the formulas specifies in the project discription
