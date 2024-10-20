import numpy as np
import os, csv
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.lines as mlines
class Data:

##########################################################################################################
    def __init__(self) -> None:
        plt.rcParams.update({"font.size":36})
        self.cm             = plt.get_cmap('viridis') 
        self.typo           = [0,1,2,3,4,5,6,7,8,9,10]
        self.cNorm          = colors.Normalize(vmin=self.typo[0], vmax=self.typo[-1])
        self.scalarMap      = cmx.ScalarMappable(norm=self.cNorm, cmap=self.cm)
        self.input_folders  = []
        self.output_folders = []
        self.base = os.path.abspath("")
        for elem in sorted(os.listdir(self.base)):
            if '.' not in elem and ("results_processed") in elem:
                self.input_folders.append(os.path.join(self.base, elem))
        for i in range(len(self.input_folders)):
            self.output_folders.append(self.input_folders[i] + "/images")
            if not os.path.exists(self.output_folders[i]):
                os.mkdir(self.output_folders[i])

##########################################################################################################
    def read_csv_file(self,file_path):
        lc              = 0
        output          = {}
        steps           = []
        rec_time        = []
        communication   = []
        n_agents        = []
        n_options       = []
        model           = []
        r_type          = []
        r_value         = []
        eta_value       = []
        mlq             = []
        mt              = []
        ms              = []
        mh              = []
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if lc == 0:
                    lc = 1
                else:
                    for val in row:
                        vals = val.split('\t')
                        output.update({(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7],vals[8],vals[9],vals[10],vals[11],vals[12]):vals[13]})        
                        if vals[0] not in steps: steps.append(vals[0])
                        if vals[1] not in rec_time: rec_time.append(vals[1])
                        if vals[2] not in communication: communication.append(vals[2])
                        if vals[3] not in n_agents: n_agents.append(vals[3])
                        if vals[4] not in n_options: n_options.append(vals[4])
                        if vals[5] not in model: model.append(vals[5])
                        if vals[6] not in r_type: r_type.append(vals[6])
                        if vals[7] not in r_value: r_value.append(vals[7])
                        if vals[8] not in eta_value: eta_value.append(vals[8])
                        if vals[9] not in mlq: mlq.append(vals[9])
                        if vals[10] not in mt: mt.append(vals[10])
                        if vals[11] not in ms: ms.append(vals[11])
                        if vals[12] not in mh: mh.append(vals[12])
        return output,(steps,rec_time,communication,n_agents,n_options,model,r_type,r_value,eta_value,mlq,mt,ms,mh)
    
##########################################################################################################
    def read_csv_array_data(self,file_path,opt = True):
        lc              = 0
        output          = {}
        steps           = []
        rec_time        = []
        communication   = []
        n_agents        = []
        n_options       = []
        model           = []
        r_type          = []
        r_value         = []
        eta_value       = []
        mlq             = []
        mt              = []
        ms              = []
        mh              = []
        option_id       = []
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if lc == 0:
                    lc = 1
                else:
                    keys = []
                    array_val = []
                    for val in row:
                        split_val = val.split('\t')
                        if len(split_val)==1:
                            tval = val  
                            if ']' in val:
                                tval = ''
                                for c in val:
                                    if c != ']':
                                        tval+=c
                            array_val.append(float(tval))
                            if ']' in val:
                                if opt:
                                    if keys[0] not in steps: steps.append(keys[0])
                                    if keys[1] not in rec_time: rec_time.append(keys[1])
                                    if keys[2] not in communication: communication.append(keys[2])
                                    if keys[3] not in n_agents: n_agents.append(keys[3])
                                    if keys[4] not in n_options: n_options.append(keys[4])
                                    if keys[5] not in model: model.append(keys[5])
                                    if keys[6] not in r_type: r_type.append(keys[6])
                                    if keys[7] not in r_value: r_value.append(keys[7])
                                    if keys[8] not in eta_value: eta_value.append(keys[8])
                                    if keys[9] not in mlq: mlq.append(keys[9])
                                    if keys[10] not in mt: mt.append(keys[10])
                                    if keys[11] not in ms: ms.append(keys[11])
                                    if keys[12] not in mh: mh.append(keys[12])
                                    if keys[13] not in option_id: option_id.append(keys[13])
                                    output.update({(keys[0],keys[1],keys[2],keys[3],keys[4],keys[5],keys[6],keys[7],keys[8],keys[9],keys[10],keys[11],keys[12],keys[13]):array_val})
                                else:                                    
                                    if keys[0] not in steps: steps.append(keys[0])
                                    if keys[1] not in rec_time: rec_time.append(keys[1])
                                    if keys[2] not in communication: communication.append(keys[2])
                                    if keys[3] not in n_agents: n_agents.append(keys[3])
                                    if keys[4] not in n_options: n_options.append(keys[4])
                                    if keys[5] not in model: model.append(keys[5])
                                    if keys[6] not in r_type: r_type.append(keys[6])
                                    if keys[7] not in r_value: r_value.append(keys[7])
                                    if keys[8] not in eta_value: eta_value.append(keys[8])
                                    if keys[9] not in mlq: mlq.append(keys[9])
                                    if keys[10] not in mt: mt.append(keys[10])
                                    if keys[11] not in ms: ms.append(keys[11])
                                    if keys[12] not in mh: mh.append(keys[12])
                                    output.update({(keys[0],keys[1],keys[2],keys[3],keys[4],keys[5],keys[6],keys[7],keys[8],keys[9],keys[10],keys[11],keys[12]):array_val})
                        else:
                            for col in range(len(split_val)):
                                tval = split_val[col]
                                if '[' in split_val[col]:
                                    tval = ''
                                    for c in split_val[col]:
                                        if c != '[':
                                            tval+=c
                                    array_val.append(float(tval))
                                else:
                                    keys.append(tval)
        if len(option_id)>0:
            return output,(steps,rec_time,communication,n_agents,n_options,model,r_type,r_value,eta_value,mlq,mt,ms,mh,option_id)
        return output,(steps,rec_time,communication,n_agents,n_options,model,r_type,r_value,eta_value,mlq,mt,ms,mh)
    
