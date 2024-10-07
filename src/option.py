# -*- coding: utf-8 -*-
# @author Fabio Oddi <fabioddi24@gmail.com>

import matplotlib,random
import matplotlib.colors as colors
import matplotlib.cm as cmx

########################################################################################
## Option
########################################################################################

##########################################################################
# factory to dynamically create agents
class OptionFactory:
    factories = {}

    def add_factory(id, option_factory):
        OptionFactory.factories[id] = option_factory
        return
    
    add_factory = staticmethod(add_factory)

    def create_option(config_element, arena):
        option_pkg = config_element.attrib.get("pkg")
        if option_pkg is None:
            return Option.Factory().create(config_element, arena)
        id = option_pkg + ".option"
        option_type = config_element.attrib.get("type")
        if option_type is not None:
            id = option_pkg + "." + option_type + ".option"
        return OptionFactory.factories[id].create(config_element, arena)
    
    create_agent = staticmethod(create_option)


##########################################################################
# the main agent class
class Option:

    num_options     = 0
    arena           = None
    max_utility     = 10.0
    std_utility     = 1.0
    k_utility       = 0.7

    cm = matplotlib.cm.get_cmap("viridis")
    typo = [0,1,2]
    cNorm  = colors.Normalize(vmin=typo[0], vmax=typo[-1])
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

    class Factory:
        def create(self, config_element, arena): return Option(config_element, arena)

    ##########################################################################
    # Initialisation of the Agent class
    def __init__(self, config_element, arena):

        self.id = Option.num_options
        if self.id == 0:
            Option.arena = arena
            Option.typo = []
            for i in range(arena.num_options):
                Option.typo.append(i)
                Option.cNorm  = colors.Normalize(vmin=Option.typo[0], vmax=Option.typo[-1])
                Option.scalarMap = cmx.ScalarMappable(norm=Option.cNorm, cmap=Option.cm)
            mu = config_element.attrib.get("max_utility")
            if mu is None:
                print ("[WARNING] missing attribute <max_utility> in tag <option>. Set to default value 10.\n")
            else:
                mu = float(mu)
                if mu<=0:
                    print ("[WARNING] attribute <max_utility> in tag <option> should be > 0. Set to default value 10.\n")
                else:
                    Option.max_utility = mu
            ms = config_element.attrib.get("std_utility")
            if ms is None:
                print ("[WARNING] missing attribute <std_utility> in tag <option>. Set to default value 1.\n")
            else:
                ms = float(ms)
                if ms<0:
                    print ("[WARNING] attribute <std_utility> in tag <option> should be >= 0. Set to default value 1.\n")
                else:
                    Option.std_utility = ms
            ku = config_element.attrib.get("k_utility")
            if ku is None:
                print ("[WARNING] missing attribute <k_utility> in tag <option>. Set to default value 0.7.\n")
            else:
                ku = float(ku)
                if ku<=0 or ku>1:
                    print ("[WARNING] attribute <k_utility> in tag <option> should be in [0,1]. Set to default value 0.7.\n")
                else:
                    Option.k_utility = ku
            self.utility = Option.max_utility
        else:
            self.utility = Option.max_utility * Option.k_utility
        self.color = colors.rgb2hex(Option.scalarMap.to_rgba(Option.typo[self.id])[:-1])
        Option.num_options += 1
        return

    ##########################################################################
    # generic init function brings back to initial positions
    def init_experiment( self ):
        self.position = [0,0,0,0]
        self.utility = Option.max_utility if self.id==0 else Option.max_utility*Option.k_utility
        return
    
    ##########################################################################
    def get_quality(self):
        return self.utility + random.uniform(0,Option.std_utility)
    