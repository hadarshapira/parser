import os
import glob

from mock import MagicMock
from services.parser import Parser
from common_utils import get_expected_file_location, get_file_content


def test_read_file():

    input_files = glob.glob(os.path.join(os.path.dirname(__file__), "input_files", "*"))
    Parser.init_headers = MagicMock()

    for input_file in input_files:
        parsed_results = Parser(input_file).read_file_to_dict()
        file_name, extension = os.path.basename(input_file).rsplit(".", 1)
        expected = get_expected_file_location(
            file_name=file_name,
            extension=extension
        )
        expected_results = get_file_content(expected)
        assert all(expect_dict == parse_dict for expect_dict, parse_dict in zip(expected_results, parsed_results))
