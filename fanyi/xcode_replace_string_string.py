
import xml.etree.ElementTree as ET
import json
import difflib
import json
import re

# 上面生成的新string 替换 xcode 里面的多语言 string文件、 已经替换的和不同的放在一个文件里面

def generate_output_files_diffent(different_string_path,replace_output_path,file_path_zhw):

    with open(replace_output_path, 'r', encoding='utf-8') as replacelocalizable_file:
        replacestringlines = replacelocalizable_file.readlines()

    with open(different_string_path, 'r', encoding='utf-8') as diflocalizable_file:
        diffentstringlines = diflocalizable_file.readlines()

    replace_lines = {}
    diffent_lines = {}

    for line in replacestringlines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            replace_lines[key] = value

    for line in diffentstringlines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            diffent_lines[key] = value

    # 更新string 里面被替换的文件
    with open(file_path_zhw, 'w', encoding='utf-8') as xcode_file:
        for key, value in replace_lines.items():
            xcode_file.write(f'"{key}" = "{value}";\n')

    # 文件写入
    # 追加进入到已经替换的文件里面 追加
    with open(file_path_zhw, 'a', encoding='utf-8') as different_new_file:
        different_new_file.write(f'"zhuijia" = "--------追加不同的---";\n')
        for key, value in diffent_lines.items():
            different_new_file.write(f'"{key}" = "{value}";\n')


# 读取 xml
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
                print(value)
                print(name)
            if r'\"' not in value:
                value = value.replace('"', r'\"')


            data[name] = value
    except FileNotFoundError:
        print(f"XML文件 '{xml_file_path}' 未找到")
    except Exception as e:
        print(f"解析 XML 文件时出错：{e}")
    return data

def get_special_characters_pattern(str):
    # 定义正则表达式，这里以匹配标点符号为例
    special_characters_pattern = re.compile(r'[%@]')
    # 使用正则表达式查找特殊符号
    matches = special_characters_pattern.findall(str)
    # 计算特殊符号的数量
    count_special_characters = len(matches)
    return count_special_characters

