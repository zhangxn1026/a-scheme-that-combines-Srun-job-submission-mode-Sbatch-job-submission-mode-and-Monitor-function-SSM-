#	coding=gbk
import os

# 读取配置文件
with open("./config.txt", "r") as f:
    config_data = f.read().splitlines()

# 提取参数
time = config_data[0].split(" = ")[1].strip()
source_folder = config_data[1].split(" = ")[1].strip()
target_folder = config_data[2].split(" = ")[1].strip()
min_DM = config_data[3].split(" = ")[1].strip()
max_DM = config_data[4].split(" = ")[1].strip()
step_size = config_data[5].split(" = ")[1].strip()
zmax = config_data[6].split(" = ")[1].strip()
numharm = config_data[7].split(" = ")[1].strip()
channels = config_data[8].split(" = ")[1].strip()

# 1. 提示用户输入参数
prepfold_path = target_folder
fits_path = source_folder
#zmax = automate_task.zmax
#channels = automate_task.channels

# 查询输出路径下所有子文件夹的完整路径（过滤掉以.__dpc开头的文件夹）
output_paths = []
for root, dirnames, filenames in os.walk(prepfold_path):
    if root.count(os.sep) - prepfold_path.count(os.sep) == 2:
        output_paths.append(root)
# 查询输入路径下所有子文件夹的完整路径（过滤掉以.__dpc开头的文件夹）
fits_input_paths = []
for root, dirnames, filenames in os.walk(fits_path):
    if root.count(os.sep) - fits_path.count(os.sep) == 2:
        fits_input_paths.append(root)

# 生成name2的列表
names2_list = []
names2_list = [name for name in os.listdir(fits_path) if os.path.isdir(os.path.join(fits_path, name))]
# 获取name1
name1 = prepfold_path.split('/')[-1]

# 读取cands.txt文件，提取包含"ACCEL"关键字的行，并获取相应的变量值
file_lines = []
for output in output_paths:
    for pulsar_name in names2_list:
        with open(os.path.join(output, "cands.txt"), 'r') as f:
            for line in f:
                if "ACCEL" in line:
                    values = line.split()
                    psr_dm = values[1]
                    psr_candnum = values[0].split(":")[1]
                    psr_candfile = str(name1) + "_" + str(pulsar_name) + "_DM" + str(psr_dm) + "_ACCEL_" + str(int(zmax)) + ".cand"
                    file_lines.append((float(psr_dm), int(psr_candnum), psr_candfile))

# 生成命令行
command_lines = []
for name2 in names2_list:
    for fits_input_path in fits_input_paths:
        for output_path in output_paths:
            if os.path.basename(os.path.dirname(fits_input_path)) == os.path.basename(os.path.dirname(output_path)) == name2:
                for line in file_lines:
                    command = "cd {} && prepfold -npart 128  -ignorechan 0:400,640:800,3800:4100 -start 0.01 -end 0.99 -noxwin -topo -mask {}/*.mask -dm {} -nsub {} -nosearch -o {}_{}_fits_DM{}_{} -accelcand {} -accelfile {} {}/*.fits".format(output_path, output_path, line[0], channels, name1, name2, line[0], line[1], line[1], line[2],fits_input_path)
                    command_lines.append(command)

# 将命令行写入文件
with open("5.prepfold_fit_command.txt", 'w') as f:
    for command in command_lines:
        f.write(command + "\n")
    f.write("wait")

print("成功！")
