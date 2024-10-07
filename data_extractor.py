import numpy as np
import os, csv, math, gc

class Results:
        
##########################################################################################################
    def __init__(self):
        self.bases=[]
        self.base = os.path.abspath("")
        for elem in sorted(os.listdir(self.base)):
            if '.' not in elem:
                selem=elem.split('_')
                if selem[0] in ("results"):
                    self.bases.append(os.path.join(self.base, elem))

##########################################################################################################
    def extract_k_data(self, base, max_steps, rec_time, dif_time, communication, n_agents, n_options, model, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, msg_path):
        num_runs        = int(len(os.listdir(msg_path))/n_agents)
        msgs_bigM_1     = [np.array([])] * n_agents
        commit_bigM_1   = [np.array([])] * n_agents
        quorum_bigM_1   = [np.array([])] * n_agents
        r_bigM_1        = [np.array([])] * n_agents
        msgs_M_1        = [np.array([],dtype=int)] * num_runs # x num_samples
        commit_M_1      = [np.array([],dtype=int)] * num_runs # x num_samples
        quorum_M_1      = [np.array([],dtype=float)] * num_runs # x num_samples
        r_M_1           = [np.array([],dtype=float)] * num_runs # x num_samples
        for elem in sorted(os.listdir(msg_path)):
            if '.' in elem:
                selem = elem.split('.')
                if selem[-1]=="csv":
                    seed = int(selem[0].split('_')[1].split('#')[1])
                    agent_id = int(selem[0].split('_')[0].split('#')[1])
                    with open(os.path.join(msg_path, elem), newline='') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            for val in row:
                                val                 = val.split('\t')
                                msgs_M_1[seed-1]    = np.append(msgs_M_1[seed-1],int(val[0]))
                                commit_M_1[seed-1]  = np.append(commit_M_1[seed-1],int(val[1]))
                                quorum_M_1[seed-1]  = np.append(quorum_M_1[seed-1],float(val[2]))
                                r_M_1[seed-1]       = np.append(r_M_1[seed-1],float(val[3]))
                    if len(msgs_M_1[seed-1])!=max_steps/rec_time: print(msg_path,'\n',"run:",seed,"agent:",agent_id,"num lines:",len(msgs_M_1[seed-1]))
                    sem = 1
                    for i in range(num_runs):
                        if len(msgs_M_1[i])==0:
                            sem = 0
                            break
                    if sem == 1:
                        msgs_bigM_1[agent_id]       = msgs_M_1
                        commit_bigM_1[agent_id]     = commit_M_1
                        quorum_bigM_1[agent_id]     = quorum_M_1
                        r_bigM_1[agent_id]          = r_M_1
                        msgs_M_1                    = [np.array([],dtype=int)] * num_runs
                        commit_M_1                  = [np.array([],dtype=int)] * num_runs
                        quorum_M_1                  = [np.array([],dtype=float)] * num_runs
                        r_M_1                       = [np.array([],dtype=float)] * num_runs
        messages        = self.rearrange_matrix(msgs_bigM_1)
        commits         = self.rearrange_matrix(commit_bigM_1)
        quorums         = self.rearrange_matrix(quorum_bigM_1)
        r_params        = self.rearrange_matrix(r_bigM_1)
        avg_messages    = self.compute_avg_msgs(messages)
        self.dump_msgs("messages_resume.csv", [max_steps, rec_time, dif_time, communication, n_agents, n_options, model, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, avg_messages])
        del avg_messages, msgs_bigM_1, msgs_M_1
        gc.collect()

#########################################################################################################
    def rearrange_matrix(self,data):
        return np.transpose(data, (1,0,2))

##########################################################################################################
    def compute_avg_msgs(self,messages):
        print("--- Computing avg buffer dimension ---")
        tot_avg = [0]*len(messages[0][0])
        for i in range(len(messages)):
            for j in range(len(messages[i])):
                for t in range(len(messages[i][j])):
                    tot_avg[t] += messages[i][j][t]
        for t in range(len(tot_avg)):
            tot_avg[t] = np.round(tot_avg[t]/(len(messages)*len(messages[0])),3)
        return tot_avg

##########################################################################################################
    def dump_msgs(self,file_name,data):
        header = ["max_steps", "rec_time", "dif_time", "rebroadcast", "n_agents", "n_options", "model", "r_value", "eta_value", "min_list_quorum", "msg_timeout", "msg_x_step", "msg_hops", "data"]
        write_header = not os.path.exists(os.path.join(os.path.abspath(""), "msgs_data", file_name))
        
        if not os.path.exists(os.path.join(os.path.abspath(""), "msgs_data")):
            os.mkdir(os.path.join(os.path.abspath(""), "msgs_data"))
        
        with open(os.path.join(os.path.abspath(""), "msgs_data", file_name), mode='a', newline='\n') as fw:
            fwriter = csv.writer(fw, delimiter='\t')
            if write_header:
                fwriter.writerow(header)
            for i in range(len(data)):
                if data[i]==None:
                    data[i]='-'
            fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]])
        return
    
##########################################################################################################
    def compute_average_quorum_on_options(self,commits,quorums):
        return
    
##########################################################################################################
    def dump_quorum(self,file_name,data):
        return
    
##########################################################################################################
    def compute_average_r_value_on_options(self,commits,r_params):
        return

##########################################################################################################
    def dump_r_values(self,file_name,data):
        return
    
##########################################################################################################
    def extract_median(self,array):
        median = 0
        sortd_arr = np.sort(array)
        if len(sortd_arr)%2 == 0:
            median = (sortd_arr[(len(sortd_arr)//2) -1] + sortd_arr[(len(sortd_arr)//2)]) * .5
        else:
            median = sortd_arr[math.floor(len(sortd_arr)/2)]
        return median