# 根据 xml 替换 string 其他语言
def generate_other_language_output_files_diffent(replace_old_output_path ,xml_file_path, string_file_path,file_path_zhw):
    xml_data_old = parse_xml_to_dict(xml_file_path)
    xml_data = {}
    xml_data_old_02 = {}
    # 去重
    for key_xml_old, value_xml_old in xml_data_old.items():
        xml_data_old_02[value_xml_old] = key_xml_old
    for key_xml_old_02, value_xml_old_02 in xml_data_old_02.items():
        xml_data[value_xml_old_02] = key_xml_old_02

    with open(replace_old_output_path, 'r', encoding='utf-8') as replacelocalizable_file:
        replacestringlines = replacelocalizable_file.readlines()

    with open(file_path_zhw, 'r', encoding='utf-8') as zwlocalizable_file:
        zwstringlines = zwlocalizable_file.readlines()

    with open(string_file_path, 'r', encoding='utf-8') as stringlocalizable_file:
        stringlines = stringlocalizable_file.readlines()

    replace_lines = {}
    string_lines = {}

    zw_lines = {}

    for line in zwstringlines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            zw_lines[key] = value

    for line in replacestringlines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            replace_lines[key] = value

    # xcode 多语言 string
    for line in stringlines:
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            string_lines[key] = value



    # 替换其他语言的 key-vslue
    # replace_other_language_lines = {}
    # replace_old_language_lines = {}
    # different_other_language_lines = {}

    replace_other_language = {}

    diffent_other_language = {}

    # 已经替换好的繁体文件
    for key_string_zw, value_zw in zw_lines.items():
        if key_string_zw == 'know':
            print(value_zw)
        if key_string_zw in replace_lines.values():
           # temp_value = replace_lines[key_string_zw]
           # replace_other_language[temp_value] = value_zw
           temArr = []
           for key_re,value_re in replace_lines.items():
               if value_re == key_string_zw and value_re not in temArr:
                   temArr.append(value_re)
                   for key_string_other, value_string_other in string_lines.items():
                       if key_string_other == key_re:
                           replace_other_language[value_re] = value_string_other
        else:
            for key_string_other_dif,value_string_other_dif in string_lines.items():
                if key_string_zw == 'know':
                    print(value_zw)
                if key_string_zw not in replace_lines.values() and key_string_zw == key_string_other_dif:
                    diffent_other_language[key_string_zw] = value_string_other_dif

    # for key_string_xcode, value_xcode in string_lines.items():
    #     for key_string, key_xml in replace_lines.items():
    #         if key_string == key_string_xcode:
    #             print(f'"{key_string}" = "{key_xml}";\n')
    #             replace_other_language_lines[key_xml] = value_xcode
    #             replace_old_language_lines[key_string] = value_xcode
    # for key_string,value_string in replace_lines.items():
    #     for key_xml, value_xml in xml_data.items():
    #         if key_string == key_xml:
    #            # 如果占位符是一样的多
    #            if get_special_characters_pattern(value_xml) == get_special_characters_pattern(value_string):
    #                replace_other_language_lines[key_xml] = value_xml
    #            else:
    #                print('占位符号不一样')
    #                print(f'"{key_xml}" = "{value_xml}";\n')
    #                print('占位符号不一样')

    # for key_str, value_str in string_lines.items():
    #     for key_replace in replace_old_language_lines.keys():
    #         if key_str != key_replace:
    #             different_other_language_lines[key_str] = value_str

    # 更新string 里面被替换的文件
    with open(string_file_path, 'w', encoding='utf-8') as xcode_file:
        for key, value in replace_other_language.items():
            xcode_file.write(f'"{key}" = "{value}";\n')

    # 文件写入
    # 追加进入到已经替换的文件里面后面 追加
    with open(string_file_path, 'a', encoding='utf-8') as different_new_file:
        different_new_file.write(f'"zhuijia" = "--------追加不同的---";\n')
        for key, value in diffent_other_language.items():
            different_new_file.write(f'"{key}" = "{value}";\n')




def main():

    # xcode 多语言文件
    file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/AlphaWallet/Localization/'

    # file_path_en = file + "en.lproj/Localizable.strings"
    file_path_zhw = file + "zh-Hant.lproj/Localizable.strings"

    replace_output_path = "./fanyi/zhw/ReplaceLocalizable.strings"  # 替换后的文件路径

    replace_old_output_path = "./fanyi/zhw/ReplaceOldLocalizable.strings"  # 被替换的文件路径 key-xml_key

    different_string_path = "./fanyi/zhw/DifferentLocalizable.strings"  # 剩余不同的文件路径

    #  替换繁体
    generate_output_files_diffent(different_string_path, replace_output_path, file_path_zhw)


    xml_file = '/Users/ahao/Downloads/xml_android/'
    other_path_languages = {
        "{}values/strings.xml".format(xml_file): "{}en.lproj/Localizable.strings".format(file),
        "{}values-fr/strings.xml".format(xml_file): "{}fr.lproj/Localizable.strings".format(file),
        "{}values-ja/strings.xml".format(xml_file): "{}ja.lproj/Localizable.strings".format(file),
        "{}values-ko/strings.xml".format(xml_file): "{}ko.lproj/Localizable.strings".format(file),
        "{}values-pt/strings.xml".format(xml_file): "{}pt-PT.lproj/Localizable.strings".format(file),
        "{}values-ru/strings.xml".format(xml_file): "{}ru.lproj/Localizable.strings".format(file),
        "{}values-tr/strings.xml".format(xml_file): "{}tr.lproj/Localizable.strings".format(file),
        "{}values-vi/strings.xml".format(xml_file): "{}vi.lproj/Localizable.strings".format(file),
    }

    for key, value in other_path_languages.items():
        #  替换其他国家语言
        generate_other_language_output_files_diffent(replace_old_output_path, key,
                                                     value,file_path_zhw)

    print('Done')