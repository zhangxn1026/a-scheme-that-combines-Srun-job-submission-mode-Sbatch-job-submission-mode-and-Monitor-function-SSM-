# coding=gbk
import os

# 读取配置文件
with open("config.txt", "r") as f:
    config_data = f.read().splitlines()

# 提取参数
input_path = config_data[1].split(" = ")[1].strip()
output_path = config_data[2].split(" = ")[1].strip()

def create_directory_structure(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        # 构造对应的目标文件夹路径
        target_root = os.path.join(output_folder, os.path.relpath(root, input_folder))
        # 创建目标文件夹
        if not os.path.exists(target_root):
            os.makedirs(target_root)
        for directory in dirs:
            # 构造对应的目标子文件夹路径
            target_directory = os.path.join(target_root, directory)
            # 创建目标子文件夹
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)

def main():
    create_directory_structure(input_path, output_path)

if __name__ == "__main__":
    main()
