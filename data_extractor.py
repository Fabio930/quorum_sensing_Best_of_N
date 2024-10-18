import numpy as np
import os, csv, math, gc

class Results:
        
##########################################################################################################
    def __init__(self):
        self.threshold = 0.9
        self.base = os.path.abspath("")
        self.input_folders  = []
        self.output_folders = []
        for raw_results_dir in sorted(os.listdir(self.base)):
            if '.' not in raw_results_dir and ("results_raw") in raw_results_dir:
                self.input_folders.append(os.path.join(self.base, raw_results_dir))
                self.output_folders.append(os.path.join(self.base, raw_results_dir.replace("results_raw","results_processed")))
        for i in range(len(self.output_folders)):
            if not os.path.exists(self.output_folders[i]):
                os.mkdir(self.output_folders[i])

##########################################################################################################
    def extract_k_data(self, base, max_steps, rec_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, msg_path):
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
                        if len(msgs_M_1[i]) == 0:
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
        self.dump_msgs(base,"messages_resume.csv", [max_steps, rec_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, avg_messages])
        del avg_messages, messages, msgs_bigM_1, msgs_M_1
        times       = self.compute_completion_times(commits,int(max_steps//rec_time),n_agents,n_options)
        median_time = self.extract_median(times,int(max_steps//rec_time))
        self.dump_median_time(base,"times_resume.csv", [max_steps, rec_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, median_time])
        del times, median_time
        residence, quorum, control_parameter = self.compute_average_residence_quorum_controlParam_on_options(commits,quorums,r_params,n_agents,n_options)
        del commits, commit_bigM_1, commit_M_1, quorums, quorum_bigM_1, quorum_M_1, r_params, r_bigM_1, r_M_1
        self.dump_residence(base,"residence_resume.csv", [max_steps, rec_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, residence])
        self.dump_quorum(base,"quorum_resume.csv", [max_steps, rec_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, quorum])
        if r_type!="static": self.dump_control_parameter(base,"controlParameter_resume.csv", [max_steps, rec_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, control_parameter])
        del residence, quorum, control_parameter
        gc.collect()

#########################################################################################################
    def rearrange_matrix(self,data):
        return np.transpose(data, (1,0,2))

##########################################################################################################
    def extract_median(self,array,max_time):
        median = -1
        no_end_count = 0
        for i in range(len(array)):
            if array[i] > max_time: no_end_count += 1
        sortd_arr = np.sort(array)
        if len(sortd_arr)%2 == 0:
            if no_end_count < len(sortd_arr)/2:
                median = (sortd_arr[math.floor(len(sortd_arr)/2) - 1] + sortd_arr[math.floor(len(sortd_arr)/2)]) * .5
        else:
            if no_end_count < math.ceil(len(sortd_arr)/2):
                median = sortd_arr[math.floor(len(sortd_arr)/2)]
        return median
    
##########################################################################################################
    def compute_avg_msgs(self,messages):
        print("--- Computing average buffer dimension ---")
        tot_avg = [0]*len(messages[0][0])
        for i in range(len(messages)):
            for j in range(len(messages[i])):
                for t in range(len(messages[i][j])):
                    tot_avg[t] += messages[i][j][t]
        for t in range(len(tot_avg)):
            tot_avg[t] = np.round(tot_avg[t]/(len(messages)*len(messages[0])),3)
        return tot_avg
    
##########################################################################################################
    def compute_completion_times(self,commits,max_time,num_agents,num_options):
        print("--- Computing median completion times ---")
        times = []
        times = np.array([max_time + 1] * len(commits),dtype=int)
        for i in range(len(commits)):
            found = False
            for k in range(len(commits[i][0])):
                count = [0] * num_options
                for j in range(len(commits[i])):
                    if commits[i][j][k] >= 0:
                        count[commits[i][j][k]] += 1
                for j in range(len(count)):
                    count[j] = count[j] / num_agents
                    if count[j] >= self.threshold:
                        times[i] = k
                        found = True
                        break
                if found: break
        return times
    
##########################################################################################################
    def compute_average_residence_quorum_controlParam_on_options(self,commits,quorums,r_params,num_agents,num_options):
        print("--- Computing average quorum on options ---")
        output_agents = np.array([[0] * len(commits[0][0])] * (num_options+1),dtype=float)
        output_quorum = np.array([[0] * len(commits[0][0])] * (num_options+1),dtype=float)
        output_paramR = np.array([[0] * len(commits[0][0])] * (num_options+1),dtype=float)
        for i in range(len(commits)):
            committed_agents    = np.array([[0] * len(commits[0][0])] * (num_options+1),dtype=float)
            flag_q              = np.array([[0] * len(commits[0][0])] * (num_options+1),dtype=float)
            flag_r              = np.array([[0] * len(commits[0][0])] * (num_options+1),dtype=float)
            for j in range(len(commits[i])):
                for k in range(len(commits[i][j])):
                    committed_agents[commits[i][j][k]][k] += 1
                    flag_q[commits[i][j][k]][k] += quorums[i][j][k]
                    flag_r[commits[i][j][k]][k] += r_params[i][j][k]
            for j in range(num_options+1):
                for k in range(len(flag_q[0])):
                    if committed_agents[j][k] > 0:
                        flag_q[j][k] = flag_q[j][k]/committed_agents[j][k]
                        flag_r[j][k] = flag_r[j][k]/committed_agents[j][k]
                    else:
                        flag_r[j][k] = 1
            for j in range(num_options+1):
                for k in range(len(output_quorum[0])):
                    output_agents[j][k] += committed_agents[j][k]
                    output_quorum[j][k] += flag_q[j][k]
                    output_paramR[j][k] += flag_r[j][k]
        for i in range(num_options+1):
            for j in range(len(output_quorum[0])):
                output_agents[i][j] = np.round(output_agents[i][j]/(len(commits)*num_agents),3)
                output_quorum[i][j] = np.round(output_quorum[i][j]/len(commits),3)
                output_paramR[i][j] = np.round(output_paramR[i][j]/len(commits),3)
        return output_agents,output_quorum,output_paramR

##########################################################################################################
    def dump_msgs(self,base,file_name,data):
        header = ["max_steps", "rec_time", "rebroadcast", "n_agents", "n_options", "model", "r_type", "r_value", "eta_value", "min_list_quorum", "msg_timeout", "msg_x_step", "msg_hops", "data"]
        output_file = base.replace("results_raw","results_processed")+'/'+file_name
        write_header = not os.path.exists(output_file)        
        with open(output_file, mode='a+', newline='\n') as fw:
            fwriter = csv.writer(fw, delimiter='\t')
            if write_header:
                fwriter.writerow(header)
            for i in range(len(data)):
                if data[i]==None:
                    data[i]='-'
            fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],list(data[13])])
        return
    
##########################################################################################################
    def dump_median_time(self,base,file_name,data):
        header = ["max_steps", "rec_time","rebroadcast", "n_agents", "n_options", "model", "r_type", "r_value", "eta_value", "min_list_quorum", "msg_timeout", "msg_x_step", "msg_hops", "data"]
        output_file = base.replace("results_raw","results_processed")+'/'+file_name
        write_header = not os.path.exists(output_file)        
        with open(output_file, mode='a+', newline='\n') as fw:
            fwriter = csv.writer(fw, delimiter='\t')
            if write_header:
                fwriter.writerow(header)
            for i in range(len(data)):
                if data[i]==None:
                    data[i]='-'
            fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13]])
        return
    
