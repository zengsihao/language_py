
import xml.etree.ElementTree as ET
import json
import difflib
import json
import re
import os


def generate_output_files_diffent(different_xml_path):

    # with open(different_xml_path, 'r', encoding='utf-8') as localizable_file:
    #     lines = localizable_file.readlines()
    key_value_pairs = {
        "key1": "value1",
        "key3": "value3"
    }
    # 清空 重新写入
    with open(different_xml_path, 'w', encoding='utf-8') as different_new_file:
        for key, value in key_value_pairs.items():
            different_new_file.write(f'"{key}" = "{value}";\n')


#  追加
def generate_output_files_diffent_in(different_xml_path):

    # with open(different_xml_path, 'r', encoding='utf-8') as localizable_file:
    #     lines = localizable_file.readlines()
    key_value_pairs = {
        "key1": "value1",
        "key2": "value2",
        "key2d": "value442",
        "key3": "value3"
    }
    with open(different_xml_path, 'a', encoding='utf-8') as different_new_file:
        # different_new_file.write(f'追加====\n')
        for key, value in key_value_pairs.items():
            different_new_file.write(f'"{key}" = "{value}";\n')

if __name__ == '__main__':

    # 剩余没有匹配上的xml
    different_xml_path = "./cesLocalizable.strings"

    generate_output_files_diffent(different_xml_path)

    # generate_output_files_diffent_in(different_xml_path)