##########################################################################################################
    def sort_dict(self,data,keys):
        steps           = keys[0]
        rec_time        = keys[1]
        communication   = keys[2]
        n_agents        = keys[3]
        n_options       = keys[4]
        model           = keys[5]
        r_type          = keys[6]
        r_value         = keys[7]
        eta_value       = keys[8]
        mlq             = keys[9]
        mtmt            = keys[10]
        mxs             = keys[11]
        mhps            = keys[12]
        option_id       = []
        if len(keys) == 14: option_id = keys[13]
        dict_r = {}
        for r in r_type:
            dict_com = {}
            for c in communication:
                hops_dict = {}
                for mh in mhps:
                    dict_flag={}
                    for s in steps:
                        for rt in rec_time:
                            for a in n_agents:
                                for o in n_options:
                                    for m in model:
                                        for rv in r_value:
                                            for ev in eta_value:
                                                for mq in mlq:
                                                    for mt in mtmt:
                                                        for ms in mxs:
                                                            if len(option_id) > 0:
                                                                for oid in option_id:
                                                                    if data.get((s,rt,c,a,o,m,r,rv,ev,mq,mt,ms,mh,oid)) != None:
                                                                        dict_flag.update({(s,rt,a,o,m,rv,ev,mq,mt,ms,oid):data.get((s,rt,c,a,o,m,r,rv,ev,mq,mt,ms,mh,oid))})
                                                            else:
                                                                if data.get((s,rt,c,a,o,m,r,rv,ev,mq,mt,ms,mh)) != None:
                                                                    dict_flag.update({(s,rt,a,o,m,rv,ev,mq,mt,ms):data.get((s,rt,c,a,o,m,r,rv,ev,mq,mt,ms,mh))})
                    hops_dict.update({mh:dict_flag})
                dict_com.update({c:hops_dict})
            dict_r.update({r:dict_com})
        return dict_r

