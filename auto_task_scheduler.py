#	coding=gbk
import os
import subprocess
import time
from datetime import datetime

with open("./config.txt", "r") as f:
    config_data = f.read().splitlines()

my_path = config_data[9].split(" = ")[1].strip()

# 调用FolderBuilder.py创建目标文件夹和子文件夹结构
subprocess.run(["python", "1.FolderBuilder.py"])
    
os.chdir(my_path)
# 生成2.rfifind_command.txt文件
subprocess.run(["python", "2.rfifind_code_generator.py"])
subprocess.run(["python", "Resource_monitoring.py 2.rfifind_command.txt"])
print(datetime.now())
os.chdir(my_path)

# 生成3.prepdata_realfft_accelsearch_command.txt文件
subprocess.run(["python", "3.prepdata_singlepulsesearch_realfft_accelsearch_code_generator.py"])
subprocess.run(["python", "Resource_monitoring.py 3.1.prepdata_single_pulse_search_command.txt"])
print(datetime.now())
os.chdir(my_path)
subprocess.run(["python", "Resource_monitoring.py 3.2.realfft_accelsearch_command.txt"])
print(datetime.now())
os.chdir(my_path)

# 生成4.ACCEL_sift_command.txt文件
subprocess.run(["python", "4.ACCEL_sift_code_generator.py"])
subprocess.run(["python", "Resource_monitoring.py 4.ACCEL_sift_command.txt"])
print(datetime.now())
os.chdir(my_path)

# 生成5.prepfold_command.txt文件
subprocess.run(["python", "5.prepfold_code_generator_fit.py"])
subprocess.run(["python", "Resource_monitoring.py 5.prepfold_fit_command.txt"])
print(datetime.now())
os.chdir(my_path)

print("great!")
