# -*- coding: utf-8 -*-
# @author Fabio Oddi <fabioddi24@gmail.com>

import tkinter as tk
import numpy as np

########################################################################################
## Pysage GUI
########################################################################################

##########################################################################
# factory to dynamically create the gui
class GUIFactory:
    factories = {}
    def add_factory(id, gui_factory):
        GUIFactory.factories[id] = gui_factory
        return
    add_factory = staticmethod(add_factory)

    def create_gui(master, arena, config_element):
        gui_pkg = config_element.attrib.get("pkg")
        if gui_pkg is None:
            return PysageGUI.Factory().create(master, arena, config_element)
        id = gui_pkg + ".gui"
        gui_type = config_element.attrib.get("type")
        if gui_type is not None:
            id = gui_pkg + "." + gui_type + ".gui"
        return GUIFactory.factories[id].create(master, arena, config_element)
    create_gui = staticmethod(create_gui)


##########################################################################
# GUI main class
class PysageGUI(object):

    class Factory:
        def create(self, master, arena, config_element): return PysageGUI(master, arena, config_element)

    ##########################################################################
    # standart class init
    def __init__(self, master, arena, config_element):

        self.master = master
        self.font=("Arial", 25)

        self.delay  = 1.0 if config_element.attrib.get("delay")  is None else float(config_element.attrib["delay"])
        self.pixels_per_meter = 100 if config_element.attrib.get("pixels_per_meter")  is None else int(config_element.attrib["pixels_per_meter"])

        # Initialize the arena and the agents
        self.arena = arena
        self.arena.init_experiment()

        # start the GUI
        self.timestep = 0
        self.best_opt = tk.StringVar()
        self.timestring = tk.StringVar()
        self.r_string_mean = tk.StringVar()
        self.r_string_std = tk.StringVar()
        self.timestring.set(str(self.timestep))
        self.best_opt.set("  best = "+str(self.arena.get_best_option()))
        self.r_string_mean.set("   r :  mean = 0")
        self.r_string_std.set(" std = 0")
        self.initialize()

        # initialise running state
        self.isRunning = False
        return

    ##########################################################################
    # GUI step function: advance the simulation by one time step
    def step(self):
        if not self.arena.experiment_finished():
            self.stop_button.config(state="normal")
            self.step_button.config(state="normal")
            self.run_button.config(state="disabled")
            self.reset_button.config(state="normal")
            self.switch_quality_button.config(state="normal")
            self.arena.update()
            self.timestring.set( str(self.arena.num_steps) )
            mean_R = 0
            s_R = 0
            for a in self.arena.agents:
                mean_R+=a.r
            mean_R=round(mean_R/len(self.arena.agents),2)
            for a in self.arena.agents:
                s_R+=(a.r-mean_R)**2
            stdR=round((s_R/(len(self.arena.agents)-1))**.5,3)
            self.best_opt.set("  best = "+str(self.arena.get_best_option()))
            self.r_string_mean.set("   r :  mean = "+str(mean_R))
            self.r_string_std.set(" std = "+str(stdR))
            self.master.update_idletasks()
            self.w.delete("all")
            if self.w.winfo_width!=self.t_width or self.w.winfo_height()!=self.t_height:
                self.t_width, self.t_height = self.w.winfo_width(),self.w.winfo_height()
                self.compute_positions()
            self.draw_arena()
        else:
            self.stop_button.config(state="disabled")
            self.step_button.config(state="disabled")
            self.run_button.config(state="disabled")
            self.reset_button.config(state="normal")
            self.switch_quality_button.config(state="disable")
            self.stop()
        return

    ##########################################################################
    # GUI run helper function
    def run_( self ):
        if self.isRunning:
            self.step()
            ms = int(10.0 * max(self.delay, 1.0))
            self.master.after(ms, self.run_)
        return

    ##########################################################################
    # GUI run function: advance the simulation
    def run(self):
        if not self.isRunning:
            self.isRunning = True
            self.run_()
        return
    
    ##########################################################################
    # GUI stop function: stops the simulation
    def stop(self):
        self.isRunning = False
        self.timestring.set( str(self.timestep) )
        self.stop_button.config(state="disabled")
        self.step_button.config(state="normal")
        self.run_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.switch_quality_button.config(state="normal")
        self.timestring.set( str(self.arena.num_steps) )
        self.master.update_idletasks()
        return
    
    ##########################################################################
    # GUI reset function: reset the simulation
    def reset(self):
        self.isRunning = False
        self.stop_button.config(state="disabled")
        self.step_button.config(state="normal")
        self.run_button.config(state="normal")
        self.reset_button.config(state="disabled")
        self.switch_quality_button.config(state="disabled")
        self.arena.set_random_seed()
        self.arena.init_experiment()
        self.timestring.set( str(self.arena.num_steps) )
        self.best_opt.set("  best = "+str(self.arena.get_best_option()))
        self.r_string_mean.set("   r :  mean = 0")
        self.r_string_std.set(" std = 0")
        self.compute_positions()
        self.draw_arena()
        self.master.update_idletasks()
        return
    
    ##########################################################################
    def switch_quality(self):
        self.arena.variation_time = self.arena.num_steps
        self.arena.change = 1
        self.best_opt.set("  best = "+str(self.arena.get_best_option()))
        return

    ##########################################################################
    # GUI intialize function: stup the tk environemt
    def initialize(self):
        self.toolbar = tk.Frame(self.master, relief="raised", bd=2)
        self.toolbar.pack(side="top", fill="x")
        self.step_button = tk.Button(self.toolbar, text="Step", command=self.step)
        self.run_button = tk.Button(self.toolbar, text="Run", command=self.run)
        self.stop_button = tk.Button(self.toolbar, text="Stop", command=self.stop)
        self.reset_button = tk.Button(self.toolbar, text="Reset", command=self.reset)
        self.switch_quality_button = tk.Button(self.toolbar, text="Switch quality", command=self.switch_quality)
        self.step_button.pack(side="left")
        self.stop_button.pack(side="left")
        self.run_button.pack(side="left")
        self.reset_button.pack(side="left")
        self.switch_quality_button.pack(side="left")
        self.stop_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.switch_quality_button.config(state="disabled")

        self.labOpt = tk.Label(self.toolbar, textvariable = self.best_opt)
        self.labOpt.pack(side="left")
        self.labRm = tk.Label(self.toolbar, textvariable = self.r_string_mean)
        self.labRm.pack(side="left",padx=10)
        self.labRs = tk.Label(self.toolbar, textvariable = self.r_string_std)
        self.labRs.pack(side="left",padx=10)
        self.label = tk.Label(self.toolbar, textvariable = self.timestring)
        self.label.pack(side="right")

        self.t_width = 800
        self.t_height = 500
        self.w = tk.Canvas(self.master, width=int(self.t_width), height=int(self.t_height), background="dimgray")
        self.w.pack(side="left",fill="both",expand="True")
        self.compute_positions()
        self.draw_arena()
        
    #########################################################################
    def compute_positions(self):
        x1,y1 = 10,10
        x2,y2 = x1+30,y1+30
        for a in range(len(self.arena.agents)):
            self.arena.agents[a].position = [x1,y1,x2,y2]
            if x2 < self.t_width - 50:
                x1 = x2 + 5
                x2 = x1 + 30
            else:
                x1,x2 = 10,40
                y1 = y2 + 5
                y2 = y1 + 30
            if y2 >= self.t_height*0.8 and x2 >=self.t_width:
                print("[WARNING] not enough space for placing agents.")
        x1,y1 = 10, self.t_height*0.8
        x2,y2 = x1+70,y1+50
        for o in range(len(self.arena.options)):
            self.arena.options[o].position = [x1,y1,x2,y2]
            if x2 < self.t_width - 70:
                x1 = x2 + 5
                x2 = x1 + 70
            else:
                x1,x2 = 10,80
                y1 = y2 + 5
                y2 = y1 + 50
            if y2 >= self.t_height and x2 >=self.t_width:
                print("[WARNING] not enough space for placing options.")
        return
    
    #########################################################################
    def draw_arena(self):
        for a in self.arena.agents:
            self.w.create_oval(a.position[0],a.position[1],a.position[2],a.position[3],fill="white")
            if a.committed > -1:
                self.w.create_oval(a.position[0]+5,a.position[1]+5,a.position[2]-5,a.position[3]-5,fill=self.arena.options[a.committed].color)
        for o in self.arena.options:
            self.w.create_rectangle(o.position[0],o.position[1],o.position[2],o.position[3],fill=(o.color))
            self.w.create_text(o.position[0]+5,o.position[1]+5,anchor="nw",text=str(self.arena.get_committed_to(o.id)),font=self.font,fill="black")
        self.w.create_text(self.arena.options[-1].position[2]+5,self.t_height*0.8+5,anchor="nw",text=str(self.arena.get_committed_to(-1)),font=self.font,fill="black")
        return