##########################################################################################################
    def plot_messages(self,data_dict,keys,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        opts_2          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[0]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='2')
        opts_3          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[3]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='3')
        opts_5          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[6]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='5')
        voter           = mlines.Line2D([], [], color="black", marker='None', linestyle='-', linewidth=10, label='Voter')
        majority        = mlines.Line2D([], [], color="black", marker='None', linestyle='--', linewidth=10, label='Majority')
        handles_r       = [opts_2,opts_3,opts_5,voter,majority]
        steps           = keys[0]
        rec_time        = keys[1]
        n_agents        = keys[3]
        n_options       = keys[4]
        model           = keys[5]
        r_value         = keys[7]
        eta_value       = keys[8]
        mlq             = keys[9]
        mtmt            = keys[10]
        mxs             = keys[11]
        svoid_x_ticks   = []
        void_x_ticks    = []
        void_y_ticks    = []
        real_x_ticks    = []
        for r in data_dict.keys():
            com_dict = data_dict.get(r)
            for c in com_dict.keys():
                hops_dict = com_dict.get(c)
                for mh in hops_dict.keys():
                    dictionary = hops_dict.get(mh)
                    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(36,10))
                    save_fig = False
                    col = 0
                    ls  = "-"
                    lc  = self.scalarMap.to_rgba(self.typo[0])
                    for s in steps:
                        for rt in rec_time:
                            x_lim = int(s)//int(rt)
                            for mq in mlq:
                                for mt in mtmt:
                                    for ms in mxs:
                                        for a in n_agents:
                                            for m in model:
                                                for o in n_options:
                                                    for rv in r_value:
                                                        for ev in eta_value:
                                                            if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms)) != None:
                                                                save_fig = True
                                                                vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms))
                                                                for i in range(len(vals)): vals[i] = vals[i]/(int(a)-1)
                                                                if ev == "0.2":
                                                                    col = 0
                                                                elif ev == "0.4":
                                                                    col = 1
                                                                elif ev == "0.6":
                                                                    col = 2
                                                                elif ev == "0.8":
                                                                    col = 3
                                                                if o == "2":
                                                                    lc = self.scalarMap.to_rgba(self.typo[0])
                                                                elif o == "3":
                                                                    lc = self.scalarMap.to_rgba(self.typo[3])
                                                                elif o == "5":
                                                                    lc = self.scalarMap.to_rgba(self.typo[6])
                                                                if m == "voter":
                                                                    ls = "-"
                                                                elif m == "majority":
                                                                    ls = "--"
                                                                ax[col].plot(vals,color=lc,linestyle=ls,lw=6)
                                                                ax[col].set_xlim(0,x_lim+1)
                                                                ax[col].set_ylim(0,1)
                                                                if len(real_x_ticks)==0:
                                                                    for x in range(0,x_lim+1,50):
                                                                        if x%150 == 0:
                                                                            svoid_x_ticks.append('')
                                                                            void_x_ticks.append('')
                                                                            real_x_ticks.append(str(int(np.round(x,0))))
                                                                        else:
                                                                            void_x_ticks.append('')
                                                                    for y in range(0,11,1):
                                                                        void_y_ticks.append('')
                                                                ax[col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                ax[col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                axt = ax[col].twiny()
                                                                labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                empty_string_labels = ['']*len(labels)
                                                                axt.set_xticklabels(empty_string_labels)
                                                                ax[col].set_xlabel(r"$T\,  s$")
                                                                if col==0:
                                                                    ax[col].set_yticks(np.arange(0,1.01,.1))
                                                                    ax[col].set_ylabel("M")
                                                                    axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                elif col==1:
                                                                    ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                    axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                elif col==2:
                                                                    ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                    axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                elif col==3:
                                                                    ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                    axt.set_xlabel(r"$\eta = 0.8\,  s$")
                    for cl in range(4):
                        ax[cl].grid(which='major')                                                                
                    fig.tight_layout()
                    fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                    fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_messages.pdf"
                    if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                    plt.close(fig)
        return
    
##########################################################################################################
    def plot_times(self,data_dict,keys,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        opts_2          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[0]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='2')
        opts_3          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[3]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='3')
        opts_5          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[6]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='5')
        voter           = mlines.Line2D([], [], color="black", marker='None', linestyle='-', linewidth=10, label='Voter')
        majority        = mlines.Line2D([], [], color="black", marker='None', linestyle='--', linewidth=10, label='Majority')
        handles_r       = [opts_2,opts_3,opts_5,voter,majority]
        steps           = keys[0]
        rec_time        = keys[1]
        n_agents        = keys[3]
        n_options       = keys[4]
        model           = keys[5]
        r_value         = keys[7]
        eta_value       = keys[8]
        mlq             = keys[9]
        mtmt            = keys[10]
        mxs             = keys[11]
        real_y_ticks    = []
        void_y_ticks    = []
        svoid_y_ticks   = []
        void_x_ticks    = []
        for r in data_dict.keys():
            com_dict = data_dict.get(r)
            for c in com_dict.keys():
                hops_dict = com_dict.get(c)
                for mh in hops_dict.keys():
                    dictionary = hops_dict.get(mh)
                    fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(36,20))
                    save_fig = False
                    col = 0
                    row = 0
                    lc  = self.scalarMap.to_rgba(self.typo[0])
                    for s in steps:
                        for rt in rec_time:
                            x_lim = int(s)//int(rt)
                            for mq in mlq:
                                for mt in mtmt:
                                    for ms in mxs:
                                        for a in n_agents:
                                            for m in model:
                                                for o in n_options:
                                                    for rv in r_value:
                                                        for ev in eta_value:
                                                            if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms)) != None:
                                                                save_fig = True
                                                                vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms))
                                                                if rv == "0.2":
                                                                    row = 0
                                                                elif rv == "0.4":
                                                                    row = 1
                                                                elif rv == "0.6":
                                                                    row = 2
                                                                elif rv == "0.8":
                                                                    row = 3
                                                                if ev == "0.2":
                                                                    col = 0
                                                                elif ev == "0.4":
                                                                    col = 1
                                                                elif ev == "0.6":
                                                                    col = 2
                                                                elif ev == "0.8":
                                                                    col = 3
                                                                if o == "2":
                                                                    lc = self.scalarMap.to_rgba(self.typo[0])
                                                                elif o == "3":
                                                                    lc = self.scalarMap.to_rgba(self.typo[3])
                                                                elif o == "5":
                                                                    lc = self.scalarMap.to_rgba(self.typo[6])
                                                                if m == "voter":
                                                                    ls = "-"
                                                                elif m == "majority":
                                                                    ls = "--"
                                                                ax[row][col].bar(vals,color=lc,linestyle=ls,lw=6)
                                                                ax[row][col].set_ylim(0,x_lim+1)
                                                                if len(real_y_ticks)==0:
                                                                    for x in range(0,x_lim+1,50):
                                                                        if x%150 == 0:
                                                                            svoid_y_ticks.append('')
                                                                            void_y_ticks.append('')
                                                                            real_y_ticks.append(str(int(np.round(x,0))))
                                                                        else:
                                                                            void_y_ticks.append('')
                                                                if row == 0:
                                                                    # ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_x_ticks)
                                                                    # ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                    axt = ax[row][col].twiny()
                                                                    labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                    empty_string_labels = ['']*len(labels)
                                                                    axt.set_xticklabels(empty_string_labels)
                                                                    if col==0:
                                                                        axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                    elif col==1:
                                                                        axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                    elif col==2:
                                                                        axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                    elif col==3:
                                                                        axt.set_xlabel(r"$\eta = 0.8\,  s$")
                                                                elif row==3:
                                                                    # ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                    # ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                    ax[row][col].set_xlabel(r"$T\,  s$")
                                                                # else:
                                                                #     ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_x_ticks)
                                                                #     ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                if col==0:
                                                                    ax[row][col].set_yticks(np.arange(0,x_lim+1,150),labels=real_y_ticks)
                                                                    ax[row][col].set_yticks(np.arange(0,x_lim+1,50),labels=void_y_ticks,minor=True)
                                                                    ax[row][col].set_ylabel("M")
                                                                elif col==3:
                                                                    ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_y_ticks)
                                                                    ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_y_ticks,minor=True)
                                                                    axt = ax[row][col].twinx()
                                                                    labels = [item.get_text() for item in axt.get_yticklabels()]
                                                                    empty_string_labels = ['']*len(labels)
                                                                    axt.set_yticklabels(empty_string_labels)
                                                                    if row==0:
                                                                        axt.set_ylabel(r"$R = 0.2\,  s$")
                                                                    elif row==1:
                                                                        axt.set_ylabel(r"$R = 0.4\,  s$")
                                                                    elif row==2:
                                                                        axt.set_ylabel(r"$R = 0.6\,  s$")
                                                                    elif row==3:
                                                                        axt.set_ylabel(r"$R = 0.8\,  s$")
                                                                else:
                                                                    ax[row][col].set_yticks(np.arange(0,x_lim+1,50),labels=void_y_ticks)
                    for rw in range(4):
                        for cl in range(4):
                            ax[rw][cl].grid(which='major')                                                                     
                    fig.tight_layout()
                    fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                    fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_times.pdf"
                    if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                    plt.close(fig)
        return
    
