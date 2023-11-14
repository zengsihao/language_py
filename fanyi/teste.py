

def readProject(file_path):
    with open(file_path, 'r', encoding='utf-8') as localizable_file:
        lines = localizable_file.readlines()

    key_value_dic = {}
    temp = []
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
            if key in temp:
                print(key)
            temp.append(key)

    return key_value_dic

def readProjectbijiao(file_path_zw,file_path_en):
    zw_data = readProject(file_path_zw)
    en_data = readProject(file_path_en)
    for key_zw,value_zw in zw_data.items():
        if key_zw not in en_data.keys():
            print(key_zw)
            print(value_zw)


if __name__ == '__main__':
    # xcode 多语言文件
    file = '/Users/ahao/Documents/INTO/NewCode/IosInto/alpha-wallet-ios/AlphaWallet/Localization/'

    file_path_en = file + "en.lproj/Localizable.strings"
    file_path_zhw = file + "zh-Hant.lproj/Localizable.strings"

    readProjectbijiao(file_path_zhw, file_path_en)