##########################################################################################################
    def dump_residence(self,base,file_name,data):
        header = ["max_steps", "rec_time", "rebroadcast", "n_agents", "n_options", "model", "r_type", "r_value", "eta_value", "min_list_quorum", "msg_timeout", "msg_x_step", "msg_hops", "option_id", "data"]
        output_file = base.replace("results_raw","results_processed")+'/'+file_name
        write_header = not os.path.exists(output_file)        
        with open(output_file, mode='a+', newline='\n') as fw:
            fwriter = csv.writer(fw, delimiter='\t')
            if write_header:
                fwriter.writerow(header)
            for i in range(len(data)-1):
                if data[i]==None:
                    data[i]='-'
            for i in range(len(data[13])):
                if i == len(data[13]) - 1:
                    fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],-1,list(data[13][i])])
                else:
                    fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],i,list(data[13][i])])
        return
    
##########################################################################################################
    def dump_quorum(self,base,file_name,data):
        header = ["max_steps", "rec_time", "rebroadcast", "n_agents", "n_options", "model", "r_type", "r_value", "eta_value", "min_list_quorum", "msg_timeout", "msg_x_step", "msg_hops", "option_id", "data"]
        output_file = base.replace("results_raw","results_processed")+'/'+file_name
        write_header = not os.path.exists(output_file)        
        with open(output_file, mode='a+', newline='\n') as fw:
            fwriter = csv.writer(fw, delimiter='\t')
            if write_header:
                fwriter.writerow(header)
            for i in range(len(data)-1):
                if data[i]==None:
                    data[i]='-'
            for i in range(len(data[13])):
                if i == len(data[13]) - 1:
                    fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],-1,list(data[13][i])])
                else:
                    fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],i,list(data[13][i])])
        return
    
##########################################################################################################
    def dump_control_parameter(self,base,file_name,data):
        header = ["max_steps", "rec_time", "rebroadcast", "n_agents", "n_options", "model", "r_type", "r_value", "eta_value", "min_list_quorum", "msg_timeout", "msg_x_step", "msg_hops", "option_id", "data"]
        output_file = base.replace("results_raw","results_processed")+'/'+file_name
        write_header = not os.path.exists(output_file)        
        with open(output_file, mode='a+', newline='\n') as fw:
            fwriter = csv.writer(fw, delimiter='\t')
            if write_header:
                fwriter.writerow(header)
            for i in range(len(data)-1):
                if data[i]==None:
                    data[i]='-'
            for i in range(len(data[13])):
                if i == len(data[13]) - 1:
                    fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],-1,list(data[13][i])])
                else:
                    fwriter.writerow([data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],i,list(data[13][i])])
        return
    