##########################################################################################################
    def plot_residence(self,data_dict,keys,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        best            = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[0]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='best')
        others          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[3]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='others')
        no_opt          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[6]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='no_opt')
        voter           = mlines.Line2D([], [], color="black", marker='None', linestyle='-', linewidth=10, label='Voter')
        majority        = mlines.Line2D([], [], color="black", marker='None', linestyle='--', linewidth=10, label='Majority')
        handles_r       = [best,others,no_opt,voter,majority]
        steps           = keys[0]
        rec_time        = keys[1]
        n_agents        = keys[3]
        n_options       = keys[4]
        model           = keys[5]
        r_value         = keys[7]
        eta_value       = keys[8]
        mlq             = keys[9]
        mtmt            = keys[10]
        mxs             = keys[11]
        option_id       = keys[13]
        svoid_x_ticks   = []
        void_x_ticks    = []
        void_y_ticks    = []
        real_x_ticks    = []
        for r in data_dict.keys():
            com_dict = data_dict.get(r)
            for c in com_dict.keys():
                hops_dict = com_dict.get(c)
                for mh in hops_dict.keys():
                    dictionary = hops_dict.get(mh)
                    for o in n_options:
                        if r == "static":
                            fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(36,20))
                            save_fig = False
                            col = 0
                            row = 0
                            ls  = "-"
                            lc  = self.scalarMap.to_rgba(self.typo[0])
                            for s in steps:
                                for rt in rec_time:
                                    x_lim = int(s)//int(rt)
                                    for mq in mlq:
                                        for mt in mtmt:
                                            for ms in mxs:
                                                for a in n_agents:
                                                    for m in model:
                                                        for rv in r_value:
                                                            for ev in eta_value:
                                                                for oid in option_id:
                                                                    if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid)) != None:
                                                                        save_fig = True
                                                                        vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid))
                                                                        if rv == "0.2":
                                                                            row = 0
                                                                        elif rv == "0.4":
                                                                            row = 1
                                                                        elif rv == "0.6":
                                                                            row = 2
                                                                        elif rv == "0.8":
                                                                            row = 3
                                                                        if ev == "0.2":
                                                                            col = 0
                                                                        elif ev == "0.4":
                                                                            col = 1
                                                                        elif ev == "0.6":
                                                                            col = 2
                                                                        elif ev == "0.8":
                                                                            col = 3
                                                                        if oid == "0":
                                                                            lc = self.scalarMap.to_rgba(self.typo[0])
                                                                        elif oid == "-1":
                                                                            lc = self.scalarMap.to_rgba(self.typo[6])
                                                                        else:
                                                                            lc = self.scalarMap.to_rgba(self.typo[3])
                                                                        if m == "voter":
                                                                            ls = "-"
                                                                        elif m == "majority":
                                                                            ls = "--"
                                                                        ax[row][col].plot(vals,color=lc,linestyle=ls,lw=6)
                                                                        ax[row][col].set_xlim(0,x_lim+1)
                                                                        ax[row][col].set_ylim(0,1)
                                                                        if len(real_x_ticks)==0:
                                                                            for x in range(0,x_lim+1,50):
                                                                                if x%150 == 0:
                                                                                    svoid_x_ticks.append('')
                                                                                    void_x_ticks.append('')
                                                                                    real_x_ticks.append(str(int(np.round(x,0))))
                                                                                else:
                                                                                    void_x_ticks.append('')
                                                                            for y in range(0,11,1):
                                                                                void_y_ticks.append('')
                                                                        if row == 0:
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_x_ticks)
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                            axt = ax[row][col].twiny()
                                                                            labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                            empty_string_labels = ['']*len(labels)
                                                                            axt.set_xticklabels(empty_string_labels)
                                                                            if col==0:
                                                                                axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                            elif col==1:
                                                                                axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                            elif col==2:
                                                                                axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                            elif col==3:
                                                                                axt.set_xlabel(r"$\eta = 0.8\,  s$")
                                                                        elif row==3:
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                            ax[row][col].set_xlabel(r"$T\,  s$")
                                                                        else:
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_x_ticks)
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                        if col==0:
                                                                            ax[row][col].set_yticks(np.arange(0,1.01,.1))
                                                                            ax[row][col].set_ylabel("A")
                                                                        elif col==3:
                                                                            ax[row][col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                            axt = ax[row][col].twinx()
                                                                            labels = [item.get_text() for item in axt.get_yticklabels()]
                                                                            empty_string_labels = ['']*len(labels)
                                                                            axt.set_yticklabels(empty_string_labels)
                                                                            if row==0:
                                                                                axt.set_ylabel(r"$R = 0.2\,  s$")
                                                                            elif row==1:
                                                                                axt.set_ylabel(r"$R = 0.4\,  s$")
                                                                            elif row==2:
                                                                                axt.set_ylabel(r"$R = 0.6\,  s$")
                                                                            elif row==3:
                                                                                axt.set_ylabel(r"$R = 0.8\,  s$")
                                                                        else:
                                                                            ax[row][col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                            for rw in range(4):
                                for cl in range(4):
                                    ax[rw][cl].grid(which='major') 
                            fig.tight_layout()
                            fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                            fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_o#"+str(o)+"_residence.pdf"
                            if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                            plt.close(fig)
                        else:
                            fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(36,20))
                            save_fig = False
                            col = 0
                            ls  = "-"
                            lc  = self.scalarMap.to_rgba(self.typo[0])
                            for s in steps:
                                for rt in rec_time:
                                    x_lim = int(s)//int(rt)
                                    for mq in mlq:
                                        for mt in mtmt:
                                            for ms in mxs:
                                                for a in n_agents:
                                                    for m in model:
                                                        for rv in r_value:
                                                            for ev in eta_value:
                                                                for oid in option_id:
                                                                    if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid)) != None:
                                                                        save_fig = True
                                                                        vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid))
                                                                        if ev == "0.2":
                                                                            col = 0
                                                                        elif ev == "0.4":
                                                                            col = 1
                                                                        elif ev == "0.6":
                                                                            col = 2
                                                                        elif ev == "0.8":
                                                                            col = 3
                                                                        if oid == "0":
                                                                            lc = self.scalarMap.to_rgba(self.typo[0])
                                                                        elif oid == "-1":
                                                                            lc = self.scalarMap.to_rgba(self.typo[6])
                                                                        else:
                                                                            lc = self.scalarMap.to_rgba(self.typo[3])
                                                                        if m == "voter":
                                                                            ls = "-"
                                                                        elif m == "majority":
                                                                            ls = "--"
                                                                        ax[col].plot(vals,color=lc,linestyle=ls,lw=6)
                                                                        ax[col].set_xlim(0,x_lim+1)
                                                                        ax[col].set_ylim(0,1)
                                                                        if len(real_x_ticks)==0:
                                                                            for x in range(0,x_lim+1,50):
                                                                                if x%150 == 0:
                                                                                    svoid_x_ticks.append('')
                                                                                    void_x_ticks.append('')
                                                                                    real_x_ticks.append(str(int(np.round(x,0))))
                                                                                else:
                                                                                    void_x_ticks.append('')
                                                                            for y in range(0,11,1):
                                                                                void_y_ticks.append('')
                                                                        ax[col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                        ax[col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                        ax[col].set_xlabel(r"$T\,  s$")
                                                                        axt = ax[col].twiny()
                                                                        labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                        empty_string_labels = ['']*len(labels)
                                                                        axt.set_xticklabels(empty_string_labels)
                                                                        if col==0:
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1))
                                                                            ax[col].set_ylabel("A")
                                                                            axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                        elif col==1:
                                                                            axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                        elif col==2:
                                                                            axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                        elif col==3:
                                                                            axt.set_xlabel(r"$\eta = 0.8\,  s$")
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                            axt = ax[col].twinx()
                                                                            labels = [item.get_text() for item in axt.get_yticklabels()]
                                                                            empty_string_labels = ['']*len(labels)
                                                                            axt.set_yticklabels(empty_string_labels)
                            for cl in range(4):
                                ax[cl].grid(which='major') 
                            fig.tight_layout()
                            fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                            fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_o#"+str(o)+"_residence.pdf"
                            if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                            plt.close(fig)
        return
    
