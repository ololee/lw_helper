import json
import xml.etree.ElementTree as ET
import csv
import yaml


def parse_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f'解析 JSON 文件 {file_path} 出错: {e}')
        return None


def parse_xml(file_path):
    try:
        tree = ET.parse(file_path)
        return tree.getroot()
    except Exception as e:
        print(f'解析 XML 文件 {file_path} 出错: {e}')
        return None


def parse_csv(file_path):
    data = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f'解析 CSV 文件 {file_path} 出错: {e}')
        return None


def parse_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f'解析 YAML 文件 {file_path} 出错: {e}')
        return None


def read_txt(file_path):
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f'读取文件 {file_path} 出错: {e}')
        return None

class FileParserFactory:
    @staticmethod
    def get_parser(file_path, type = None):
        if file_path.endswith('.json'):
            return parse_json(file_path)
        elif file_path.endswith('.xml'):
            return parse_xml(file_path)
        elif file_path.endswith('.csv'):
            return parse_csv(file_path)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            return parse_yaml(file_path)
        elif file_path.endswith('.txt'):
            return read_txt(file_path)
        else:
            print(f'不支持的文件格式: {file_path}')
            return None