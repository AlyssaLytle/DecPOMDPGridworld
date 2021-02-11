# DecPOMDPGridworld
This directory contains problem examples meant for the [MADP Toolbox](http://www.fransoliehoek.net/fb/index.php?fuseaction=software.madp). 

![Reward Map 1](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/Ex1Rmap.png)


## Example 1: 23gwsimple
This is a basic 2x3 gridworld example. Two agents are moving around a reward map (shown in the image).   They both must make the same action for it to take effect. (e.g. to move right they both must choose "right" as their action.) They start at the top right corner and must solve to navigate. 

![Reward Maps 1 and 2](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/ExRmap3.png)
![What the policy should look like](https://github.com/AlyssaByrnes/DecPOMDPGridworld/blob/master/Policy.png)


## Example 2: 23gw-rmap
This is similar to Example 1 except now there are two reward maps. The agents are able to observe what reward map they are on and navigate accordingly. 

## Example 3: 23gw-comm
This expands on the previous examples. Now, for actions, they can either move or move AND communicate. When they communicate, they are able to observe what reward map they are on. 
