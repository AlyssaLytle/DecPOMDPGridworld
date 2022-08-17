import numpy as np
from GWwriter import *


rmap1 = np.zeros((4,4))
rmap2 = np.zeros((4,4))
rmap3 = np.zeros((4,4))
rmap_dict = {"rmap1" : rmap1, "rmap2" : rmap2, "rmap3" : rmap3}


obstacle_cost = -5
switch_control_cost = -3
communicate_cost = -1
regular_cost = 0
goal_reward = 10
sink_cost = -1000

transition_likelihood = .1

cost_dict = {"control" : switch_control_cost, "communicate" : communicate_cost, "sink": sink_cost}

for i in range (1,4):
    for j in range(1,4):
        for map_name in rmap_dict.keys():
            map1 = (map_name == "rmap1")
            map2 = (map_name == "rmap2")
            map3 = (map_name == "rmap3")
            if map1 & (i == 3) & (j == 2):
                rmap_dict[map_name][i][j] = obstacle_cost
            elif map2 & (i == 2) & (j == 3):
                rmap_dict[map_name][i][j] = obstacle_cost
            elif map3 & (i == 3) & (j == 1):
                rmap_dict[map_name][i][j] = obstacle_cost
            elif (i == 3) & (j == 3):
                rmap_dict[map_name][i][j] = goal_reward
            else:
                rmap_dict[map_name][i][j] = regular_cost
                
print(rmap1)
print(rmap2)
print(rmap3)

#this is to know which reward maps we could potentially be on                
possible_rmaps = ["rmap1", "rmap2"]
#possible_rmaps = ["rmap1", "rmap3"]
actions = ["down", "right", "communicate", "take-control"]

writer = GWDPOMDP(3,3,rmap_dict, cost_dict,transition_likelihood)

ss1 = [[1,1],"rmap1","H"]
ss2 = [[1,1],"rmap2","H"]
ss3 = [[1,1],"rmap3","H"]
start_states  = [ss1,ss2]
#start_states = [ss1,ss3]

dpomdp = writer.write(start_states, possible_rmaps, actions)

filename = "33gw-late.dpomdp"
f = open(filename, "w")
f.writelines(dpomdp)
f.close()
