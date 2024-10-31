# coding=gbk
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


# Get user input for cp_ACCEL_sift_to_path
cp_ACCEL_sift_to_path = target_folder

# Traverse the two levels of subdirectories under cp_ACCEL_sift_to_path
cp_ACCEL_sift_to_path_list = []

for root, dirs, files in os.walk(cp_ACCEL_sift_to_path):
    dirs[:] = [d for d in dirs if not d.startswith(".__dpc")]  # Exclude dirs starting with ".__dpc"
    for dir in dirs:
        current_path = os.path.join(root, dir)
        for sub_dir in os.listdir(current_path):  # Iterate over subdirectories of current_path
            sub_path = os.path.join(current_path, sub_dir)
            if os.path.isdir(sub_path):  # Check if it is a directory
                base_path = sub_path
                cp_ACCEL_sift_to_path_list.append(base_path)
                # Copy ACCEL_sift.py to the subdirectory
                command = f"cp /groups/g9800070/home/share/pulsar_software/presto/examplescripts/ACCEL_sift.py {base_path}"
                os.system(command)

# Generate ACCEL_sift_command.txt file
with open("4.ACCEL_sift_command.txt", "w") as file:
    for path in cp_ACCEL_sift_to_path_list:
#        command = f"cd {path};ACCEL_sift.py > {path}/cands.txt\n"
        command = f"cd {path};LD_PRELOAD=/usr/lib64/libgfortran.so.3 python $PRESTO/examplescripts/ACCEL_sift.py > cands.txt\n"
        file.write(command)
    file.write("wait")
print("成功！")
