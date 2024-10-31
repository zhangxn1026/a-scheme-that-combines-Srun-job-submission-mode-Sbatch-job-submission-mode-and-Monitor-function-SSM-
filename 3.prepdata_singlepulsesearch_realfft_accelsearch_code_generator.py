#	coding=gbk
import os
import numpy as np


# 读取配置文件
with open("./config.txt", "r") as f:
    config_data = f.read().splitlines()

# 提取参数
time = config_data[0].split(" = ")[1].strip()
source_folder = config_data[1].split(" = ")[1].strip()
target_folder = config_data[2].split(" = ")[1].strip()
min_DM = float(config_data[3].split(" = ")[1].strip())
max_DM = float(config_data[4].split(" = ")[1].strip())
step_size = float(config_data[5].split(" = ")[1].strip())
zmax = config_data[6].split(" = ")[1].strip()
numharm = config_data[7].split(" = ")[1].strip()
channels = config_data[8].split(" = ")[1].strip()



# 获取用户输入的参数
#min_DM = automate_task.min_DM
#max_DM = automate_task.max_DM
#step_size = automate_task.step_size
output_path = target_folder
fits_input_path = source_folder 
#zmax = automate_task.zmax
#numharm = automate_task.numharm

# 查询输出路径下所有子文件夹的完整路径（过滤掉以.__dpc开头的文件夹）
output_paths = []
for dirpath, dirnames, filenames in os.walk(output_path):
    dirnames[:] = [dirname for dirname in dirnames if not dirname.startswith(".__dpc")]
    for dirname in dirnames:
        output_paths.append(os.path.join(dirpath, dirname))

# 查询输入路径下所有子文件夹的完整路径（过滤掉以.__dpc开头的文件夹）
fits_input_paths = []
for dirpath, dirnames, filenames in os.walk(fits_input_path):
    dirnames[:] = [dirname for dirname in dirnames if not dirname.startswith(".__dpc")]
    for dirname in dirnames:
        fits_input_paths.append(os.path.join(dirpath, dirname))

# 生成name2的列表
names2_list = [os.path.basename(dirpath) for dirpath in fits_input_paths]

# 获取name1
name1 = output_path.split('/')[-1]

# 生成命令行
cmds = []
cmds2 = []
file_cmds = []
file_cmds2 = []
for name2 in names2_list:
    for fits_input_path in fits_input_paths:
        for output_path in output_paths:
            if os.path.basename(os.path.dirname(fits_input_path)) == os.path.basename(os.path.dirname(output_path)) == name2:
#                filename = f"3.prepdata_realfft_accelsearch_command.txt"
                for DM in np.arange(min_DM, max_DM + step_size, step_size):
                    prepdata_cmd = f"cd {output_path} && prepdata -downsamp 1 -ignorechan 0:200,640:800,3800:4100 -dm {DM:.2f} -nobary -mask {output_path}/*.mask -o {output_path}/{name1}_{name2}_DM{DM:.2f} {fits_input_path}/*.fits"
                    single_pulse_search_cmd = f"single_pulse_search.py -b -m 300 {output_path}/{name1}_{name2}_DM{DM:.2f}.dat"
                    realfft_cmd = f"realfft -fwd -mem {output_path}/{name1}_{name2}_DM{DM:.2f}.dat"
                    accelsearch_cmd = f"accelsearch -zmax {zmax} -numharm {numharm} -inmem {output_path}/{name1}_{name2}_DM{DM:.2f}.fft"
                    cmd = f"{prepdata_cmd} && {single_pulse_search_cmd}"
                    cmd2 = f"cd {output_path} && {realfft_cmd} && {accelsearch_cmd}"
                    file_cmds.append(cmd)
                    file_cmds2.append(cmd2)
                cmds.append((file_cmds))
                cmds2.append((file_cmds2))
# 生成文件
for file_cmds in cmds:
    with open("3.1.prepdata_single_pulse_search_command.txt", "w") as f:
        f.write("\n".join(file_cmds))
        f.write("\nwait")
for file_cmds2 in cmds2:
    with open("3.2.realfft_accelsearch_command.txt", "w") as f:
        f.write("\n".join(file_cmds2))
        f.write("\nwait")

print("成功！")
