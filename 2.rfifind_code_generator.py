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


# 提示用户输入参数值
#time = automate_task.time
output_path = target_folder
imput_path = source_folder

# 获取$output_path的子文件夹完整路径（至少往下遍历2层）
output_paths = []
for folder1 in os.listdir(output_path):
    sub_path1 = os.path.join(output_path, folder1)
    if os.path.isdir(sub_path1):
        for folder2 in os.listdir(sub_path1):
            sub_path2 = os.path.join(sub_path1, folder2)
            if os.path.isdir(sub_path2) and not folder2.startswith("__dpc"):
                output_paths.append(sub_path2)

# 获取$imput_path的子文件夹完整路径（至少往下遍历2层）
imput_paths = []
for folder1 in os.listdir(imput_path):
    sub_path1 = os.path.join(imput_path, folder1)
    if os.path.isdir(sub_path1):
        for folder2 in os.listdir(sub_path1):
            sub_path2 = os.path.join(sub_path1, folder2)
            if os.path.isdir(sub_path2) and not folder2.startswith("__dpc"):
                imput_paths.append(sub_path2)

# 获取$name1和$name2的值
name1 = imput_path.split('/')[-1]
name2_folders = os.listdir(imput_path)
names2 = []
for folder in name2_folders:
    if not folder.startswith("__dpc"):
        names2.append(folder)

# 生成命令行并写入txt文件，确保生成的命令行不重复
command_lines = []
for output in output_paths:
    for imput in imput_paths:
        for name2 in names2:
            if os.path.basename(os.path.dirname(output)) == os.path.basename(os.path.dirname(imput)) == name2:
                command_line = f"rfifind -ignorechan 0:200,640:800,3800:4100 -time {time} -o {output}/{name1}_{name2}_{time} {imput}/*.fits"
                command_lines.append(command_line)

# 将命令行写入txt文件
with open("2.rfifind_command.txt", "w") as file:
    for command_line in command_lines:
        file.write(command_line + "\n")
    file.write("wait")

print("脚本运行结束，命令行已生成至2.rfifind_command.txt文件！")
