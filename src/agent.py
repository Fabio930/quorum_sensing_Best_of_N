# -*- coding: utf-8 -*-
# @author Fabio Oddi <fabioddi24@gmail.com>

import random
import numpy as np
########################################################################################
## Agent
########################################################################################

##########################################################################
# factory to dynamically create agents
class AgentFactory:
    factories = {}

    def add_factory(id, agent_factory):
        AgentFactory.factories[id] = agent_factory
        return
    
    add_factory = staticmethod(add_factory)

    def create_agent(config_element, arena):
        agent_pkg = config_element.attrib.get("pkg")
        if agent_pkg is None:
            return Agent.Factory().create(config_element, arena)
        id = agent_pkg + ".agent"
        agent_type = config_element.attrib.get("type")
        if agent_type is not None:
            id = agent_pkg + "." + agent_type + ".agent"
        return AgentFactory.factories[id].create(config_element, arena)
    
    create_agent = staticmethod(create_agent)


##########################################################################
# the main agent class
class Agent:

    num_agents          = 0
    arena               = None
    r_val               = 0.5
    message_timeout     = 60
    messages_per_step   = 5
    quorum_list_min     = 5
    message_hops        = 1
    eta                 = .6
    model               = "voter"
    r_type              = "static"
    rebroadcast         = "no"
    message_hops        = 10

    class Factory:
        def create(self, config_element, arena): return Agent(config_element, arena)

    ##########################################################################
    # Initialisation of the Agent class
    def __init__(self, config_element, arena):

        # identification
        self.id = Agent.num_agents
        self.options = []
        if self.id == 0:
            Agent.arena = arena
            # parse custon parameters from configuration file
            if config_element.attrib.get("message_timeout") is not None:
                mt = int(config_element.attrib["message_timeout"])
                if mt<=0:
                    print ("[WARNING] for tag <agent> in configuration file the parameter <message_timeout> should be > 0 and integer. Initialized to 60.\n")
                else:
                    Agent.message_timeout = mt
            if config_element.attrib.get("messages_per_step") is not None:
                ms = int(config_element.attrib["messages_per_step"])
                if ms<=0:
                    print ("[WARNING] for tag <agent> in configuration file the parameter <messages_per_step> should be > 0 and integer. Initialized to 5.\n")
                else:
                    Agent.messages_per_step = ms
            if config_element.attrib.get("quorum_list_min") is not None:
                bm = int(config_element.attrib["quorum_list_min"])
                if bm<0 or bm>Agent.arena.num_agents:
                    print ("[WARNING] for tag <agent> in configuration file the parameter <quorum_list_min> should be in [0,num_agents]. Initialized to 5.\n")
                else:
                    Agent.quorum_list_min = bm
            if config_element.attrib.get("r_val") is not None:
                rg = float(config_element.attrib["r_val"])
                if rg<0 or rg>1:
                    print ("[WARNING] for tag <agent> in configuration file the parameter <r_val> should be in [0,1]. Initialized to 0.5.\n")
                else:
                    Agent.r_val=rg
            if config_element.attrib.get("message_hops") is not None:
                mh = int(config_element.attrib["message_hops"])
                if mh<1:
                    print ("[WARNING] for tag <agent> in configuration file the parameter <message_hops> should be greather or equal to 1. Initialized to 1.\n")
                else:
                    Agent.message_hops=mh
            if config_element.attrib.get("eta") is not None:
                et = float(config_element.attrib["eta"])
                if et<0 or et>1:
                    print ("[WARNING] for tag <agent> in configuration file the parameter <eta> should be in [0,1]. Initialized to 0.6.\n")
                else:
                    Agent.eta=et
            if config_element.attrib.get("model") is not None:
                ml = str(config_element.attrib["model"])
                if ml!="voter" and ml!="majority":
                    print ("[WARNING] for tag <agent> in configuration file the parameter <model> should be 'voter' or 'majority'. Initialized to 'voter'.\n")
                else:
                    Agent.model=ml
            if config_element.attrib.get("r_type") is not None:
                rv = str(config_element.attrib["r_type"])
                if rv!="static" and rv!="centralized" and rv!="decentralized":
                    print ("[WARNING] for tag <agent> in configuration file the parameter <r_type> should be 'static' or 'centralized' or 'decentralized'. Initialized to 'static'.\n")
                else:
                    Agent.r_type=rv
            if config_element.attrib.get("rebroadcast") is not None:
                rb = str(config_element.attrib["rebroadcast"])
                if rb!="static" and rb!="centralized" and rb!="decentralized" and rb!="no":
                    print ("[WARNING] for tag <agent> in configuration file the parameter <rebroadcast> should be 'static' or 'centralized' or 'decentralized' or 'no'. Initialized to 'no'.\n")
                else:
                    Agent.rebroadcast=rb
        Agent.num_agents += 1
        return
    
    ##########################################################################
    # generic init function brings back to initial positions
    def init_experiment( self ):
        commit = Agent.arena.num_agents // (Agent.arena.num_options + 1)
        self.committed = -1
        if self.id >= commit:
            for i in range(2,Agent.arena.num_options + 2):
                if self.id < commit*i:
                    self.committed = i-2
                    break
        self.position = [0,0,0,0]
        self.message_buffer = []
        self.quorum_level = 0
        self.r = Agent.r_val
        self.options = np.arange(self.arena.num_options)
        self.best_id = self.arena.get_best_option()
        return
    
    ##########################################################################
    def update(self):
        self.check_best_option()
        self.erase_expired_messages()
        self.take_info()
        self.compute_quorum_level()
        self.decision()
        return
    
    ##########################################################################
    def check_best_option(self):
        max_u = 0
        for i in range(len(self.options)):
            if self.arena.options[i].utility > max_u:
                max_u = self.arena.options[i].utility
                self.best_id = i
        return
    
    ##########################################################################
    def check_majority(self):
        count = [0]*self.arena.num_options
        for i in range(len(self.message_buffer)):
            if self.message_buffer[i][1] > -1:
                count[int(self.message_buffer[i][1])] += 1
        max_u = 0
        best = None
        for i in range(len(count)):
            if count[i] > max_u:
                max_u = count[i]
                best = i
        return best
    
    ##########################################################################
    def voter_model(self):
        message_id = self.take_message_from_buffer()
        if message_id != None:
            if self.committed != -1:
                if int(self.message_buffer[message_id][1]) != self.committed:
                       self.committed = -1
            else:
                self.committed = int(self.message_buffer[message_id][1])
        return

    ##########################################################################
    def majority_model(self):
        commit_to = self.check_majority()
        if commit_to != None:
            if self.committed != -1:
                if commit_to != self.committed:
                    self.committed = -1
            else:
                self.committed = commit_to
        return

    ##########################################################################
    def decision(self):
        if Agent.r_type=="decentralized":
            self.r = 1 - self.quorum_level# if self.committed == -1 else 1-self.quorum_level
        elif Agent.r_type=="centralized":
            self.r = 1 - self.compute_gt()# if self.committed == -1 else 1-self.compute_gt()
        if random.uniform(0,1) < self.r:
            if Agent.model == "voter":
                self.voter_model()
            elif Agent.model == "majority":
                self.majority_model()
        else:
            p = random.uniform(0,1)
            if p < Agent.eta:
                vec = np.delete(self.options,self.best_id)
                option = random.choice(vec)
                if self.committed == -1:
                    self.committed = option
                else:
                    if self.committed != option:
                        self.committed = -1
            else:
                if self.committed == -1:
                    self.committed = self.best_id
                else:
                    if self.committed != self.best_id:
                        self.committed = -1
        return
    
    #########################################################################
    def broadcast(self):
        listened = []
        for s in range(Agent.messages_per_step):
            rnd_id = random.choice(np.arange(self.arena.num_agents))
            while rnd_id == self.id or rnd_id in listened:
                rnd_id = random.choice(np.arange(self.arena.num_agents))
            listened.append(rnd_id)
            if len(self.message_buffer) == 0:
                self.message_buffer = [[rnd_id,self.arena.agents[rnd_id].committed,self.compute_msg_hops()-1,Agent.message_timeout]]
            else:
                write = 1
                for i in range(len(self.message_buffer)):
                    if self.message_buffer[i][0] == rnd_id and self.message_buffer[i][1] == self.arena.agents[rnd_id].committed:
                        write = 0
                        break
                if write == 1: self.message_buffer = np.append(self.message_buffer,[[rnd_id,self.arena.agents[rnd_id].committed,self.compute_msg_hops()-1,Agent.message_timeout]],axis=0)
        return

    #########################################################################
    def re_broadcast(self):
        listened = []
        for s in range(Agent.messages_per_step):
            broadcast = 1
            rnd_id = random.choice(np.arange(self.arena.num_agents))
            while rnd_id == self.id or rnd_id in listened:
                rnd_id = random.choice(np.arange(self.arena.num_agents))
            listened.append(rnd_id)
            if len(self.arena.agents[rnd_id].message_buffer) > 0:
                msg_id = random.choice(np.arange(len(self.arena.agents[rnd_id].message_buffer)))
                if self.arena.agents[rnd_id].message_buffer[msg_id][2] > 0:
                    broadcast = 0
                    if self.arena.agents[rnd_id].message_buffer[msg_id][0] != self.id:
                        if len(self.message_buffer) == 0:
                            self.message_buffer = [[self.arena.agents[rnd_id].message_buffer[msg_id][0],self.arena.agents[rnd_id].message_buffer[msg_id][1],self.arena.agents[rnd_id].message_buffer[msg_id][2]-1,Agent.message_timeout]]
                        else:
                            write = 1
                            for i in range(len(self.message_buffer)):
                                if self.message_buffer[i][0] == self.arena.agents[rnd_id].message_buffer[msg_id][0] and self.message_buffer[i][1] == self.arena.agents[rnd_id].message_buffer[msg_id][1]:
                                    write = 0
                                    break
                            if write == 1: self.message_buffer = np.append(self.message_buffer,[[self.arena.agents[rnd_id].message_buffer[msg_id][0],self.arena.agents[rnd_id].message_buffer[msg_id][1],self.arena.agents[rnd_id].message_buffer[msg_id][2]-1,Agent.message_timeout]],axis=0)

            if broadcast == 1:
                if len(self.message_buffer) == 0:
                    self.message_buffer = [[rnd_id,self.arena.agents[rnd_id].committed,self.compute_msg_hops()-1,Agent.message_timeout]]
                else:
                    write = 1
                    for i in range(len(self.message_buffer)):
                        if self.message_buffer[i][0] == rnd_id and self.message_buffer[i][1] == self.arena.agents[rnd_id].committed:
                            write = 0
                            break
                    if write == 1: self.message_buffer = np.append(self.message_buffer,[[rnd_id,self.arena.agents[rnd_id].committed,self.compute_msg_hops()-1,Agent.message_timeout]],axis=0)
        return
    
    ##########################################################################
    def compute_msg_hops(self):
        if Agent.rebroadcast == "centralized":
            return int(np.max([1,Agent.message_hops*(1-self.compute_gt())]))
        elif Agent.rebroadcast == "decentralized":
            return int(np.max([1,Agent.message_hops*(1-self.quorum_level)]))
        elif Agent.rebroadcast == "static":
            return int(Agent.message_hops)
        else:
            return 1
    
    #########################################################################
    def take_info(self):
        if Agent.rebroadcast == "no":
            self.broadcast()
        else:
            p = random.uniform(0,1)
            if p<.5: self.broadcast()
            else: self.re_broadcast()
        return

    #########################################################################
    def take_message_from_buffer(self):
        if len(self.message_buffer) == 0:
            return None
        rnd_id = random.choice(np.arange(len(self.message_buffer)))
        while self.message_buffer[rnd_id][1] == -1:
            rnd_id = random.choice(np.arange(len(self.message_buffer)))
        return rnd_id

    #########################################################################
    def erase_expired_messages(self):
        to_erase = []
        for i in range(len(self.message_buffer)):
            self.message_buffer[i][-1]-=1
            if self.message_buffer[i][-1] <= 0:
                to_erase.append(i)
        self.message_buffer = np.delete(self.message_buffer,to_erase,axis=0)
        return
    
    #########################################################################
    def compute_quorum_level(self):
        self.quorum_level = 0
        if len(self.message_buffer) < self.quorum_list_min:
            return
        for i in self.message_buffer:
            if i[1] == self.committed:
                self.quorum_level+=1
        if self.quorum_level > 0: self.quorum_level = (self.quorum_level + 1)/(len(self.message_buffer) + 1)
        return
    
    #########################################################################
    def compute_gt(self):
        gt = 1
        for a in Agent.arena.agents:
            if a.id!=self.id and a.committed == self.committed:
                gt += 1
        return gt/Agent.arena.num_agents