##########################################################################################################
    def plot_quorum(self,data_dict,keys,output_dir):        
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        best            = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[0]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='best')
        others          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[3]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='others')
        no_opt          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[6]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='no_opt')
        voter           = mlines.Line2D([], [], color="black", marker='None', linestyle='-', linewidth=10, label='Voter')
        majority        = mlines.Line2D([], [], color="black", marker='None', linestyle='--', linewidth=10, label='Majority')
        handles_r       = [best,others,no_opt,voter,majority]
        steps           = keys[0]
        rec_time        = keys[1]
        n_agents        = keys[3]
        n_options       = keys[4]
        model           = keys[5]
        r_value         = keys[7]
        eta_value       = keys[8]
        mlq             = keys[9]
        mtmt            = keys[10]
        mxs             = keys[11]
        option_id       = keys[13]
        svoid_x_ticks   = []
        void_x_ticks    = []
        void_y_ticks    = []
        real_x_ticks    = []
        for r in data_dict.keys():
            com_dict = data_dict.get(r)
            for c in com_dict.keys():
                hops_dict = com_dict.get(c)
                for mh in hops_dict.keys():
                    dictionary = hops_dict.get(mh)
                    for o in n_options:
                        if r == "static":
                            fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(36,20))
                            save_fig = False
                            col = 0
                            row = 0
                            ls  = "-"
                            lc  = self.scalarMap.to_rgba(self.typo[0])
                            for s in steps:
                                for rt in rec_time:
                                    x_lim = int(s)//int(rt)
                                    for mq in mlq:
                                        for mt in mtmt:
                                            for ms in mxs:
                                                for a in n_agents:
                                                    for m in model:
                                                        for rv in r_value:
                                                            for ev in eta_value:
                                                                for oid in option_id:
                                                                    if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid)) != None:
                                                                        save_fig = True
                                                                        vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid))
                                                                        if rv == "0.2":
                                                                            row = 0
                                                                        elif rv == "0.4":
                                                                            row = 1
                                                                        elif rv == "0.6":
                                                                            row = 2
                                                                        elif rv == "0.8":
                                                                            row = 3
                                                                        if ev == "0.2":
                                                                            col = 0
                                                                        elif ev == "0.4":
                                                                            col = 1
                                                                        elif ev == "0.6":
                                                                            col = 2
                                                                        elif ev == "0.8":
                                                                            col = 3
                                                                        if oid == "0":
                                                                            lc = self.scalarMap.to_rgba(self.typo[0])
                                                                        elif oid == "-1":
                                                                            lc = self.scalarMap.to_rgba(self.typo[6])
                                                                        else:
                                                                            lc = self.scalarMap.to_rgba(self.typo[3])
                                                                        if m == "voter":
                                                                            ls = "-"
                                                                        elif m == "majority":
                                                                            ls = "--"
                                                                        ax[row][col].plot(vals,color=lc,linestyle=ls,lw=6)
                                                                        ax[row][col].set_xlim(0,x_lim+1)
                                                                        ax[row][col].set_ylim(0,1)
                                                                        if len(real_x_ticks)==0:
                                                                            for x in range(0,x_lim+1,50):
                                                                                if x%150 == 0:
                                                                                    svoid_x_ticks.append('')
                                                                                    void_x_ticks.append('')
                                                                                    real_x_ticks.append(str(int(np.round(x,0))))
                                                                                else:
                                                                                    void_x_ticks.append('')
                                                                            for y in range(0,11,1):
                                                                                void_y_ticks.append('')
                                                                        if row == 0:
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_x_ticks)
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                            axt = ax[row][col].twiny()
                                                                            labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                            empty_string_labels = ['']*len(labels)
                                                                            axt.set_xticklabels(empty_string_labels)
                                                                            if col==0:
                                                                                axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                            elif col==1:
                                                                                axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                            elif col==2:
                                                                                axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                            elif col==3:
                                                                                axt.set_xlabel(r"$\eta = 0.8\,  s$")
                                                                        elif row==3:
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                            ax[row][col].set_xlabel(r"$T\,  s$")
                                                                        else:
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,150),labels=svoid_x_ticks)
                                                                            ax[row][col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                        if col==0:
                                                                            ax[row][col].set_yticks(np.arange(0,1.01,.1))
                                                                            ax[row][col].set_ylabel("Q")
                                                                        elif col==3:
                                                                            ax[row][col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                            axt = ax[row][col].twinx()
                                                                            labels = [item.get_text() for item in axt.get_yticklabels()]
                                                                            empty_string_labels = ['']*len(labels)
                                                                            axt.set_yticklabels(empty_string_labels)
                                                                            if row==0:
                                                                                axt.set_ylabel(r"$R = 0.2\,  s$")
                                                                            elif row==1:
                                                                                axt.set_ylabel(r"$R = 0.4\,  s$")
                                                                            elif row==2:
                                                                                axt.set_ylabel(r"$R = 0.6\,  s$")
                                                                            elif row==3:
                                                                                axt.set_ylabel(r"$R = 0.8\,  s$")
                                                                        else:
                                                                            ax[row][col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                            for rw in range(4):
                                for cl in range(4):
                                    ax[rw][cl].grid(which='major')                
                            fig.tight_layout()
                            fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                            fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_o#"+str(o)+"_quorum.pdf"
                            if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                            plt.close(fig)
                        else:
                            fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(36,20))
                            save_fig = False
                            col = 0
                            ls  = "-"
                            lc  = self.scalarMap.to_rgba(self.typo[0])
                            for s in steps:
                                for rt in rec_time:
                                    x_lim = int(s)//int(rt)
                                    for mq in mlq:
                                        for mt in mtmt:
                                            for ms in mxs:
                                                for a in n_agents:
                                                    for m in model:
                                                        for rv in r_value:
                                                            for ev in eta_value:
                                                                for oid in option_id:
                                                                    if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid)) != None:
                                                                        save_fig = True
                                                                        vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid))
                                                                        if ev == "0.2":
                                                                            col = 0
                                                                        elif ev == "0.4":
                                                                            col = 1
                                                                        elif ev == "0.6":
                                                                            col = 2
                                                                        elif ev == "0.8":
                                                                            col = 3
                                                                        if oid == "0":
                                                                            lc = self.scalarMap.to_rgba(self.typo[0])
                                                                        elif oid == "-1":
                                                                            lc = self.scalarMap.to_rgba(self.typo[6])
                                                                        else:
                                                                            lc = self.scalarMap.to_rgba(self.typo[3])
                                                                        if m == "voter":
                                                                            ls = "-"
                                                                        elif m == "majority":
                                                                            ls = "--"
                                                                        ax[col].plot(vals,color=lc,linestyle=ls,lw=6)
                                                                        ax[col].set_xlim(0,x_lim+1)
                                                                        ax[col].set_ylim(0,1)
                                                                        if len(real_x_ticks)==0:
                                                                            for x in range(0,x_lim+1,50):
                                                                                if x%150 == 0:
                                                                                    svoid_x_ticks.append('')
                                                                                    void_x_ticks.append('')
                                                                                    real_x_ticks.append(str(int(np.round(x,0))))
                                                                                else:
                                                                                    void_x_ticks.append('')
                                                                            for y in range(0,11,1):
                                                                                void_y_ticks.append('')
                                                                        ax[col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                        ax[col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                        ax[col].set_xlabel(r"$T\,  s$")
                                                                        axt = ax[col].twiny()
                                                                        labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                        empty_string_labels = ['']*len(labels)
                                                                        axt.set_xticklabels(empty_string_labels)
                                                                        if col==0:
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1))
                                                                            ax[col].set_ylabel("Q")
                                                                            axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                        elif col==1:
                                                                            axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                        elif col==2:
                                                                            axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                        elif col==3:
                                                                            axt.set_xlabel(r"$\eta = 0.8\,  s$")
                                                                            ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                            axt = ax[col].twinx()
                                                                            labels = [item.get_text() for item in axt.get_yticklabels()]
                                                                            empty_string_labels = ['']*len(labels)
                                                                            axt.set_yticklabels(empty_string_labels)
                            for cl in range(4):
                                ax[cl].grid(which='major') 
                            fig.tight_layout()
                            fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                            fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_o#"+str(o)+"_quorum.pdf"
                            if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                            plt.close(fig)
        return
    
