import os
import json


def get_expected_and_actual_files_locations(file_name, extension, test_output):
    actual = get_actual_file_location(file_name, extension, test_output)
    expected = get_expected_file_location(file_name, extension)
    return actual, expected


def get_expected_file_location(file_name, extension):
    return os.path.join(os.path.dirname(__file__), "test_results", "parser_results",
                        extension, f"{file_name}_parsed.json")


def get_actual_file_location(file_name, extension, test_output):
    return os.path.join(test_output, "parser_results", extension, f"{file_name}_parsed.json")


def get_file_content(file_path):
    with open(file_path) as expected:
        result = json.load(expected)
    return result
