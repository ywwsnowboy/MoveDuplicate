########################################################################################################################
# Author: Wangwang Yu
# Email: ywwsnowboy@outlook.com
# Date: 2023/08/18
# Description: 功能根据需要选择
########################################################################################################################

import os
import shutil
from MoveDuplicate import MoveDuplicate
from MoveDuplicate import ExtractFieldTags

# 定义输入文件夹和处理数据后的输出文件夹
input_dir = './input'
output_dir = './output'

# 检查文件夹是否存在
if os.path.exists(output_dir):
    # 删除文件夹及其内容
    shutil.rmtree(output_dir)
    os.makedirs(output_dir)
else:
    os.makedirs(output_dir)

# 以下是所有的功能, 需要进行哪一部分就注释其他部分代码

# 功能一: 根据文献名称移除重复的文献, 不考虑大小写对排除重复文献的影响
move_duplicate_file = MoveDuplicate(input_dir, output_dir)
move_duplicate_file.read_old_files_write_to_new_files()

# 功能二: 提取文献信息中的 SO 信息内容(也就是期刊名称), 并写入 csv 文件中, 便于后续统计分析
extract_field_tag_data = ExtractFieldTags(input_dir, output_dir)
extract_field_tag_data.extract_field_tags_data_write_into_new_csv_files()


