# -*- coding: utf-8 -*-
# @author Fabio Oddi <fabioddi24@gmail.com>

import os, csv
from agent import Agent
from datetime import datetime
import numpy as np

class Results:
    def __init__(self,arena):
        self.arena = arena
        self.files = [0]*arena.num_agents
        self.base = os.path.abspath("../results_raw")
        if not os.path.exists(self.base):
            os.mkdir(self.base)
        steps_dir = self.base + "/s#" + str(arena.experiment_length) + "_rec#" + str(arena.rec_time)
        if not os.path.exists(steps_dir):
            os.mkdir(steps_dir)
        rebroad_dir = steps_dir +"/rb#" + Agent.rebroadcast
        if not os.path.exists(rebroad_dir):
            os.mkdir(rebroad_dir)
        agents_dir = rebroad_dir + "/a#" + str(arena.num_agents)
        if not os.path.exists(agents_dir):
            os.mkdir(agents_dir)
        options_dir = agents_dir + "/o#" + str(arena.num_options)
        if not os.path.exists(options_dir):
            os.mkdir(options_dir)
        model_dir = options_dir + "/m#" + Agent.model
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
        r_dir = model_dir + "/rt#" + str(Agent.r_type) + "_rv#" + str(Agent.r_val).replace(".",",")
        if not os.path.exists(r_dir):
            os.mkdir(r_dir)
        eta_dir = r_dir + "/e#" + str(Agent.eta).replace(".",",")
        if not os.path.exists(eta_dir):
            os.mkdir(eta_dir)
        msg_dir = eta_dir + "/qm#" + str(Agent.quorum_list_min) + "_mt#" + str(Agent.message_timeout) + "_ms#" + str(Agent.messages_per_step) + "_mh#" + str(Agent.message_hops)
        if not os.path.exists(msg_dir):
            os.mkdir(msg_dir)
        self.save_path = msg_dir
        return
    
########################################################################################    
    def open_files(self):
        for i in range(len(self.files)):
            self.files[i] = open(self.save_path+"/agent#"+str(i)+"_run#"+str(self.arena.run_id)+"_t#"+str(datetime.now()).replace(".",",").replace(" ","--")+".csv",mode="a",newline="\n")
        return
    
########################################################################################    
    def close_files(self):
        for i in range(len(self.files)):
            self.files[i].close()
        return
    
########################################################################################    
    def print_records(self):
        for a in (range(len(self.files))):
            write_file = csv.writer(self.files[a],delimiter="\t",lineterminator="\n")
            write_file.writerow([len(self.arena.agents[a].message_buffer), self.arena.agents[a].committed, np.round(self.arena.agents[a].quorum_level,3), np.round(self.arena.agents[a].r,3)])
        return