import os
import sys
import datetime

from collections import defaultdict

remove_flag = False

configs = {
    'script_path': os.path.abspath(os.getcwd()),
    'b_dir': os.path.abspath('./klee/build/'),
}

def gen_run_cmd(pgm, a_budget, trial, 
                used_core, seed):
    argv = "--sym-args 0 1 10 --sym-args 0 2 2 --sym-files 1 8 --sym-stdin 8 --sym-stdout"

    if "sqlite" in pgm:
        pgm = "sqlite3"
    
    if seed == "":
        postfix = " ".join(["",
            pgm + ".bc",
            argv])
    else:
        postfix = " ".join(["",
            "-seed-file=" + seed,
            pgm + ".bc",
            argv])
        
    run_cmd = " ".join([configs['b_dir']+"/bin/klee", 
                                "-only-output-states-covering-new", "--simplify-sym-indices", "--output-module=false",
                                "--output-source=false", "--output-stats=false", "--disable-inlining", 
                                "--optimize", "--use-forked-solver", "--use-cex-cache", "--libc=uclibc", 
                                "--posix-runtime", "-env-file=" + configs['b_dir'] + "/../test.env",
                                "--max-sym-array-size=4096", "--max-memory-inhibit=false",
                                "--switch-type=internal", "--use-batching-search", 
                                "--batch-instructions=10000", "--write-kqueries"
                                "--watchdog",
                                "-max-time=" + a_budget,  
                                f"{postfix}"
                        ]) 

    return run_cmd

def running_function(pconfig, pgm, top_dir, trial, total_time, init_time, a_budget, \
                    used_core, seed):
    global remove_flag
    core_dir = top_dir + "/" + str(used_core)
    if os.path.exists(core_dir) and not remove_flag:
        remove_flag = int(input("Duplicated Directory Founded! U wanna delete it? : "))
        
    if remove_flag:
        rm_duplicated_dir = " ".join(["rm", "-rf", core_dir])
        os.system(rm_duplicated_dir)

    os.mkdir(core_dir)

    core_exec_dir = core_dir + "/" + pconfig["exec_dir"]
    if not os.path.exists(core_exec_dir):
        os.mkdir(core_exec_dir)

    group_dir = configs["top_dir"] + "/obj_llvm" + str(used_core)
    os.system(" ".join(["cp -rf", pconfig['pgm_dir'] + "*", group_dir]))

    tc_location = group_dir + "/" + pconfig['exec_dir']
    os.chdir(tc_location)

    rc = 0
    os.chdir(tc_location) # home/jaehyeok/dd-klee/experiments/1__find1/gawk/1 (groupId)

    run_cmd = gen_run_cmd(pgm, a_budget, trial, used_core, seed) # klee command & log
    
    with open(os.devnull, 'wb') as devnull:
        os.system(run_cmd) # klee execution

    info_file = open(tc_location + "/klee-out-0/info", 'a')
    info_file.write("File : " + configs["script_path"] + "/" + sys.argv[0] + "\n")
    info_file.close()

    os.system(" ".join(["mv klee-out-0", core_exec_dir]))
    os.chdir(configs['script_path'])

def run(pconfig, pgm, trial, total_time, init_time, a_budget, \
        ith_trial, used_core, seed):
    global configs
    configs['top_dir'] = os.path.abspath("./experiments_exp_" + pgm + "/#" + str(ith_trial) + "experiment/")

    iter_dir = "/".join([configs['top_dir'], "iteration_" + trial])
    top_dir = "/".join([iter_dir, pgm])
    os.makedirs(top_dir)    

    rc = running_function(pconfig, pgm, top_dir, trial, total_time, init_time, a_budget, \
                        used_core, seed)
