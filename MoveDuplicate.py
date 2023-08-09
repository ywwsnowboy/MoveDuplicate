import os
import re


class MoveDuplicate:

    def __init__(self, old_file_path, new_file_path):
        self.old_file_path = old_file_path
        self.new_file_path = new_file_path
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
        for subdir, _, files in os.walk(self.old_file_path):
            len_have_duplicate_dataset = []
            len_no_duplicate_dataset = []
            for file in files:
                if file.endswith('.txt'):
                    textpath = os.path.join(subdir, file)
                    no_duplicate_joint_contents, len_origin, len_no_duplicate = self.move_duplicate_title_data(textpath)
                    len_have_duplicate_dataset.append(len_origin)
                    len_no_duplicate_dataset.append(len_no_duplicate)

                    new_text_path = os.path.join(self.new_file_path, file)
                    # 写入内容到txt文件
                    with open(new_text_path, "w", encoding='utf-8') as w_file:
                        w_file.write(no_duplicate_joint_contents)

                    print(f"{file} in ./old/ folder had been updated and was saved in {self.new_file_path}.")
            print("原始每个文件中的文献数据量:")
            output1 = " ".join(list(map(str, len_have_duplicate_dataset)))
            print(output1)
            print("去重后每个文件中的文献数据量:")
            output2 = " ".join(list(map(str, len_no_duplicate_dataset)))
            print(output2)

