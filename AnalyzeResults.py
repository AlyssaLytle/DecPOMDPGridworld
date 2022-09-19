def find_time_difference(start_time, end_time):
    [start_min, start_sec] = start_time
    [end_min, end_sec] = end_time
    end_min = int(end_min)
    start_min = int(start_min)
    if end_min < start_min:
        end_min += 60
    minutes = end_min - start_min
    seconds = 60 * minutes + int(end_sec) - int(start_sec)
    return seconds



def find_list_differences(start_list,end_list):
    diff_array = []
    for idx in range(len(start_list)):
        start_time = start_list[idx]
        end_time = end_list[idx]
        diff_array.append(find_time_difference(start_time, end_time))
    av_time = sum(diff_array)/len(diff_array)
    return av_time

def analyze_results(fname):
    f = open(fname, "r")
    outputs = f.readlines()
    ex1_start_times = []
    ex2_start_times = []
    ex3_start_times = []
    ex3_end_times = []
    for l in outputs:
        line = l.split(":")
        if line[0][-1] == "1":
            #ex 1 start time
            min = line[1][1:]
            sec = line[2][:2]
            ex1_start_times.append([min,sec])
        elif line[0][-1] == "2":
            #ex 2 start time
            min = line[1][1:]
            sec = line[2][:2]
            ex2_start_times.append([min,sec])
        elif line[0][0] == "E":
            #ex 3 end time
            min = line[1][1:]
            sec = line[2][:2]
            ex3_end_times.append([min,sec])
        else:
            #ex 3 start time
            min = line[1][1:]
            sec = line[2][:2]
            ex3_start_times.append([min,sec])
    ex1_av_time = find_list_differences(ex1_start_times, ex2_start_times)
    ex2_av_time = find_list_differences(ex2_start_times, ex3_start_times)
    ex3_av_time = find_list_differences(ex3_start_times, ex3_end_times)
    return [ex1_av_time, ex2_av_time, ex3_av_time]
    #return [ex1_start_times, ex2_start_times, ex3_start_times, ex3_end_times]

print("Average Times with Optimization:")
print(analyze_results("optoutputs.log"))
print("Average Times without Optimization:")
print(analyze_results("nonoptout.log"))