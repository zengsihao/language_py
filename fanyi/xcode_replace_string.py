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
        for filename in filenames:
            file_data = ""
            realfilePath = os.path.join(filepath, filename)
            if filename[-5:] == 'swift' or filename[-1:] == 'm' :  # 判断文件是否为swift文件
                isSwift = True
                if filename[-5:] == 'swift':
                    isSwift = True
                if filename[-1:] == 'm':
                    isSwift = False

                # if filename == 'languageces08ViewController.swift':
                    # print("000000000===")
                with open(realfilePath, 'r') as f:
                    lines = f.readlines()
                    # print("read lines =", lines)
                    for line in lines:
                        # print(line)
                        for key_old, key_xml in oldDic.items():
                            print(key_old+'=='+key_xml)
                            # print(key_old + key_xml)
                            # if key_old == 'transaction.gasFee.label.title':
                            #     print(key_xml)
                            if key_old == 'settings.wallet.rename':
                                print(key_old)
                            if "." in key_old:
                                # 如果包含点号，分割字符串并将首字母大写
                                # if key_old == "transaction.gasFee.label.title":
                                    # print("aaaaaaaa====")
                                # if key_old == 'send.error.emptyClipBoard':
                                #     print(key_old)
                                parts = key_old.split(".")
                                new_key = ''
                                for x in range(len(parts)):
                                    if x == 0:
                                        new_key = parts[x]
                                    else:
                                        ced = ''
                                        for index in range(len(parts[x])):
                                            if index == 0:
                                                ced = parts[x][index].capitalize()
                                            else:
                                                ced = ced + parts[x][index]
                                        new_key += ced
                                    # print(parts[x])
                                # new_key = parts[0] + ''.join(word.capitalize() for word in parts[1:])
                                # swift 替换
                                # replaced_swift_output[key] = new_key
                                if key_xml == 'em_login_password_hint_blank':
                                    print(key_xml)
                                if isSwift == True:
                                    x_key_old = 'R.string.localizable.' + new_key
                                    s_key_xml = 'R.string.localizable.' + key_xml
                                else:
                                    x_key_old = 'NSLocalizedString(@"%s" ' % (key_old)
                                    s_key_xml = 'NSLocalizedString(@"%s"' % (key_xml)
                                # s_key_old = key_old.replace('.', '_')
                                # if new_key == 'transactionGasFeeLabelTitle':
                                #     print("ddddddd====")
                                if x_key_old in line:
                                    line = line.replace(x_key_old, s_key_xml)
                            else:
                                if key_xml == 'em_login_password_hint_blank':
                                    print(key_xml)
                                if isSwift == True:
                                    x_key_old = 'R.string.localizable.' + key_old
                                    s_key_xml = 'R.string.localizable.' + key_xml
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


    # xcode 项目路径
    # file = '/Users/ahao/Documents/language_tools/languageces/languageces/'
    file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/AlphaWallet/'

    replaceSiwftRswift(file, replaced_output_path)

    print('Done')