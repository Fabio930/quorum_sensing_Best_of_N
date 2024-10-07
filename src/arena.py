# -*- coding: utf-8 -*-
# @author Fabio Oddi <fabioddi24@gmail.com>

import importlib
import sys, random
from agent import AgentFactory
from option import OptionFactory

########################################################################################
## Arena
########################################################################################
# factory to dynamically create the arena
class ArenaFactory:
    factories = {}
    
    def add_factory(id, arena_factory):
        ArenaFactory.factories[id] = arena_factory
        return
    
    add_factory = staticmethod(add_factory)

    def create_arena(config_element):
        arena_pkg = config_element.attrib.get("pkg")
        if arena_pkg is None:
            return Arena.Factory().create(config_element)
        id = arena_pkg + ".arena"
        return ArenaFactory.factories[id].create(config_element)
    
    create_arena = staticmethod(create_arena)

##########################################################################
# main arena class
class Arena:
    'this class manages the enviroment of the multi-agent simualtion'

    class Factory:
        def create(self, config_element): return Arena(config_element)

    ##########################################################################
    # standart class init
    def __init__( self, config_element ):
        # random seed
        self.num_runs = 1 if config_element.attrib.get("num_runs") is None else int(config_element.attrib["num_runs"])
        self.run_id = 0
        self.timestep_length = 1 if config_element.attrib.get("timestep_length") is None else float(config_element.attrib.get("timestep_length"))
        self.num_steps = 0
        self.experiment_length = 0 if config_element.attrib.get("experiment_length") is None else int(config_element.attrib["experiment_length"]) # 0 means no limit
        self.variation_time_init = 0 if config_element.attrib.get("variation_time") is None else int(config_element.attrib["variation_time"]) # 0 means no change
        self.rec_time = 0 if config_element.attrib.get("rec_time") is None else int(config_element.attrib["rec_time"]) # 0 means no records
        self.num_agents = 1
        self.num_options = 1
        self.agents = []
        self.options = []
        self.variation_time = self.variation_time_init
        na = config_element.attrib.get("num_agents")
        if na is None:
            print ("[WARNING] missing attribute <num_agents> in tag <arena>. Set to default value 1.\n")
        else:
            na = int(na)
            if na<=0:
                print ("[WARNING] attribute <num_agents> in tag <arena> should be > 0. Set to default value 1.\n")
            else:
                self.num_agents = na
        no = config_element.attrib.get("num_options")
        if no is None:
            print ("[WARNING] missing attribute <num_options> in tag <arena>. Set to default value 1.\n")
        else:
            no = int(no)
            if no<=0:
                print ("[WARNING] attribute <num_options> in tag <arena> should be > 0. Set to default value 1.\n")
            else:
                self.num_options = no
        self.create_agents(config_element)
        self.create_options(config_element)
        return
    
    ##########################################################################
    # create the agents
    def create_agents( self, config_element ):
        # Get the tree correspnding to agent parameters
        agent_config= config_element.find('agent')
        if agent_config is None:
            print ("[ERROR] required tag <agent> in configuration file is missing")
            sys.exit(1)
        # dynamically load the desired module
        lib_pkg    = agent_config.attrib.get("pkg")
        if lib_pkg is not None:
            importlib.import_module(lib_pkg + ".agent", lib_pkg)
        for i in range(0,self.num_agents):
            self.agents.append(AgentFactory.create_agent(agent_config, self))
        return
    
    ##########################################################################
    # create the options
    def create_options( self, config_element ):
        # Get the tree correspnding to option parameters
        option_config= config_element.find('option')
        if option_config is None:
            print ("[ERROR] required tag <option> in configuration file is missing")
            sys.exit(1)
        # dynamically load the desired module
        lib_pkg    = option_config.attrib.get("pkg")
        if lib_pkg is not None:
            importlib.import_module(lib_pkg + ".option", lib_pkg)
        for i in range(0,self.num_options):
            self.options.append(OptionFactory.create_option(option_config, self))
        return

    ##########################################################################
    # set the random seed
    def set_random_seed( self , seed = None):
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()
        return

    ##########################################################################
    # initialisation/reset of the experiment variables
    def init_experiment(self, results):
        self.num_steps = 0
        self.results = results
        self.variation_time = self.variation_time_init
        self.change = 1
        self.rcd_permission = True if self.rec_time>0 and self.experiment_length>0 else False
        self.set_random_seed(self.run_id) if self.run_id > 0 else self.set_random_seed()
        for a in self.agents:
            a.init_experiment()
        for o in self.options:
            o.init_experiment()
        print("Experiment started")

    ##########################################################################
    # run experiment until finished
    def run_experiment( self ):
        while not self.experiment_finished():
            self.update()
            print('Running...    '+str(self.num_steps), end=" steps\r", flush=True)
        return

    ##########################################################################
    # updates the simulation state
    def update( self ):
        if self.rcd_permission and self.num_steps%self.rec_time==0:
            self.results.print_records()
        ag = random.choice(self.agents)
        ag.update()
        self.num_steps += 1
        if self.variation_time > 0 and self.change == 1 and self.num_steps >= self.variation_time:
            self.change = 0
            flag = self.options[0].utility
            self.options[0].utility = self.options[1].utility
            self.options[1].utility = flag

    ##########################################################################
    # determines if an exeperiment is finished
    def experiment_finished( self):
        if (self.experiment_length > 0) and (self.experiment_length <= self.num_steps):
            print("Run finished")
            return 1
    
    ##########################################################################
    def get_best_option(self):
        best_id = 0
        max_u = 0
        for i in range(len(self.options)):
            if self.options[i].utility > max_u:
                max_u = self.options[i].utility
                best_id = i
        return best_id
    
    ##########################################################################
    def get_committed_to(self,id):
        num = 0
        for a in self.agents:
            if a.committed == id:
                num+=1
        return num