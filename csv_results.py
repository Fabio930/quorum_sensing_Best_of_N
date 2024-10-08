import numpy as np
import os, csv, math
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.lines as mlines
class Data:

##########################################################################################################
    def __init__(self) -> None:
        self.input_folder = ""
        self.base = os.path.abspath("")
        for elem in sorted(os.listdir(self.base)):
            if '.' not in elem and ("results_processed") in elem:
                self.input_folder = os.path.join(self.base, elem)
                break
        self.output_folder = self.input_folder + "/images"
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

##########################################################################################################
    def read_csv_file(self,file_path):
        lc = 0
        output = {}
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if lc == 0:
                    lc = 1
                else:
                    for val in row:
                        vals = val.split('\t')
                        output.update({(vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],vals[7],vals[8],vals[9],vals[10],vals[11],vals[12],vals[13]):vals[14]})
        return output
    
##########################################################################################################
    def read_csv_array_data(self,file_path,opt = True):
        lc = 0
        output = {}
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
                                if opt: output.update({(keys[0],keys[1],keys[2],keys[3],keys[4],keys[5],keys[6],keys[7],keys[8],keys[9],keys[10],keys[11],keys[12],keys[13],keys[14]):array_val})
                                else: output.update({(keys[0],keys[1],keys[2],keys[3],keys[4],keys[5],keys[6],keys[7],keys[8],keys[9],keys[10],keys[11],keys[12],keys[13]):array_val})
                        else:
                            for k in range(len(split_val)):
                                tval = split_val[k]
                                if '[' in split_val[k]:
                                    tval = ''
                                    for c in split_val[k]:
                                        if c != '[':
                                            tval+=c
                                    array_val.append(float(tval))
                                else:
                                    keys.append(tval)
        return output
    
##########################################################################################################
    def plot_messages(self,data_dict,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        return
    
##########################################################################################################
    def plot_times(self,data_dict,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        return
    
##########################################################################################################
    def plot_residence(self,data_dict,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        return
    
##########################################################################################################
    def plot_quorum(self,data_dict,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        return
    
##########################################################################################################
    def plot_controlParameter(self,data_dict,output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        return