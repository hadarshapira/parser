#!/usr/bin/env python
import os
import json
import argparse
import tempfile

from services.parser import Parser, json_serial
from services.logger_helper import init_logger, remove_logger_handlers


def _get_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help='Path to input file for parsing')
    parser.add_argument('-o', '--output_dir', required=False, default=tempfile.gettempdir(), help='Output folder')
    parser.add_argument('-c', '--config', required=False, help='Output folder')
    return parser.parse_args()


def _get_parser(config, logger):
    if config:
        return Parser(config=config, logger=logger)
    return Parser(logger=logger)


def _write_outputs(input_file, output_dir, parsed_results):
    file_name, extension = os.path.basename(input_file).rsplit(".", 1)
    output_dir = os.path.join(output_dir, "parser_results", extension)
    os.makedirs(name=output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{file_name}_parsed.json')
    with open(output_file, "w") as output_json:
        json.dump(parsed_results, output_json, indent=4, default=json_serial)


def run():
    args = _get_command_line_args()
    os.makedirs(name=args.output_dir, exist_ok=True)
    logger = init_logger(output_dir=args.output_dir)
    try:
        parser = _get_parser(config=args.config, logger=logger)
        logger.info(f"Start parsing: {args.input_file}")
        format_results = parser.parse(file_path=args.input_file)
        logger.info(f"Start parsing: {args.input_file}")
        _write_outputs(args.input_file, args.output_dir, format_results)
    finally:
        remove_logger_handlers(logger=logger)


if __name__ == '__main__':
    run()
