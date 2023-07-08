import os
import shutil
from MoveDuplicate import MoveDuplicate

# 定义旧文件夹和新文件夹
old_dir = './old'
new_dir = './new'

# 检查文件夹是否存在
if os.path.exists(new_dir):
    # 删除文件夹及其内容
    shutil.rmtree(new_dir)
    os.makedirs(new_dir)
else:
    os.makedirs(new_dir)

movefile = MoveDuplicate(old_dir, new_dir)
movefile.read_old_files_write_to_new_files()
