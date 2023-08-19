import os
import re
import csv


class MoveDuplicate:

    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.duplicate_paper_title = []  # 重复的文献标题全部用小写表示
        self.new_pt_er = []

    def move_duplicate_title_data(self, textpath):
        with open(textpath, 'r', encoding='utf-8') as f:
            content = f.read()
            pattern_title = r'\nTI (.*?)\nSO '  # 使用非贪婪匹配，提取每个 TI 的内容
            matches_title = re.findall(pattern_title, content, re.DOTALL)
            pattern_pt_er = r'PT J\n.*?\nER\n'  # 使用非贪婪匹配，提取每对 PT 和 ER 之间的内容
            matches_pt_er = re.findall(pattern_pt_er, content, re.DOTALL)
            len_origin = len(matches_title)
            unique_strings = []  # 存放不重复的字符串
            unique_lower_strings = []  # 存放不重复的字符串的所有小写形式
            unique_strings_index = []  # 存放不重复的字符串在content中的顺序
            for index_match, string in enumerate(matches_title):
                search_string_lower = string.lower()  # 将字符转换成小写字符
                if index_match == 0 or \
                        (index_match > 0 and (search_string_lower not in unique_lower_strings)):
                    # 第一个不需要检测是否重复，直接添加进来即可,后续的字符串也不存在重复，并且是WOS数据库的数据，则将其替换为
                    unique_strings.append(string)
                    unique_lower_strings.append(search_string_lower)
                    unique_strings_index.append(index_match)
                else:
                    if index_match > 0 and (search_string_lower in unique_lower_strings):
                        # 这里是除了第一个的字符串,存在重复的文献标题
                        index_in_duplicate_string_unique_strings = unique_lower_strings.index(search_string_lower)
                        #  index_in_duplicate_string_unique_strings 为当前的字符串在unique_lower_strings中的序号
                        self.duplicate_paper_title.append(search_string_lower)  # 保存重复的字符串，这里是小写字符串
                        string_wos = 'UT WOS:'
                        if string_wos in matches_pt_er[index_match]:
                            unique_strings_index[index_in_duplicate_string_unique_strings] = index_match
        no_duplicate_no_joint_content = []
        for index_unique_strings_index in unique_strings_index:
            no_duplicate_no_joint_content.append(matches_pt_er[index_unique_strings_index])
        no_duplicate_contents = "\n".join(no_duplicate_no_joint_content)
        len_no_duplicate = len(unique_strings_index)
        return no_duplicate_contents, len_origin, len_no_duplicate

    def read_old_files_write_to_new_files(self):
        for subdir, _, files in os.walk(self.input_file_path):
            len_have_duplicate_dataset = []
            len_no_duplicate_dataset = []
            for file in files:
                if file.endswith('.txt'):
                    textpath = os.path.join(subdir, file)
                    no_duplicate_joint_contents, len_origin, len_no_duplicate = self.move_duplicate_title_data(textpath)
                    len_have_duplicate_dataset.append(len_origin)
                    len_no_duplicate_dataset.append(len_no_duplicate)

                    new_text_path = os.path.join(self.output_file_path, file)
                    # 写入内容到txt文件
                    with open(new_text_path, "w", encoding='utf-8') as w_file:
                        w_file.write(no_duplicate_joint_contents)

                    print(f"{file} in ./old/ folder had been updated and was saved in {self.output_file_path}.")
            print("原始每个文件中的文献数据量:")
            output1 = " ".join(list(map(str, len_have_duplicate_dataset)))
            print(output1)
            print("去重后每个文件中的文献数据量:")
            output2 = " ".join(list(map(str, len_no_duplicate_dataset)))
            print(output2)


class ExtractFieldTags:
    def __init__(self, input_file_path, output_file_path):
        self.all_publication_name = []
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def split_single_field_tag(self, textpath):
        with open(textpath, 'r', encoding='utf-8') as f:
            content = f.read()
            pattern_pt_er = r'PT J\n.*?\nER\n'  # 使用非贪婪匹配，提取每对 PT 和 ER 之间的内容
            split_all_paper_information = re.findall(pattern_pt_er, content, re.DOTALL)
            for single_paper_information in split_all_paper_information:
                pattern_publication_name = r'\nSO (.*?)\nLA '  # 使用非贪婪匹配，提取每个 SO 的内容
                matched_publication_name = re.findall(pattern_publication_name,
                                                      single_paper_information,
                                                      re.DOTALL)
                self.all_publication_name.append(matched_publication_name)

    def extract_field_tags_data_write_into_new_csv_files(self):
        for subdir, _, files in os.walk(self.input_file_path):
            for file in files:
                if file.endswith('.txt'):
                    textpath = os.path.join(subdir, file)
                    self.split_single_field_tag(textpath)

        ################################################################
        # 统计期刊名称，这部分代码写法一
        no_duplicate_publication_name = []
        no_duplicate_publication_count = []
        index_pub = 0
        for publication_name in self.all_publication_name:
            if index_pub == 0:
                index_pub += 1
                no_duplicate_publication_name.append(publication_name)
                no_duplicate_publication_count.append(1)
            else:
                if publication_name in no_duplicate_publication_name:
                    index_no_duplicate = no_duplicate_publication_name.index(publication_name)
                    no_duplicate_publication_count[index_no_duplicate] += 1
                else:
                    no_duplicate_publication_name.append(publication_name)
                    no_duplicate_publication_count.append(1)

        # 拼接文件路径
        output_file_path = os.path.join(self.output_file_path, 'output.csv')
        # 指定要写入的文件名

        # 将两个列表合并为一个列表的列表，每个子列表代表一行
        data = list(zip(no_duplicate_publication_name, no_duplicate_publication_count))

        # 使用CSV模块写入CSV文件
        with open(output_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Column A', 'Column B'])  # 写入标题行
            writer.writerows(data)  # 写入数据行

        print("数据已写入CSV文件。")

        # 上面的用分割线隔开的代码可以用下面的注释代码替换
        ################################################################
        # 统计期刊名称，这部分代码写法二，和上述代码一样，不过这里使用字典来进行字符计数
        # all_publication_name_count = {}
        # for string_name in all_publication_name:
        #     if tuple(string_name) in all_publication_name_count:
        #         all_publication_name_count[tuple(string_name)] += 1
        #     else:
        #         all_publication_name_count[tuple(string_name)] = 1
        #
        # # # 拼接文件路径
        # output_file_path = os.path.join(self.output_file_path, 'output.csv')
        #
        # # 打开CSV文件以写入模式
        # with open(output_file_path, 'w', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #
        #     # 写入表头
        #     writer.writerow(['Name', 'times'])
        #
        #     # 写入数据行
        #     for name, count in all_publication_name_count.items():
        #         writer.writerow([name, count])
        #
        # print("数据已写入CSV文件。")
        ################################################################
