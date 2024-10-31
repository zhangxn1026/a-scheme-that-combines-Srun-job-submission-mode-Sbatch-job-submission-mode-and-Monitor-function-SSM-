# -*- coding: utf-8 -*-  
import subprocess  
import time  
import sys  # 导入 sys 模块以处理命令行参数  

submitted_jobs = set()  

def check_idle_nodes():  
    node_cores = []  
    # Adjust the command to retrieve node info as per requirement  
    node_info_output = subprocess.check_output(['sinfo', '-p', 'cpu-liminghui', '-N', '-o', '"%.15P %c %C %N"'], universal_newlines=True)  
    node_info_list = node_info_output.strip().split('\n')  
    for i, node_info in enumerate(node_info_list):  
        if i == 0:  # Skip header line  
            continue  
        fields = node_info.split()  
        if len(fields) >= 4:  
            partition = fields[0]  
            try:  
                core_name = fields[4].strip('"')  
                num_cores_idle = int(fields[3].split('/')[1])  
                num_cores_total = int(fields[3].split('/')[3])  
                print(num_cores_idle)  
                print(num_cores_total)  
            except ValueError:  
                print(f"Skipping line due to ValueError: {node_info}")  
                continue  
            node = fields[3]  
            if num_cores_idle > 0:  
                node_cores.append((core_name, num_cores_idle))  
        else:  
            print(f"Error parsing node info: {node_info}")  
    return node_cores  

def submit_jobs(core_name, num_cores_idle, task_file):  
    print(f"Submitting jobs on node {core_name} with {num_cores_idle} cores\n")  
    
    with open(task_file, 'r') as file:  
        commands = file.readlines()  

    job_file_path2 = f"job-{core_name}-task{num_cores_idle*2}.txt"  
    with open(job_file_path2, 'w') as job_file2:  
        start_line = (num_cores_idle - 1) * 2  
        end_line = start_line + num_cores_idle * 2  
        for i in range(start_line, end_line):  
            if i < len(commands):  
                job_file2.write(commands[i])  
            else:  
                break  

    job_file_path = f"job-{core_name}-task{num_cores_idle*2}.sh"  
    with open(job_file_path, 'w') as job_file:  
        job_file.write("#!/bin/bash\n")  
        job_file.write("#SBATCH -J new_zxn_M2\n")  
        job_file.write("#SBATCH -o job-%j.log\n")  
        job_file.write("#SBATCH -e job-%j.err\n")  
        job_file.write("#SBATCH -p cpu-liminghui\n")  
        job_file.write(f"#SBATCH -w {core_name}\n")  
        job_file.write(f"#SBATCH -n {num_cores_idle}\n")  
        job_file.write('\n')  
        job_file.write(f'task_file="{job_file_path2}"\n')  
        job_file.write('while IFS= read -r cmd; do\n')  
        job_file.write('    echo "Running command: $cmd"\n')  
        job_file.write('    bash -c "$cmd"\n')  
        job_file.write('done < "$task_file"\n')  
        
    result = subprocess.run(['sbatch', job_file_path])  
    print(result)  # Print the result of the subprocess command  
    submitted_jobs.add(job_file_path)  

# 使用命令行参数而不是输入提示  
if len(sys.argv) != 2:  
    print("Usage: python submit_jobs.py <task_file>")  
    sys.exit(1)  

task_file = sys.argv[1]  

# Main loop  
while True:  
    node_cores = check_idle_nodes()  
    
    if node_cores:  
        for core_name, num_cores_idle in node_cores:  
            submit_jobs(core_name, num_cores_idle, task_file)  # Pass the task_file parameter here  
            time.sleep(1)  # Wait 1 second between submitting jobs on each node  
       
        # Wait for all submitted jobs to finish  
        while submitted_jobs:  
            time.sleep(10)  # Check every 10 seconds  
            running_jobs = subprocess.check_output(['squeue', '-u', 'zhangxingnan'], universal_newlines=True)  
            if not running_jobs:  
                submitted_jobs.clear()  # Clear submitted jobs set if no jobs are running  
        
    print("Sleeping for 2 seconds...")  
    time.sleep(60)  # Check every 60 seconds
