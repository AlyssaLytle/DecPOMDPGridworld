import copy


class ArrayTree:

    #child_idx = given a node p, which index child is c?
    #idx = general index in tree
    #num_branches = number of branches

    def __init__(self, num_branches):
        self.nodes = []
        self.edges = []
        self.num_branches = num_branches
    
    def __init__(self, num_branches, inp_nodes, inp_edges):
        self.nodes = inp_nodes
        self.edges = inp_edges
        self.num_branches = num_branches

    def child_idx_from_idx(self, idx):
        if (idx % self.num_branches) == 0:
            return (self.num_branches - 1)
        else:
            return ((idx % self.num_branches) - 1)

    
    def get_parent_idx(self, idx):
        mod_child_idx = (self.child_idx_from_idx(idx) + 1)
        return int(((idx - mod_child_idx)/self.num_branches))


    def get_children(self, parent_idx):
        children = []
        first_child = parent_idx * self.num_branches + 1
        if len(self.nodes) > first_child:
            for x in range(0,self.num_branches):
                children.append(self.nodes[first_child + x])
        return children
    
    def get_children_indexes(self, parent_idx):
        children = []
        first_child = parent_idx * self.num_branches + 1
        if len(self.nodes) > first_child:
            for x in range(0,self.num_branches):
                children.append(first_child + x)
        return children

    def get_height(self):
        idx = len(self.nodes)-1
        height = 0
        while idx > 0:
            height += 1
            idx = self.get_parent_idx(idx)
        return height
    
    def get_childs_tree_idx(self, parent_idx, child_idx):
        return self.num_branches * parent_idx + child_idx + 1
    
    def has_child(self, parent_idx):
        return ((len(self.nodes)-1)  >= self.get_childs_tree_idx(parent_idx, 0))
    
    def get_leaves(self):
        idx = 0
        while self.has_child(idx):
            idx = self.get_childs_tree_idx(idx,0)
        return self.nodes[idx:]
    
    def add_level(self, inp_nodes, inp_edges):
        #input array should be the proper length
        #check if len(inp_array) == len(self.get_leaves())*num_branches
        self.nodes.extend(inp_nodes)
        self.edges.extend(inp_edges)
        
    def copy_and_add_level(self, inp_nodes, inp_edges):
        #input array should be the proper length
        #check if len(inp_array) == len(self.get_leaves())*num_branches
        tree = ArrayTree(self.num_branches, self.nodes.copy(), self.edges.copy())
        tree.nodes.extend(inp_nodes)
        tree.edges.extend(inp_edges)
        return tree
    
    def fully_explored(self,horizon):
        #height of tree should be 1 less than horizon, e.g. if horizon is 1, return tree of height 0
        #print("Height: " + str(self.get_height()))
        return ((horizon - 1) <= (self.get_height()))
    
    def get_level(self, idx):
        #given an index, tells you what level of the tree it is on
        level = 0
        while idx > 0:
            level += 1
            idx = self.get_parent_idx(idx)
        return int(level)
    
    def print(self):
        print(self.nodes[0])
        for i in range(1,len(self.nodes)):
            print("-" * self.get_level(i) + " Obs: " + str(self.edges[i]) + " -> Act: " + str(self.nodes[i]))
    
   
    def get_graph_viz(self, tree_name):
        #returns tree in graph_viz format
        output = ''
        output += 'digraph ' + tree_name + ' {\n'
        output += 'edge [dir=none];\n'
        for i in range(len(self.nodes)):
            output += 'node' + str(i) + ' [ label = "' + str(self.nodes[i]) + '" ];\n'
        for i in range(1,len(self.nodes)):
            output += 'node' + str(self.get_parent_idx(i)) + ' -> ' 
            output += 'node' + str(i) + ' [label="' + str(self.edges[i]) + '"];\n'
        output += "}"
        return output
            
    def get_child_edge_idx_with_value(self, parent_idx, value):
        for child_idx in self.get_children_indexes(parent_idx):
            if self.edges[child_idx] == value:
                return child_idx
        print("ERROR. Observation not found")
        return " "
    
