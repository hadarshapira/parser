import os
import json
import argparse
import tempfile

from services.parser import Parser


def _get_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help='Path to input file for parsing')
    parser.add_argument('-o', '--output_dir', required=False, default=tempfile.gettempdir(), help='Output folder')
    return parser.parse_args()


def run():
    args = _get_command_line_args()
    parser = Parser(args.input_file)
    parsed_results = parser.read_file_to_dict()
    format_results = parser.convert_to_single_format()
    _write_outputs(args.input_file, args.output_dir, parsed_results)


def _write_outputs(input_file, output_dir, parsed_results):
    file_name, extension = os.path.basename(input_file).rsplit(".", 1)
    output_dir = os.path.join(output_dir, "parser_results", extension)
    print(output_dir)
    os.makedirs(name=output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{file_name}_parsed.json')
    with open(output_file, "w") as output_json:
        json.dump(parsed_results, output_json, indent=4)


if __name__ == '__main__':
    run()
