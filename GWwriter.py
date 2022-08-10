def state_to_string(state):
    if (isinstance(state, list)):
        [location, rmap_name, control] = state
        [i,j] = location
        name = "loc" + str(i) + str(j) + "-" + rmap_name + "-" + control[0]
        return name
    else:
        #hopefully, this means it's already a string
        return state

def trans_string(h_action, m_action, start, next, prob):
    tline = "T : " + h_action + " " + m_action + " : " 
    tline += state_to_string(start) + " : "
    tline += state_to_string(next) + " : "
    tline += str(prob) + "\n"
    return tline

def rew_string(h_action, m_action, start, reward):
    r_str = "R: " + h_action + " " + m_action + " : "
    r_str += state_to_string(start) + " : * : * : "
    r_str += str(reward) + "\n"
    return r_str

def is_allowed_machine(start_state, action):
    #returns true if an action is allowed
    [start_loc, start_rmap_name, start_control] = start_state
    ctrl_actions = ["up", "down", "left", "right"]
    no_ctrl_actions = ["take-control", "communicate"]
    if (start_control == "M") & (action in ctrl_actions):
        return True
    elif (start_control == "H") & (action in no_ctrl_actions):
        return True
    else:
        return False
        
def is_allowed_human(start_state, action):
    #returns true if an action is allowed
    [start_loc, start_rmap_name, start_control] = start_state
    ctrl_actions = ["up", "down", "left", "right"]
    no_ctrl_actions = ["take-control", "communicate"]
    if (start_control == "H") & (action in ctrl_actions):
        return True
    elif (start_control == "M") & (action in no_ctrl_actions):
        return True
    else:
        return False

class GWDPOMDP:
    
    def __init__(self, width, height, rmaps_dict, cost_dict):
        self.width = width
        self.height = height
        self.rmaps = rmaps_dict
        self.costs = cost_dict
        
    def move(self, start : str, action : str) -> list:
        [i,j] = start
        if action == "down":
            if i < self.height:
                i += 1
        if action == "up":
            if i > 1:
                i -= 1
        if action == "right":
            if j < self.width:
                j += 1
        if action == "left":
            if j > 1:
                j -= 1
        return [i,j]
    
    def transition(self, start : str, h_action : str, m_action : str) -> list:
        [start_loc, start_rmap_name, start_control] = start
        human_in_control = (start_control == "H")
        machine_in_control = (start_control == "M")
        if human_in_control:
            new_loc = self.move(start_loc, h_action)
            if m_action == "take-control":
                new_control = "M"
            else:
                new_control = start_control
        elif machine_in_control:
            new_loc = self.move(start_loc, m_action)
            if h_action == "take-control":
                new_control = "H"
            else:
                new_control = start_control
        else:
            print("ERROR! Not reading control correctly.")
            new_loc = [-1,-1]
            new_control = "ERROR"
        return [new_loc, start_rmap_name, new_control]    
    
    def get_transition_line(self,start_state : str, h_action : str, m_action : str) -> str:
        tline = "T : " + h_action + " " + m_action + " : " + state_to_string(start_state) + " : "
        next_state = self.transition(start_state, h_action, m_action)
        tline += state_to_string(next_state) + " : 1\n"
        return tline
                
    def get_reward(self, next_state: list, action: list) -> int:
        [end_loc, end_rmap_name, end_control] = next_state
        #location cost is defined in rmap
        [h_action, m_action] = action
        [i,j] = end_loc
        end_rmap = self.rmaps[end_rmap_name]
        reward = end_rmap[i][j]
        if (h_action == "communicate") | (m_action == "communicate"):
            reward += self.costs["communicate"]
        elif (h_action == "take-control") | (m_action == "take-control"):
            reward += self.costs["control"]
        return int(reward)
    

    def get_reward_line(self, start_state : str, action :str) -> str:
        [h_action, m_action] = action
        next_state = self.transition(start_state, h_action, m_action)
        reward = self.get_reward(next_state, action)
        r_str = "R: " + h_action + " " + m_action + " : "
        r_str += state_to_string(start_state) + " : * : * : "
        r_str += str(reward) + "\n"
        return r_str
        
    def get_observation(self, next_state : str, action : str, possible_rmaps : list) -> list:
        [h_action, m_action] = action
        [loc, rmap_name, control] = next_state
        h_obs = {}
        if m_action == "communicate":
            h_obs[rmap_name] = 1
        else:
            #human observes all reward maps with equal likelihood
            likelihood = 1/len(possible_rmaps)
            for elem in possible_rmaps:
                h_obs[elem] = likelihood
        m_obs = rmap_name
        return [h_obs, m_obs]
    
    def get_observation_strings(self, start_state : str, action :str, possible_rmaps : list) -> str:
        [h_action, m_action] = action
        next_state = self.transition(start_state, h_action, m_action)
        [h_obs, m_obs] = self.get_observation(next_state, action, possible_rmaps)
        obs_strs = ""
        obs_prefix = "O: " + h_action + " " + m_action + " : " 
        obs_prefix += state_to_string(next_state) + " : "
        for rmap in h_obs.keys():
            obs_strs += obs_prefix + rmap + " " + m_obs + " : " + str(h_obs[rmap]) + "\n"
        return obs_strs
    
    def write(self, start_state: list, possible_rmaps : list, actions : list) -> str:
        output = "agents: 2\n"
        output += "discount: 1\n"
        output += "values: reward\n"
        output += "states:"
        states = []
        for rmap in possible_rmaps:
            for i in range(1,self.height+1):
                for j in range(1,self.width+1):
                    for ctrl in ["H", "M"]:
                        state = [[i,j], rmap, ctrl]
                        states.append(state)
                        output += " " + state_to_string(state)
        output += "\n"
        output += "start include: " + state_to_string(start_state) + "\n"
        output += "actions: \n"
        action_str = ""
        for elem in actions:
            action_str += elem + " "
        output += action_str[:-1] + "\n"
        output += action_str[:-1] + "\n"
        output += "observations:\n"
        obs_str = ""
        for rmap in possible_rmaps:
            obs_str += rmap + " "
        output += obs_str[:-1] + "\n"
        output += obs_str[:-1] + "\n"
        transitions = ""
        observations = ""
        rewards = ""
        #non_sink_states = states - ["sink"]
        for s in states:
            for m_action in actions:
                for h_action in actions:
                    if (is_allowed_human(s,h_action) & is_allowed_machine(s,m_action)):
                        transitions += self.get_transition_line(s,h_action,m_action)
                        observations += self.get_observation_strings(s,[h_action,m_action],possible_rmaps)
                        rewards += self.get_reward_line(s,[h_action,m_action])         
        output += transitions
        output += observations
        output += rewards
        return output
                    
                    
                    
                      
                
            
    