##########################################################################################################
    def plot_controlParameter(self,data_dict,keys,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        best            = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[0]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='best')
        others          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[3]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='others')
        no_opt          = mlines.Line2D([], [], color=self.scalarMap.to_rgba(self.typo[6]), marker='_', linestyle='None', markeredgewidth=18, markersize=18, label='no_opt')
        voter           = mlines.Line2D([], [], color="black", marker='None', linestyle='-', linewidth=10, label='Voter')
        majority        = mlines.Line2D([], [], color="black", marker='None', linestyle='--', linewidth=10, label='Majority')
        handles_r       = [best,others,no_opt,voter,majority]
        steps           = keys[0]
        rec_time        = keys[1]
        n_agents        = keys[3]
        n_options       = keys[4]
        model           = keys[5]
        r_value         = keys[7]
        eta_value       = keys[8]
        mlq             = keys[9]
        mtmt            = keys[10]
        mxs             = keys[11]
        option_id       = keys[13]
        svoid_x_ticks   = []
        void_x_ticks    = []
        void_y_ticks    = []
        real_x_ticks    = []
        for r in data_dict.keys():
            com_dict = data_dict.get(r)
            for c in com_dict.keys():
                hops_dict = com_dict.get(c)
                for mh in hops_dict.keys():
                    dictionary = hops_dict.get(mh)
                    for o in n_options:
                        fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(36,20))
                        save_fig = False
                        col = 0
                        ls  = "-"
                        lc  = self.scalarMap.to_rgba(self.typo[0])
                        for s in steps:
                            for rt in rec_time:
                                x_lim = int(s)//int(rt)
                                for mq in mlq:
                                    for mt in mtmt:
                                        for ms in mxs:
                                            for a in n_agents:
                                                for m in model:
                                                    for rv in r_value:
                                                        for ev in eta_value:
                                                            for oid in option_id:
                                                                if dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid)) != None:
                                                                    save_fig = True
                                                                    vals = dictionary.get((s,rt,a,o,m,rv,ev,mq,mt,ms,oid))
                                                                    if ev == "0.2":
                                                                        col = 0
                                                                    elif ev == "0.4":
                                                                        col = 1
                                                                    elif ev == "0.6":
                                                                        col = 2
                                                                    elif ev == "0.8":
                                                                        col = 3
                                                                    if oid == "0":
                                                                        lc = self.scalarMap.to_rgba(self.typo[0])
                                                                    elif oid == "-1":
                                                                        lc = self.scalarMap.to_rgba(self.typo[6])
                                                                    else:
                                                                        lc = self.scalarMap.to_rgba(self.typo[3])
                                                                    if m == "voter":
                                                                        ls = "-"
                                                                    elif m == "majority":
                                                                        ls = "--"
                                                                    ax[col].plot(vals,color=lc,linestyle=ls,lw=6)
                                                                    ax[col].set_xlim(0,x_lim+1)
                                                                    ax[col].set_ylim(0,1)
                                                                    if len(real_x_ticks)==0:
                                                                        for x in range(0,x_lim+1,50):
                                                                            if x%150 == 0:
                                                                                svoid_x_ticks.append('')
                                                                                void_x_ticks.append('')
                                                                                real_x_ticks.append(str(int(np.round(x,0))))
                                                                            else:
                                                                                void_x_ticks.append('')
                                                                        for y in range(0,11,1):
                                                                            void_y_ticks.append('')
                                                                    ax[col].set_xticks(np.arange(0,x_lim+1,150),labels=real_x_ticks)
                                                                    ax[col].set_xticks(np.arange(0,x_lim+1,50),labels=void_x_ticks,minor=True)
                                                                    ax[col].set_xlabel(r"$T\,  s$")
                                                                    axt = ax[col].twiny()
                                                                    labels = [item.get_text() for item in axt.get_xticklabels()]
                                                                    empty_string_labels = ['']*len(labels)
                                                                    axt.set_xticklabels(empty_string_labels)
                                                                    if col==0:
                                                                        ax[col].set_yticks(np.arange(0,1.01,.1))
                                                                        ax[col].set_ylabel("A")
                                                                        axt.set_xlabel(r"$\eta = 0.2\,  s$")
                                                                    elif col==1:
                                                                        axt.set_xlabel(r"$\eta = 0.4\,  s$")
                                                                        ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                    elif col==2:
                                                                        axt.set_xlabel(r"$\eta = 0.6\,  s$")
                                                                        ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                    elif col==3:
                                                                        axt.set_xlabel(r"$\eta = 0.8\,  s$")
                                                                        ax[col].set_yticks(np.arange(0,1.01,.1),labels=void_y_ticks)
                                                                        axt = ax[col].twinx()
                                                                        labels = [item.get_text() for item in axt.get_yticklabels()]
                                                                        empty_string_labels = ['']*len(labels)
                                                                        axt.set_yticklabels(empty_string_labels)
                        for cl in range(4):
                            ax[cl].grid(which='major') 
                        fig.tight_layout()
                        fig.legend(bbox_to_anchor=(1, 0),handles=handles_r,ncols=5,loc="upper right",framealpha=0.7,borderaxespad=0)
                        fig_path = output_dir+"/r#"+str(r)+"_c#"+str(c)+"_h#"+str(mh)+"_o#"+str(o)+"_controlParameter.pdf"
                        if save_fig: fig.savefig(fig_path, bbox_inches="tight")
                        plt.close(fig)
        return