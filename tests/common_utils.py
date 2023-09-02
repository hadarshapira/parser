import os
import json
import sqlite3


def get_expected_and_actual_files_locations(file_name, extension, test_output):
    actual = get_actual_file_location(test_output)
    expected = get_expected_file_location(file_name, extension)
    return actual, expected


def get_expected_file_location(file_name, extension):
    return os.path.join(os.path.dirname(__file__), "test_results", extension, f"{file_name}_parsed.json")


def get_actual_file_location(test_output):
    return os.path.join(test_output, "parser_results", f"parser.json")


def ignore_fields_in_json_file(files_paths, ignore_fields):
    for file_path in files_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            d = json.load(f)
            for item in d:
                field_to_remove = []
                for header in item["headers"]:
                    if header in ignore_fields:
                        field_to_remove.append(header)
                for header in field_to_remove:
                    del(item["headers"][header])
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(d, f, indent=4)


def compare_db_files(db1_path, db2_path):
    conn1, conn2 = None, None
    try:
        conn1 = sqlite3.connect(db1_path)
        conn2 = sqlite3.connect(db2_path)

        cursor1 = conn1.cursor()
        cursor2 = conn2.cursor()

        for table in ["headers", "dynamic"]:
            cursor1.execute(f"SELECT COUNT(*) FROM {table}")
            cursor2.execute(f"SELECT COUNT(*) FROM {table}")

            count1 = cursor1.fetchone()[0]
            count2 = cursor2.fetchone()[0]

            assert count1 == count2
    finally:
        if conn1:
            conn1.close()
        if conn2:
            conn2.close()


def compare_json_files(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = f1.read().replace('\r\n', '\n')
        content2 = f2.read().replace('\r\n', '\n')
        return content1 == content2
