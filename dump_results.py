import data_extractor as dex
import os
import sys
import logging
import gc
import time
import psutil
from multiprocessing import Process, Manager

# Setup logging
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

# Check command line inputs
def check_inputs():
    if len(sys.argv) > 1:
        logging.error("Too many arguments --EXIT--")
        exit()
    return

# Process folder with retries and memory management
def process_folder(task):
    exp_length, rec_time, dif_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, msg_path = task
    retry_count = 50

    while retry_count > 0:
        try:
            # Memory usage logging
            process = psutil.Process(os.getpid())
            logging.info(f"Memory usage before processing {msg_path}: {process.memory_info().rss / (1024 * 1024)} MB")

            results = dex.Results()
            results.extract_k_data(exp_length, rec_time, dif_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, msg_path)
            gc.collect()
            # Memory usage logging
            logging.info(f"Memory usage after processing {msg_path}: {process.memory_info().rss / (1024 * 1024)} MB")

            break
        except MemoryError as e:
            logging.error(f"MemoryError processing {msg_path}: {e}")
            retry_count -= 1
            if retry_count > 0:
                logging.info(f"Retrying {msg_path} ({retry_count}) after MemoryError")
                time.sleep(600)  # Delay before retrying
            else:
                logging.error(f"Failed {msg_path} due to MemoryError")
            gc.collect()
        except Exception as e:
            logging.error(f"Error processing {msg_path}: {e}")
            gc.collect()
            break

def main():
    setup_logging()
    check_inputs()

    tasks = []
    base = dex.Results().input_folder:
    for exp_l_dir in sorted(os.listdir(base)):
        if '.' not in exp_l_dir and '#' in exp_l_dir:
            exp_l_path = os.path.join(base, exp_l_dir)
            values = exp_l_dir.split('_')
            exp_length = int(values[0].split('#')[1])
            rec_time = int(values[1].split('#')[1]) if len(values)==2 else int(values[2].split('#')[1])
            dif_time = None
            if len(values)==3: dif_time = int(values[1].split('#')[1])
            for comm_dir in sorted(os.listdir(exp_l_path)):
                if '.' not in comm_dir and '#' in comm_dir:
                    comm_path = os.path.join(exp_l_path, comm_dir)
                    communication = str(comm_dir.split('#')[1])
                    for agents_dir in sorted(os.listdir(comm_path)):
                        if '.' not in agents_dir and '#' in agents_dir:
                            agents_path = os.path.join(comm_path, agents_dir)
                            n_agents = int(agents_dir.split('#')[1])
                            for options_dir in sorted(os.listdir(agents_path)):
                                if '.' not in options_dir and '#' in options_dir:
                                    options_path = os.path.join(agents_path, options_dir)
                                    n_options = int(options_dir.split('#')[1])
                                    for model_dir in sorted(os.listdir(options_path)):
                                        if '.' not in model_dir and '#' in model_dir:
                                            model_path = os.path.join(options_path,model_dir)
                                            model = str(model_dir.split('#')[1])
                                            for r_dir in sorted(os.listdir(model_path)):
                                                if '.' not in r_dir and '#' in r_dir:
                                                    r_path = os.path.join(model_path,r_dir)
                                                    r_type = str(r_dir.split('_')[0].split('#')[1])
                                                    r_value = float(str(r_dir.split('_')[1].split('#')[1]).replace(",","."))
                                                    for eta_dir in sorted(os.listdir(r_path)):
                                                        if '.' not in eta_dir and '#' in eta_dir:
                                                            eta_path = os.path.join(r_path,eta_dir)
                                                            eta_value = float(str(eta_dir.split('#')[1]).replace(",","."))
                                                            for msg_dir in sorted(os.listdir(eta_path)):
                                                                if '.' not in msg_dir and '#' in msg_dir:
                                                                    msg_path = os.path.join(eta_path,msg_dir)
                                                                    values = msg_dir.split('_')
                                                                    quorum_min_list = int(values[0].split('#')[1])
                                                                    msg_timeout = int(values[1].split('#')[1])
                                                                    msg_x_step = int(values[2].split('#')[1])
                                                                    msg_hops = int(values[3].split('#')[1])
                                                                    tasks.append((exp_length, rec_time, dif_time, communication, n_agents, n_options, model, r_type, r_value, eta_value, quorum_min_list, msg_timeout, msg_x_step, msg_hops, msg_path))

    # Using a manager to handle the queue
    manager = Manager()
    queue = manager.Queue()

    for task in tasks:
        queue.put(task)

    active_processes = []
    total_memory = psutil.virtual_memory().total / (1024 * 1024)  # Total memory in MB
    memory_per_process_25 = 162625 / 1024 # Memory used by each process with 25 agents check
    memory_per_process_100 = 325250 / 1024 # Memory used by each process with 100 agents check

    while not queue.empty() or active_processes:
        # Calculate total memory used by active processes
        total_memory_used = sum(memory_per_process_25 if n_agents == 25 else memory_per_process_100 for p, n_agents in active_processes)

        # Launch new processes if there is room
        while total_memory_used + min(memory_per_process_25, memory_per_process_100) <= total_memory and not queue.empty():
            task = queue.get()
            n_agents = task[4]
            required_memory = memory_per_process_25 if n_agents == 25 else memory_per_process_100
            if total_memory_used + required_memory < total_memory:
                p = Process(target=process_folder, args=(task,))
                p.start()
                active_processes.append((p, n_agents))
                total_memory_used += required_memory
            else:
                # Requeue the task if there's not enough memory
                queue.put(task)
                break
        # Check for completed processes
        for p, n_agents in active_processes:
            if not p.is_alive():
                p.join()
                active_processes.remove((p, n_agents))
                if n_agents == 25:
                    total_memory_used -= memory_per_process_25
                elif n_agents == 100:
                    total_memory_used -= memory_per_process_100

        time.sleep(1)  # Avoid busy-waiting

    logging.info("All tasks completed.")

if __name__ == "__main__":
    main()
