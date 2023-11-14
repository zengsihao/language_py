import xml.etree.ElementTree as ET
import json
import difflib
import json

# 解析 XML 文件并生成字典
def parse_xml_to_dict(xml_file_path):
    data = {}
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        for string_element in root.findall(".//string"):
            name = string_element.get("name")
            value = string_element.text
            # name = '"' + name + '"'
            # value = '"' + value + '"'
            if value == None:
                continue
            #  替换占位符
            value = value.replace("%1$s","%@")
            value = value.replace("%2$", "%@")
            value = value.replace("%2$s", "%@")
            value = value.replace("%3$s", "%@")
            value = value.replace("%4$s", "%@")
            value = value.replace("%s", "%@")

            value = value.replace("%1$d", "%@")
            value = value.replace("%2$d", "%@")
            value = value.replace("%3$d", "%@")
            value = value.replace("%d", "%@")
            if name == 'select_receive_group_hint':
                print(name)
            if r'\"' not in value:
                value = value.replace('"', r'\"')

            data[name] = value
    except FileNotFoundError:
        print(f"XML文件 '{xml_file_path}' 未找到")
    except Exception as e:
        print(f"解析 XML 文件时出错：{e}")
    return data

# 生成不同的 Localizable.strings 文件
def generate_output_files(xml_file_path, string_path, replace_output_path, different_output_path, replace_old_output_path, replace_old_key_value_output_path,different_xml_output_path):
    xml_data_old = parse_xml_to_dict(xml_file_path)
    xml_data = {}
    xml_data_old_02 = {}
    for key_xml_old,value_xml_old in xml_data_old.items():
        xml_data_old_02[value_xml_old] = key_xml_old
    for key_xml_old_02, value_xml_old_02 in xml_data_old_02.items():
        xml_data[value_xml_old_02] = key_xml_old_02

    with open(string_path, 'r', encoding='utf-8') as localizable_file:
        lines = localizable_file.readlines()

    replace_output = {}
    # 被替换的 旧的 key-key_xml
    replaced_key_xml_output = {}
    # 被替换的 旧的 key-value
    replaced_key_value_output = {}

    different_output = {}

    different_xml_output = {}

    replace_temp = []
    replace_temp_congfu = []
    for line in lines:
        if '=' in line:
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')

            if key in replace_temp:
                replace_temp_congfu.append(key)
                continue
            replace_temp.append(value)

            if key == '"presale.tips"':
                print(key)
            if value in xml_data.values():
                for key_xml, value_xml in xml_data.items():
                    if value == value_xml:
                        replace_output[key_xml] = value
                        replaced_key_xml_output[key] = key_xml
                        replaced_key_value_output[key] = value
            else:
                if value == '知道了':
                    print(key)
                different_output[key] = value

    for key_xml, value_xml in xml_data.items():
        if key_xml not in replaced_key_xml_output.values():
           # print('在xml里面没有被替换')
           different_xml_output[key_xml] = value_xml

    # 没有被替换的 xml里面的key
    with open(different_xml_output_path, 'w', encoding='utf-8') as replaced_file:
        for key, value in different_xml_output.items():
            replaced_file.write(f'"{key}" = "{value}";\n')


    # 被替换的文件 key - xml_key
    with open(replace_old_output_path, 'w', encoding='utf-8') as replaced_file:
        for key, value in replaced_key_xml_output.items():
            replaced_file.write(f'"{key}" = "{value}";\n')

    # 被替换的文件 key - value
    with open(replace_old_key_value_output_path, 'w', encoding='utf-8') as replaced_file:
        for key, value in replaced_key_value_output.items():
            replaced_file.write(f'"{key}" = "{value}";\n')

    # 替换后的文件
    with open(replace_output_path, 'w', encoding='utf-8') as replace_file:
        for key, value in replace_output.items():
            replace_file.write(f'"{key}" = "{value}";\n')

    # 不同的文件
    with open(different_output_path, 'w', encoding='utf-8') as different_file:
        for key, value in different_output.items():
            different_file.write(f'"{key}" = "{value}";\n')
    print('重复的key----')
    print(replace_temp_congfu)
    print('----++')

def main():

    # xml 路径
    xml_file_path_zhw = "./xml/zhw/strings.xml"
    # 剩余没有匹配上的xml
    different_xml_output_path = "./xml/zhw/DifferentLocalizable.strings"


    # xcode 里面的晒过去重的 string 文件
    string_path = "./fanyi/zhw/Localizable.strings"

    replace_output_path = "./fanyi/zhw/ReplaceLocalizable.strings"  # 替换后的文件路径
    different_output_path = "./fanyi/zhw/DifferentLocalizable.strings"  # 剩余不同的文件路径

    replace_old_output_path = "./fanyi/zhw/ReplaceOldLocalizable.strings"  # 被替换的文件路径 key-xml_key
    replace_old_output_key_value_path = "./fanyi/zhw/ReplaceOldKeyValueLocalizable.strings"  # 被替换的文件路径 key-value


    generate_output_files(xml_file_path_zhw, string_path, replace_output_path, different_output_path,replace_old_output_path,replace_old_output_key_value_path,different_xml_output_path)

    # 查看被替换的文件然后修改xcode里面的 R.string.localizable.


    print('Done')

