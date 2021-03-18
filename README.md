# DecPOMDPGridworld
This directory contains problem examples meant for the [MADP Toolbox](http://www.fransoliehoek.net/fb/index.php?fuseaction=software.madp). 



## Example 1: 23gwsimple

![Reward Map 1](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/Ex1Rmap.png)

This is a basic 2x3 gridworld example. Two agents are moving around a reward map (shown in the image).   They both must make the same action for it to take effect. (e.g. to move right they both must choose "right" as their action.) They start at the top right corner and must solve to navigate. 

### Solution Policy 
![Solution Policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/simple-sol.png)




## Example 2: 23gw-rmap

![Reward Maps 1 and 2](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/ExRmap3.png)
![What the policy should look like](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/Policy.png)

This is similar to Example 1 except now there are two reward maps. The agents are able to observe what reward map they are on and navigate accordingly. 

### Solution Policy 
![Solution Policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/Rmap-sol.png)

## Example 3: 23gw-comm
This expands on the previous examples. Now, for actions, they can either move or move AND communicate. Communication comes at a small cost. When they communicate, they are able to observe what reward map they are on. 

### Solution Policy 
![Solution Policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/comm-sol.png)

## Example 4: 23gw-nocomm
This is the same as the previous example, except the reward maps are different.

![New Rmaps](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/no-comm-rmaps.png)

Note that, regardless of which map the agents are on, there is always a path that doesn't hit an obstacle. This makes communication unnecessary. This is shown in the policy. 

![No Communication Policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/no-comm-example.png)

## Example 5: 23gw-machine knows

In this example, we are back to the original two reward maps. The human is the one deciding movement in the environment and the machine is the one deciding whether or not to communicate. The machine knows everything about the environment. You can see that the machine decides to communicate and therefore the human traverses the obstacles correctly. 

![Human Policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/humanpol.png)

![Machine Policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/machinepol.png)


## Example 6: 23gw-sharedctrl

In this example, the machine knows everything and has the option to communicate or take control.  The cost to communicate is -1 and the cost to take control is -5. The machine chooses to communicate and not take control.

![human policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/human-in-control.png)

![machine policy](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/machine-communicate.png)

## Example 7: 23gw-sharedctrl2

In this example, it's the same as before but the cost to communicate is -5 and the cost to take control is -1.  In this one, the machine chooses to take control. 

![Machine takes control](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/machine-take-control.png)
