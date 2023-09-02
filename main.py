#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import argparse
import tempfile
from typing import *

from services.parser import Parser, json_serial
from services.db_service import DatabaseService
from services.logger_service import init_logger, remove_logger_handlers


def _get_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help='Path to input file for parsing')
    parser.add_argument('-o', '--output_dir', required=False, default=tempfile.gettempdir(), help='Output folder')
    parser.add_argument('-c', '--config', required=False, help='Config file path')
    parser.add_argument('-a', '--append', required=False, action="store_true", help='Append results to an existing files')
    parser.add_argument('-u', '--update_db', required=False, action="store_true", help='Writes results to db file')
    return parser.parse_args()


def _get_parser(config, logger):
    if config:
        return Parser(config=config, logger=logger)
    return Parser(logger=logger)


def _write_results_to_db(update_db: bool, output_dir: str, results: List[Dict], append: bool, parser: Parser):
    if update_db:
        database_helper = DatabaseService(
            fields=parser.fields,
            dynamic_data=parser.dynamic_data_keys,
            output=output_dir,
            append=append
        )
        for item in results:
            database_helper.insert_item(item=item)


def _write_results_to_json(output_dir, results, append, logger):
    logger.info(f'Writing results to json file')
    os.makedirs(name=output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'parser.json')
    with open(output_file, "a" if append else "w", encoding='utf-8') as output_json:
        json.dump(results, output_json, indent=4, default=json_serial)
    logger.info(f'Results were written to: {output_file}')


def run():
    args = _get_command_line_args()
    output_dir = os.path.join(args.output_dir, "parser_results")
    logs_folder = os.path.join(output_dir, "logs")
    os.makedirs(name=logs_folder, exist_ok=True)
    logger = init_logger(output_dir=logs_folder)
    try:
        parser = _get_parser(config=args.config, logger=logger)
        logger.info(f"Start parsing: {args.input_file}")
        parser_results = parser.parse(file_path=args.input_file)
        logger.info(f"Finished parsing: {args.input_file}")
        _write_results_to_json(
            output_dir=output_dir,
            results=parser_results,
            append=args.append,
            logger=logger
        )
        _write_results_to_db(
            update_db=args.update_db,
            output_dir=output_dir,
            results=parser_results,
            append=args.append,
            parser=parser
        )

    finally:
        remove_logger_handlers(logger=logger)


if __name__ == '__main__':
    run()
