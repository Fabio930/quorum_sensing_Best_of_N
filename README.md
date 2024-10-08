# SwarmRobotics_Best_of_N

This is a simple multi-agent simulation environment for mobile agents.
Install the venv through the command 'compile.sh'. Launch a simple visual experiment through the command 'run.sh' or a set of experiments wich results will be saved through the command 'runbatch.sh'

The basic classes provide a not-spatial simulation about Best of N decision making problem.

The xml file in the 'config' folder provides the basic configuration options for the arena and the agents, as well as for the GUI. The GUI can be disable commenting the respective line.
The xml file in the 'config/batch' folder provides the basic configuration options for the arena and the agents which are managed in 'config/batch_config.xml' and 'config/batch/loop_runs.sh' file. In batch tests the GUI is disabled.

Everything can be configured by overloading the base classes.

After 'runbatch.sh' completes all the simulations then is possible to process the data with the 'dump_result.py' command. The plots of the data can be performed afterwards with the command 'plot_results.py'.
