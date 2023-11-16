import xml.etree.ElementTree as ET
import json
import difflib
import json
import re

# 在没有被替换的文件里面 继续筛选 然后写入到替换后的文件里面

#  获取字符串里面的 %@ 有多少个
def get_special_characters_pattern(str):
    # 定义正则表达式，这里以匹配标点符号为例
    special_characters_pattern = re.compile(r'[%@]')
    # 使用正则表达式查找特殊符号
    matches = special_characters_pattern.findall(str)
    # 计算特殊符号的数量
    count_special_characters = len(matches)
    return count_special_characters

def generate_output_files_diffent(different_xml_path,different_string_path,rate,replace_output_path,replace_old_output_path,replace_old_key_value_output_path):

    with open(different_xml_path, 'r', encoding='utf-8') as localizable_file:
        xmllines = localizable_file.readlines()


    with open(different_string_path, 'r', encoding='utf-8') as diflocalizable_file:
        stringlines = diflocalizable_file.readlines()

    xml_lines = {}

    # 被替换的 旧的 key-value
    replaced_key_value_output = {}
    # 被替换的 旧的 key-key_xml
    replaced_key_xml_output = {}

    string_lines = {}

    for line in xmllines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            xml_lines[key] = value

    for line in stringlines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            string_lines[key] = value

    rate_diffent_output = {}
    rate_new_output = {}
    rate_string = {}
    for key_string, value_string in string_lines.items():
        for key_xml, value_xml in xml_lines.items():

            first_two_characters_string = value_string[:3]
            last_two_characters_string = value_string[-3:]

            first_two_characters_xml = value_xml[:3]
            last_two_characters_xml = value_xml[-3:]

            if first_two_characters_string == first_two_characters_xml and last_two_characters_string == last_two_characters_xml:
                print(
                    f"Similar strings found: '{value_string}' and '{value_xml}' with a similarity of ")

            similarity = difflib.SequenceMatcher(None, value_string, value_xml).ratio()
            if similarity >= rate:
                # print(f"Similar strings found: '{value_string}' and '{value_xml}' with a similarity of {similarity:.2f}")
                # different_new_file.write(f'"{key},{value}" = "{value_xml},{key_xml}";\n')
                key_new = f'{key_string},{value_string}'
                value_new = f'{value_xml},{key_xml}'

                first_two_characters_string = value_string[:2]
                last_two_characters_string = value_string[-2:]

                first_two_characters_xml = value_xml[:2]
                last_two_characters_xml = value_xml[-2:]

                if first_two_characters_string == first_two_characters_xml and last_two_characters_string == last_two_characters_xml:
                    # print('筛选后===')
                    #  因为xml 里面有多个相同的 value 所以 会导致  rate_string 和 rate_new_output 不一致
                    if get_special_characters_pattern(value_string) == get_special_characters_pattern(value_xml):
                        # print(
                        #     f"Similar strings found: '{value_string}' and '{value_xml}' with a similarity of {similarity:.2f}")
                        # print(
                        #     f"Similar strings found: '{key_xml}' and '{key_string}' with a similarity of {similarity:.2f}")
                        rate_new_output[key_xml] = value_xml
                        rate_string[key_string] = value_string
                        replaced_key_xml_output[key_string] = key_xml
                        replaced_key_value_output[key_string] = value_string

    diffent_new_string = {}
    # 更新xml 里面不同的diffent 文件
    diffent_xml = {}
    for key_xml, value_xml in xml_lines.items():
        if key_xml not in rate_new_output.keys():
            diffent_xml[key_xml] = value_xml

    # 更新string 里面不同的diffent 文件
    for key_string, value_string in string_lines.items():
        if key_string not in rate_string.keys():
            diffent_new_string[key_string] = value_string

    # 文件写入
    # 追加进入到已经替换的文件里面 追加
    with open(replace_output_path, 'a', encoding='utf-8') as different_new_file:
        # different_new_file.write(f'"zhuijia" = "--------追加不同的--{rate}-";\n')
        for key, value in rate_new_output.items():
            different_new_file.write(f'"{key}" = "{value}";\n')

    # 追加进入被替换的文件 key - xml_key
    with open(replace_old_output_path, 'a', encoding='utf-8') as replaced_key_xml_file:
        # replaced_key_xml_file.write(f'"zhuijia" = "--------追加不同的--{rate}-";\n')
        for key, value in replaced_key_xml_output.items():
            replaced_key_xml_file.write(f'"{key}" = "{value}";\n')

    # 追加进入到被替换的文件 key - value
    with open(replace_old_key_value_output_path, 'a', encoding='utf-8') as replaced_file:
        # replaced_file.write(f'"zhuijia" = "--------追加不同的--{rate}-";\n')
        for key, value in replaced_key_value_output.items():
            replaced_file.write(f'"{key}" = "{value}";\n')


    # 更新string 里面没有被替换的文件
    with open(different_string_path, 'w', encoding='utf-8') as different_file:
        for key, value in diffent_new_string.items():
            different_file.write(f'"{key}" = "{value}";\n')

    # 更新xml 里面没有被替换的文件
    with open(different_xml_path, 'w', encoding='utf-8') as different_xml_file:
        for key, value in diffent_xml.items():
            different_xml_file.write(f'"{key}" = "{value}";\n')

if __name__ == '__main__':

    print('rate == start')
    different_xml_path = "./xml/zhw/DifferentLocalizable.strings"  # 剩余没有匹配上的xml

    replace_output_path = "./fanyi/zhw/ReplaceLocalizable.strings"  # 替换后的文件路径

    replace_old_output_path = "./fanyi/zhw/ReplaceOldLocalizable.strings"  # 被替换的文件路径 key-xml_key
    replace_old_output_key_value_path = "./fanyi/zhw/ReplaceOldKeyValueLocalizable.strings"  # 被替换的文件路径 key-value

    rate = 0.7

    different_string_path = "./fanyi/zhw/DifferentLocalizable.strings"  # 剩余不同的文件路径

    generate_output_files_diffent(different_xml_path, different_string_path, rate, replace_output_path,replace_old_output_path,replace_old_output_key_value_path)

    print('Done')