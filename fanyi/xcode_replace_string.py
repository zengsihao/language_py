import os
import xml.etree.ElementTree as ET
import json
import difflib
import json

# 读取 需要替换的 string 文件 R.string.localizable.
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

def replaceSiwftRswift(path,oldpath):
    oldDic = generate_output_files_diffent(oldpath)
    for filepath, dirnames, filenames in os.walk(path):
        # print(dirnames)
        for filename in filenames:
            file_data = ""
            realfilePath = os.path.join(filepath, filename)
            # print(realfilePath)
            if filename[-5:] == 'swift' or filename[-1:] == 'm' :  # 判断文件是否为swift文件
                isSwift = True
                if filename[-5:] == 'swift':
                    isSwift = True
                if filename[-1:] == 'm':
                    isSwift = False
                # print(filename)
                # if filename == 'AppToolUtils.swift':
                #     print(filename)
                with open(realfilePath, 'r') as f:
                    lines = f.readlines()
                    # print("read lines =", lines)
                    for line in lines:
                        # print(line)
                        for key_old, key_xml in oldDic.items():
                            # print(key_old+'=='+key_xml)
                            # print(key_old + key_xml)
                            if "." in key_old:
                                # 如果包含点号，分割字符串并将首字母大写
                                parts = key_old.split(".")
                                new_key = ''
                                for x in range(len(parts)):
                                    if x == 0:
                                        ced_first = ''
                                        for index1 in range(len(parts[x])):
                                            if index1 == 0:
                                                ced_first = parts[x][index1].lower()
                                            else:
                                                ced_first = ced_first + parts[x][index1]
                                        new_key += ced_first
                                    else:
                                        ced = ''
                                        for index in range(len(parts[x])):
                                            if index == 0:
                                                ced = parts[x][index].capitalize()
                                            else:
                                                ced = ced + parts[x][index]
                                        new_key += ced
                                    # print(parts[x])
                                # swift 替换
                                # replaced_swift_output[key] = new_key
                                # if key_xml == 'em_login_password_hint_blank':
                                #     print(key_xml)
                                if isSwift == True:
                                    x_key_old = 'R.string.localizable.' + new_key + '('
                                    s_key_xml = 'R.string.localizable.' + key_xml + '('
                                else:
                                    x_key_old = 'NSLocalizedString(@"%s"' % (key_old)
                                    s_key_xml = 'NSLocalizedString(@"%s"' % (key_xml)
                                # s_key_old = key_old.replace('.', '_')
                                # if new_key == 'transactionGasFeeLabelTitle':
                                #     print("ddddddd====")
                                if x_key_old in line:
                                    line = line.replace(x_key_old, s_key_xml)
                            else:
                                # if key_xml == 'em_login_password_hint_blank':
                                #     print(key_xml)
                                if isSwift == True:
                                    if ' ' in key_old:
                                        kongge_parts = key_old.split(" ")
                                        first_str = ''
                                        for x in range(len(kongge_parts)):
                                            if x == 0:
                                                for index in range(len(kongge_parts[x])):
                                                    if index == 0:
                                                        first_str = kongge_parts[x][index].lower()
                                                    else:
                                                        first_str = first_str + kongge_parts[x][index]
                                            else:
                                                other = ''
                                                for index in range(len(kongge_parts[x])):
                                                    if index == 0:
                                                        other = kongge_parts[x][index].capitalize()
                                                    else:
                                                        other = other + kongge_parts[x][index]
                                                first_str += other
                                        x_key_old = 'R.string.localizable.' + first_str + '('
                                        s_key_xml = 'R.string.localizable.' + key_xml + '('
                                    else:
                                        other_str = ''
                                        for index in range(len(key_old)):
                                            if index == 0:
                                                other_str = key_old[index].lower()
                                            else:
                                                other_str = other_str + key_old[index]
                                        x_key_old = 'R.string.localizable.' + other_str + '('
                                        s_key_xml = 'R.string.localizable.' + key_xml + '('
                                else:
                                    x_key_old = 'NSLocalizedString(@"%s"' % (key_old)
                                    s_key_xml = 'NSLocalizedString(@"%s"' % (key_xml)
                                # x_key_old = 'R.string.localizable.' + key_old
                                # s_key_xml = 'R.string.localizable.' + key_xml
                                if x_key_old in line:
                                    line = line.replace(x_key_old, s_key_xml)
                        file_data += line

                with open(realfilePath, "w", encoding="utf-8") as fw:
                    fw.write(file_data)


def main():
    # 被替换的string key-key_xml
    replaced_output_path = "./fanyi/zhw/ReplaceOldLocalizable.strings"

    print('3')
    # xcode 项目路径
    # file = '/Users/ahao/Documents/language_tools/languageces/languageces/'
    file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/AlphaWallet/'
    # file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/utils/'

    replaceSiwftRswift(file, replaced_output_path)

    print('Done')