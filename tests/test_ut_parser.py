import os
import glob

from mock import MagicMock
from services.parser import Parser

expected_dict = [
    {
        'field_1': 'value_1',
        'field_2': 'value_2'
    },
    {
        'field_1': 'value_3',
        'field_2': 'value_4'
    }
]


def test_read_file():
    input_files = glob.glob(os.path.join(os.path.dirname(__file__), "input_files", "files_by_extension", "*"))
    Parser.init_headers = MagicMock()
    for input_file in input_files:
        parsed_results = Parser(input_file, logger=MagicMock()).read_file_to_dict()
        assert parsed_results == expected_dict
