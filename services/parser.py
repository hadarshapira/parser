import re
import csv
import json
import datetime
import os.path as osp
import xml.etree.ElementTree as ET

from typing import *
from services.field import Field
from dateutil import parser as datetime_parser


class UnknownFileExtensionError(Exception):
    pass


class Parser:
    FIELDS_CONFIG_PATH = osp.join(osp.dirname(osp.dirname(__file__)), "configs", "fields_config.json")
    AVAILABLE_FILE_EXTENSIONS = [
        "json",
        "xml",
        "log",
        "csv",
    ]
    FIELDS_TYPES = {
        "String": str,
        "Int": int,
        "Datetime": datetime_parser.parse
    }

    def __init__(self, file_path: str = ""):
        self.file_path = file_path
        self.file_dict = []
        self.headers = self.init_headers()
        self.mandatory_headers = set(header.name for header in self.headers.values() if header.mandatory)

    def init_headers(self) -> Dict[Set, Field]:
        fields_dict = self.json_to_dict(file_path=self.FIELDS_CONFIG_PATH)
        fields = [Field(**field) for field in fields_dict]
        headers = {}
        for field in fields:
            if hasattr(field, "naming_conventions"):
                for name in set(field.naming_conventions):
                    headers[name.lower()] = field
            headers[field.name.lower()] = field
        return headers

    def read_file_to_dict(self) -> List[Dict]:
        file_extension = self.file_path.rsplit(".", 1)[-1]
        if file_extension not in self.AVAILABLE_FILE_EXTENSIONS:
            raise UnknownFileExtensionError(f"The given file have no legal extension to parse, "
                                            f"please make sure your file is one of the following"
                                            f" formats and have valid extension: "
                                            f"{', '.join(self.AVAILABLE_FILE_EXTENSIONS)}")
        self.file_dict = getattr(self, f'{file_extension}_to_dict')(self.file_path)
        return self.file_dict


    def convert_to_single_format(self, dict_to_convert: List[Dict] = None):
        if not dict_to_convert:
            dict_to_convert = self.file_dict
        result = []
        for item in dict_to_convert:
            format_item = {}
            for key, value in item.items():
                header = self.headers.get(key.lower())
                if self._validate_value(header, value):
                    format_item[header.name] = self.FIELDS_TYPES[header.field_type](value)
            missing_headers = []
            for header in self.mandatory_headers:
                if header not in format_item:
                    missing_headers.append(header)
            if missing_headers:
                raise Exception(f"The following mandatory headers are missing: {' '.join(missing_headers)}")
            if format_item:
                result.append(format_item)
        return result


    def _validate_value(self, header, value):
        if not header:
            return False
        if not header.field_type in self.FIELDS_TYPES:
            raise Exception(f"Type: {header.field_type} for header: {header.name},"
                            f" is not valid! Please sure your header config have only valid types: "
                            f"{' or '.join(self.FIELDS_TYPES)}")
        if header.length > 0:
            if len(value) > header.length:
                raise Exception(f"The header {header.name} value,"
                                f" is not valid! the value length: {len(value)} ->"
                                f" the header limit is: {header.length}")
        try:
            self.FIELDS_TYPES[header.field_type](value)
        except Exception as ex:
            raise Exception(f"The header {header.name} value,"
                                f" is not valid! the value can't be casting to the wanted type.\n"
                                f"Expected casting to {header.field_type}, failed on ex: {str(ex)}")



    @staticmethod
    def json_to_dict(file_path: str) -> List[Dict]:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def xml_to_dict(file_path: str) -> List[Dict]:
        tree = ET.parse(file_path)
        root = tree.getroot()
        result = []
        for product_elem in root.findall('product'):
            product_dict = {}
            for child_elem in product_elem:
                product_dict[child_elem.tag] = child_elem.text
            result.append(product_dict)
        return result

    @staticmethod
    def csv_to_dict(file_path: str) -> List[Dict]:
        with open(file_path, 'r', newline='') as csvfile:
            result = list(csv.DictReader(csvfile))
        return result

    @staticmethod
    def log_to_dict(file_path: str) -> List[Dict]:
        result = []
        with open(file_path, 'r') as logfile:
            info_lines = re.findall(r'\[.*?\] INFO: (.*)', logfile.read())
            for info_line in info_lines:
                info_dict = {}
                info_parts = info_line.split('|')
                for part in info_parts:
                    key, value = part.strip().split(':', 1)
                    info_dict[key.strip()] = value.strip()
                result.append(info_dict)
        return result
