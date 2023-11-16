
import os
import xml.etree.ElementTree as ET
import json
import difflib
import json

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


def generate_output_files_diffent(different_output_path):
    with open(different_output_path, 'r', encoding='utf-8') as localizable_file:
        lines = localizable_file.readlines()

    replaced_new_output = {}
    for line in lines:
        if '=' in line:
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')

            key = key.strip('"')
            value = value.strip('"')
            replaced_new_output[key] = value
    return replaced_new_output

def replaceSting(path,oldpath):

    xml_data = parse_xml_to_dict(path)

    oldDic = generate_output_files_diffent(oldpath)

    replace = {}
    diffent = {}
    for key_string,value_string in oldDic.items():
        if key_string in xml_data.keys():
            replace[key_string] = value_string
        else:
            diffent[key_string] = value_string

    # 更新string 里面被替换的文件
    with open(oldpath, 'w', encoding='utf-8') as xcode_file:
        for key, value in replace.items():
            xcode_file.write(f'"{key}" = "{value}";\n')

    # 文件写入
    # 追加进入到已经替换的文件里面后面 追加
    with open(oldpath, 'a', encoding='utf-8') as different_new_file:
        different_new_file.write(f'"zhuijia" = "--------追加不同的---";\n')
        for key, value in diffent.items():
            different_new_file.write(f'"{key}" = "{value}";\n')



if __name__ == '__main__':
    # xcode 多语言文件
    file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/AlphaWallet/Localization/'

    xml_file = '/Users/ahao/Downloads/xml_android/'


    xml_zw_file = xml_file + 'values-zh-rTW//strings.xml'

    other_path_language_string = [
        "{}en.lproj/Localizable.strings".format(file),
       "{}fr.lproj/Localizable.strings".format(file),
       "{}ja.lproj/Localizable.strings".format(file),
    "{}ko.lproj/Localizable.strings".format(file),
    "{}pt-PT.lproj/Localizable.strings".format(file),
    "{}ru.lproj/Localizable.strings".format(file),
    "{}tr.lproj/Localizable.strings".format(file),
    "{}vi.lproj/Localizable.strings".format(file),
    "{}de.lproj/Localizable.strings".format(file),
    "{}zh-Hans.lproj/Localizable.strings".format(file),
        "{}zh-Hant.lproj/Localizable.strings".format(file),
    "{}es.lproj/Localizable.strings".format(file),
    ]



    for i in range(len(other_path_language_string)):
        value = other_path_language_string[i]
        replaceSting(xml_zw_file, value)