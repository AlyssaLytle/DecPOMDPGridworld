

def make_cmd(fname, ie, cluster):
    solve_comm = "../MADP2/src/solvers/GMAA --sparse --GMAA=MAAstar"    
    horizon_arg = " -h4"
    clustering_arg = " --useBGclustering"
    ie_arg = " --BGIP_Solver=BnB --BnB-ordering=Prob"
    no_out = " > /dev/null\n"
    output = solve_comm
    if ie:
        output += ie_arg
    if cluster:
        output += clustering_arg
    output += " " + fname
    output += horizon_arg
    output += no_out
    return output

def make_shell(ie, cluster, shellname, num_repeats):
    get_time = """now="$(date +'%M:%S')"\n"""
    cmd = "cd .. \n"
    for x in range(num_repeats):
        cmd += get_time
        cmd += """echo "Start time ex 1: $now"\n"""
        cmd += make_cmd('33gw.dpomdp', ie, cluster)
        cmd += get_time
        cmd += """echo "Start time ex 2: $now"\n"""
        cmd += make_cmd('33gw-nocomm.dpomdp',ie,cluster)
        cmd += get_time
        cmd += """echo "Start time ex 3: $now"\n"""
        cmd += make_cmd('33gw-late.dpomdp', ie, cluster)
        cmd += get_time
        cmd += """echo "End time ex 3: $now"\n"""
    f = open(shellname, "w")
    f.writelines(cmd)
    f.close

def call_line(ex_name):
    pref = ex_name[:-3]
    out = "sh " + ex_name + " > " + pref + ".log\n"
    return out
    
No_opt_name = "NoOpt.sh"
IE_name = "IE.sh"
Cluster_name = "IC.sh"
ICE_name = "ICE.sh"
#fnames = [No_opt_name, IE_name, Cluster_name, ICE_name]

call_line(No_opt_name)


num_ex = 10
shell_out = ""
make_shell(False, False, No_opt_name, num_ex)
shell_out += call_line(No_opt_name)
make_shell(True, False, IE_name, num_ex)
shell_out += call_line(IE_name)
make_shell(False, True, Cluster_name, num_ex)
shell_out += call_line(Cluster_name)
make_shell(True, True, ICE_name, num_ex)
shell_out += call_line(ICE_name)

f = open("RunAll.sh", "w")
f.writelines(shell_out)
f.close

