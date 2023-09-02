import os
import re
import csv
import json
import datetime
import functools

from typing import *
from logging import Logger
from services.field import Field
from xml.etree import ElementTree
from services import fields_config
from services.logger_helper import init_logger
from dateutil import parser as datetime_parser


def json_serial(obj: datetime.datetime) -> str:
    if isinstance(obj, datetime.datetime):
        return obj.isoformat(sep=" ", timespec="seconds")
    raise TypeError(f"Type {type(obj)} not serializable")


def exception_wrapper(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            raise Exception(f"Exception catch when calling '{func.__name__}':\n{ex}") from ex
    return func_wrapper


class Parser:
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
    HEADERS = "headers"
    DYNAMIC = "dynamic"

    def __init__(self, config: str = None, logger: Logger = None):
        self.logger = logger if logger else init_logger()
        self.fields = []
        self.dynamic_data_keys = set()
        self.headers = self.init_headers(config=config)
        self.mandatory_headers = set(header.name for header in self.headers.values() if header.mandatory)

    def init_headers(self, config: str) -> Dict[str, Field]:
        if config:
            fields_dict = self.json_to_dict(file_path=config)
        else:
            fields_dict = fields_config.fields_dict
        self.fields.extend([Field(**field) for field in fields_dict])
        headers = {}
        for field in self.fields:
            if hasattr(field, "naming_conventions"):
                for name in set(field.naming_conventions):
                    headers[name.lower()] = field
            headers[field.name.lower()] = field
        return headers

    def parse(self, file_path: str = "") -> List[Dict]:
        file_dict = self._read_file_to_dict(file_path=file_path)
        return self._convert_to_single_format(
            file_path=file_path,
            file_dict=file_dict,
        )

    def _read_file_to_dict(self, file_path: str = "") -> List[Dict]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File: {file_path}, doesn't exist, please check your input")
        if not os.path.isfile(file_path):
            raise IsADirectoryError(f"File: {file_path}, is a directory, please check your input")
        self.logger.debug("Extracting file content to dict")
        file_extension = file_path.rsplit(".", 1)[-1]
        self.logger.debug(f"File extension: {file_extension}")
        if file_extension not in self.AVAILABLE_FILE_EXTENSIONS:
            raise Exception(f"The given file have no legal extension to parse, "
                            f"please make sure your file is one of the following"
                            f" formats and have valid extension: "
                            f"{', '.join(self.AVAILABLE_FILE_EXTENSIONS)}")
        return getattr(self, f'{file_extension}_to_dict')(file_path)

    def _convert_to_single_format(self, file_path: str = "", file_dict: List[Dict] = None) -> List[Dict]:
        file_dict = file_dict if file_dict else {}
        source_type = file_path.split(".", 1)[-1]
        result = []
        for item in file_dict:
            format_item = self._convert_single_item_to_single_format(
                file_path=file_path,
                item=item,
                source_type=source_type
            )
            if format_item is False:
                continue
            if not self._check_if_missing_mandatory_headers(format_item=format_item):
                continue
            result.append(format_item)
        return result

    def _convert_single_item_to_single_format(self, file_path: str, item: Dict, source_type: str) -> [Dict, bool]:
        format_item = {self.HEADERS: {}, self.DYNAMIC: {}}
        for key, value in item.items():
            header = self.headers.get(key.lower())
            if not header:
                format_item[self.DYNAMIC][key] = value
                self.dynamic_data_keys.add(key)
                continue
            if not self._validate_value(header, value):
                return False
            format_item[self.HEADERS][header.name] = self.FIELDS_TYPES[header.field_type](value)
        format_item = self._add_source_type_and_file(
            file_path=file_path,
            format_item=format_item,
            source_type=source_type
        )
        return format_item

    def _add_source_type_and_file(self, file_path: str, format_item: Dict, source_type: str) -> Dict:
        header = self.headers.get("source_type")
        if self._validate_value(header, source_type):
            format_item[self.HEADERS][header.name] = self.FIELDS_TYPES[header.field_type](source_type)
        header = self.headers.get("source_file")
        if self._validate_value(header, file_path):
            format_item[self.HEADERS][header.name] = self.FIELDS_TYPES[header.field_type](file_path)
        return format_item

    def _check_if_missing_mandatory_headers(self, format_item: Dict) -> bool:
        missing_headers = []
        for header in self.mandatory_headers:
            if header not in format_item[self.HEADERS]:
                missing_headers.append(header)
        if missing_headers:
            self.logger.debug(json.dumps(format_item[self.HEADERS], indent=4, default=json_serial))
            self.logger.warning(f"The following mandatory headers are missing:"
                                f" {' '.join(missing_headers)}, skipping item")
            return False
        return True

    def _validate_value(self, header: Field, value: str) -> bool:
        if header.field_type not in self.FIELDS_TYPES:
            self.logger.warning(f"Type: {header.field_type} for header: {header.name},"
                                f" is not valid! Please sure your header config have only valid types: "
                                f"{' or '.join(self.FIELDS_TYPES)}, skipping item")
            return False
        if header.length > 0:
            if len(value) > header.length:
                self.logger.warning(f"The header {header.name} value,"
                                    f" is not valid! the value length: {len(value)} ->"
                                    f" the header limit is: {header.length}, skipping item")
                return False
        try:
            self.FIELDS_TYPES[header.field_type](value)
        except Exception as ex:
            self.logger.warning(f"The header {header.name} value,"
                                f" is not valid! the value can't be casting to the wanted type.\n"
                                f"Expected casting to {header.field_type}, failed on ex: {str(ex)}, skipping item")
            return False
        return True

    @staticmethod
    @exception_wrapper
    def json_to_dict(file_path: str) -> List[Dict]:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

    @staticmethod
    @exception_wrapper
    def xml_to_dict(file_path: str) -> List[Dict]:
        tree = ElementTree.parse(file_path)
        root = tree.getroot()
        result = []
        for product_elem in root.findall('product'):
            product_dict = {}
            for child_elem in product_elem:
                product_dict[child_elem.tag] = child_elem.text
            result.append(product_dict)
        return result

    @staticmethod
    @exception_wrapper
    def csv_to_dict(file_path: str) -> List[Dict]:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            result = list(csv.DictReader(csvfile))
        return result

    @staticmethod
    @exception_wrapper
    def log_to_dict(file_path: str) -> List[Dict]:
        result = []
        with open(file_path, 'r', encoding='utf-8') as logfile:
            info_lines = re.findall(r'\[.*?] INFO: (.*)', logfile.read())
            for info_line in info_lines:
                info_dict = {}
                info_parts = info_line.split('|')
                for part in info_parts:
                    key, value = part.strip().split(':', 1)
                    info_dict[key.strip()] = value.strip()
                result.append(info_dict)
        return result
