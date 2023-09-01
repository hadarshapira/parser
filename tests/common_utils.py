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


def ignore_fields_in_json_file(files_paths, ignore_fields):
    for file_path in files_paths:
        with open(file_path, 'r') as f:
            d = json.load(f)
            for item in d:
                field_to_remove = []
                for header in item["headers"]:
                    if header in ignore_fields:
                        field_to_remove.append(header)
                for header in field_to_remove:
                    del(item["headers"][header])
        with open(file_path, 'w') as f:
            json.dump(d, f, indent=4)


def get_file_content(file_path):
    with open(file_path) as expected:
        result = json.load(expected)
    return result


def compare_json_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read().replace('\r\n', '\n')
        content2 = f2.read().replace('\r\n', '\n')
        return content1 == content2