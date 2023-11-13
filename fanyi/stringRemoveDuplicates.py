# string 文件去重 生成新的 string 文件

def readProject(file_path,file_out_path):
    with open(file_path, 'r', encoding='utf-8') as localizable_file:
        lines = localizable_file.readlines()

    key_value_dic = {}

    for line in lines:
        # print(line)
        if '=' in line:
            # key, value = line.strip().split(' = ',1)
            key, value = line.strip().split(' = ', 1)
            value = value.lstrip()
            value = value.rstrip(';\n')
            key = key.strip('"')
            value = value.strip('"')
            key_value_dic[key] = value
    # 清空之后 重新上传
    with open(file_out_path, 'w', encoding='utf-8') as replaced_file:
        for key, value in key_value_dic.items():
            replaced_file.write(f'"{key}" = "{value}";\n')

def main():

    # xcode 多语言文件
    file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/AlphaWallet/Localization/'

    # file_path_en = file + "en.lproj/Localizable.strings"
    file_path_zhw = file + "zh-Hant.lproj/Localizable.strings"

    # 原文件string 去重之后的 新string
    file_path_output_zhw = './fanyi/zhw/Localizable.strings'


    # 写入 去重之后的 新string
    file_data_dic = readProject(file_path_zhw, file_path_output_zhw)

    # 读取xml文件


    print('Done')



