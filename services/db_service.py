import datetime
import os
import sqlite3
import functools

from typing import *
from services.field import Field


def db_connection(func):
    @functools.wraps(func)
    def func_wrapper(self, *args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(self.connection_string)
            cursor = conn.cursor()
            func(self, cursor, *args, **kwargs)
            conn.commit()
            conn.close()
        except Exception as ex:
            raise Exception(f"Exception catch when calling '{func.__name__}':\n{ex}") from ex
        finally:
            if conn:
                conn.close()
    return func_wrapper


class DatabaseService:

    HEADERS = "headers"
    DYNAMIC = "dynamic"
    
    PRIMARY_KEY = ("serial_number", "part")

    COLUMNS_TYPES_DICT = {
        "String": "TEXT",
        "Int": "INTEGER",
        "Datetime": "INTEGER"
    }

    def __init__(self, fields: List[Field], dynamic_data: List[str], append: bool, output: str, ):
        db_file = os.path.join(output, 'parser.db')
        self.connection_string = db_file
        self._create_tables(fields=fields, dynamic_data=dynamic_data)
        if os.path.exists(db_file) and append:
            self.connection_string = db_file
        else:
            if os.path.exists(db_file):
                os.remove(db_file)
            self.connection_string = db_file
            self._create_tables(fields=fields, dynamic_data=dynamic_data)


    def _create_tables(self, fields, dynamic_data):
        self._create_table_for_headers(fields=fields)
        primary_key = [field for field in fields if field.name in self.PRIMARY_KEY]
        self._create_table_for_dynamic_data(dynamic_data=dynamic_data, primary_key=primary_key)

    def _create_table_for_headers(self, fields: List[Field]):
        fields_setup = []
        for field in fields:
            field_str = f"{field.name}"
            field_str += f" {self.COLUMNS_TYPES_DICT.get(field.field_type)}"
            if field.length > 0:
                field_str += f' ({field.length})'
            if field.mandatory:
                field_str += f' NOT NULL'
            fields_setup.append(field_str)
        primary_key = f'({",".join(self.PRIMARY_KEY)})'
        self._generate_table(
            table_name=self.HEADERS,
            fields_setup=fields_setup,
            primary_key=primary_key
        )

    def _create_table_for_dynamic_data(self, dynamic_data: List[str], primary_key: List[Field]):
        fields_setup = [f"{field} TEXT (1000)" for field in dynamic_data]
        for key in primary_key:
            foreign_key = f"{key.name} {self.COLUMNS_TYPES_DICT.get(key.field_type)}"
            if key.length > 0:
                foreign_key += f' ({key.length})'
            foreign_key += f' NOT NULL'
            fields_setup.insert(0, foreign_key)
        extra_params = f', FOREIGN KEY ({", ".join(self.PRIMARY_KEY)}) ' \
                       f'REFERENCES {self.HEADERS} ({", ".join(self.PRIMARY_KEY)})'
        self._generate_table(
            table_name=self.DYNAMIC,
            fields_setup=fields_setup,
            extra_params=extra_params
        )

    @db_connection
    def _generate_table(self, cursor, table_name: str, fields_setup: List[str],
                        primary_key: str = None, extra_params: str = ""):
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ('
        create_table_sql += ', '.join(fields_setup)
        if primary_key:
            create_table_sql += f', PRIMARY KEY {primary_key})'
        if extra_params:
            create_table_sql += extra_params + ')'
        cursor.execute(create_table_sql)

    @db_connection
    def insert_item(self, cursor, item: Dict):
        headers_data = item[self.HEADERS]
        columns = ', '.join(headers_data.keys())
        values = ', '.join([self.cast_date_to_str(value) for value in headers_data.values()])
        headers_insert_command = f"INSERT INTO {self.HEADERS} ({columns}) " \
                                 f"VALUES ({values});"
        cursor.execute(headers_insert_command)

        dynamic_data = item[self.DYNAMIC]
        values = [self.cast_date_to_str(value) for value in dynamic_data.values()]
        values.extend([self.cast_date_to_str(headers_data.get(key)) for key in self.PRIMARY_KEY])
        values = ', '.join(values)
        columns = ', '.join(dynamic_data.keys()) + ", " + ", ".join(self.PRIMARY_KEY)
        dynamic_insert_command = f"INSERT INTO {self.DYNAMIC} ({columns}) " \
                                 f"VALUES ({values});"
        cursor.execute(dynamic_insert_command)

    @staticmethod
    def cast_date_to_str(value):
        if isinstance(value, datetime.datetime):
            kwargs = {"sep": " ", "timespec": "seconds"}
            return f"'{value.isoformat(**kwargs)}'"
        if isinstance(value, str):
            value = value.replace('\\', '\\\\')
            return f"'{value}'"
        return str(value)
