import sys
import graphviz

from numpy import zeros
from ArrayTree import ArrayTree
sys.path.append("..")
from GWwriter import *

def get_most_recent_obs(edge):
    res = edge.split(',')
    return res[-1]

def get_node_and_edge(line):
    [edge, node] = line.split("-->")
    if len(edge) > 3:
        edge = edge[1:-2]
    else:
        edge = ""
    node = node[1:-1]
    print(node)
    return [edge,node]

def get_trees(filename, agent0_branch_size, agent1_branch_size):   
    value = -1000
    f = open(filename, "r")
    #skip first 3 lines
    if f.readline():
        f.readline()
        f.readline()
        flag = True
        edges = []
        nodes = []
        while(flag):
            l = f.readline()
            if l:
                if l[0] == "(":
                    [edge, node] = get_node_and_edge(l)
                    nodes.append(node)
                    edges.append(edge)
                else:
                    flag = False
            else:
                flag = False
        agent0_tree = ArrayTree(agent0_branch_size, nodes, edges)
        flag = True
        edges = []
        nodes = []
        while(flag):
            l = f.readline()
            if l:
                if l[0] == "(":
                    [edge, node] = get_node_and_edge(l)
                    nodes.append(node)
                    edges.append(edge)
                else:
                    if l[:6] == "Sample":
                        value = l[17:-19]
            else:
                flag = False
        agent1_tree = ArrayTree(agent1_branch_size, nodes, edges) 
        return [agent0_tree, agent1_tree, value]
    else:
        return []


#If machine communicates, human only observes whatever the machine observed

def get_graph_viz_limit_branches(human_tree, machine_tree, start_state, trans_prob, rmap_list):
        #returns trees in graph_viz format including only relevant branches
        #ONLY WRITTEN FOR TREES OF HEIGHT 1 FOR NOW
        if trans_prob:
            #If rmap is changing (transitional probabilities), 
            machine_obs = rmap_list
        else:
            [location, rmap_name, control] = start_state
            machine_obs = [rmap_name]
        output1 = 'digraph human_tree {\n'
        output2 = 'digraph machine_tree {\n'
        output1 += 'edge [dir=none];\n'
        output2 += 'edge [dir=none];\n'
        nodes_h = ""
        edges_h = ""
        nodes_m = ""
        edges_m = ""
        output1 += 'node0 [ label = "' + str(human_tree.nodes[0]) + '" ];\n'
        output2 += 'node0 [ label = "' + str(machine_tree.nodes[0]) + '" ];\n'
        num_hum_nodes = 1
        num_mach_nodes = 1
        hum_parent_ids = [-1]*len(human_tree.nodes)
        mach_parent_ids = [-1]*len(machine_tree.nodes)
        hum_parent_ids[0] = 0
        mach_parent_ids[0] = 0
        for i in range(1,len(human_tree.nodes)):
            human_edge = get_most_recent_obs(human_tree.edges[i])
            machine_edge = get_most_recent_obs(machine_tree.edges[i])
            parent_idx = human_tree.get_parent_idx(i) #idx should be same for both human or machine
            prev_mach_action = machine_tree.nodes[parent_idx]
            curr_mach_obs = get_most_recent_obs(machine_tree.edges[i])
            if prev_mach_action == "communicate":
                #if machine communicates
                if trans_prob:
                    #if probabilistic transitions, observe what machine observes
                    human_obs = [curr_mach_obs]
                else:
                    #otherwise, just observe what state the machine KNOWS they're always in
                    human_obs = machine_obs
            else: 
                human_obs = rmap_list
            m_parent_id = mach_parent_ids[parent_idx]
            h_parent_id = hum_parent_ids[parent_idx]
            if (human_edge in human_obs) & (h_parent_id != -1):
                hum_parent_ids[i] = num_hum_nodes
                nodes_h += 'node' + str(num_hum_nodes) + ' [ label = "' + str(human_tree.nodes[i]) + '" ];\n'
                edges_h += 'node' + str(h_parent_id) + ' -> ' 
                edges_h += 'node' + str(num_hum_nodes) + ' [label="' + str(get_most_recent_obs(human_tree.edges[i])) + '"];\n'
                num_hum_nodes += 1
            if (machine_edge in machine_obs) & (m_parent_id != -1):
                mach_parent_ids[i] = num_mach_nodes
                nodes_m += 'node' + str(num_mach_nodes) + ' [ label = "' + str(machine_tree.nodes[i]) + '" ];\n'
                edges_m += 'node' + str(m_parent_id) + ' -> ' 
                edges_m += 'node' + str(num_mach_nodes) + ' [label="' + str(get_most_recent_obs(machine_tree.edges[i])) + '"];\n'
                num_mach_nodes += 1
        output1 += nodes_h + edges_h
        output2 += nodes_m + edges_m
        output = [output1 + '}', output2 + '}']
        print(hum_parent_ids)
        return output

''' 
!!!! Values :
'''
start_state = [[1,1],"rmap1","H"]
trans_prob = False
rmap_list = ["rmap1", "rmap2"]

'''Read Results'''
[h_tree, m_tree, value] = get_trees("Ex1-Res", 2, 2)
'''Make .dot files'''
[hgraph, mgraph] = get_graph_viz_limit_branches(h_tree, m_tree, start_state, trans_prob, rmap_list)
f = open("htree.dot", "w")
f.writelines(hgraph)
f.close()
g = open("mtree.dot", "w")
g.writelines(mgraph)
g.close()
'''Generate Graphviz Images'''
graph = graphviz.Source.from_file('htree.dot')
graph.format = 'png'
graph.view()
#tree_name = "figs/Human"
#filename = graph.render(filename=tree_name)

graph = graphviz.Source.from_file('mtree.dot')
graph.format = 'png'
graph.view()
#tree_name = "figs/Machine"
#filename = graph.render(filename=tree_name)