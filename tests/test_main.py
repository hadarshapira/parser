import os
import sys
import main
import glob
import pytest
import shutil
import filecmp
import tempfile

from mock import patch
from common_utils import get_expected_and_actual_files_locations, ignore_fields_in_json_file


@pytest.fixture
def setup():
    working_dir = tempfile.mkdtemp()
    # working_dir = os.path.join(os.path.dirname(__file__), "test_results")
    os.makedirs(working_dir, exist_ok=True)
    yield working_dir
    if os.path.isdir(working_dir):
        shutil.rmtree(working_dir)


MAIN = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")


def test_parsing_all_input_types_happy_flow(setup):

    input_files = glob.glob(os.path.join(os.path.dirname(__file__), "input_files", "samples_by_extension", "*"))

    for input_file in input_files:
        fake_args = [
            MAIN,
            "-i", input_file,
            "-o", setup
        ]
        with patch.object(sys, 'argv', fake_args):
            main.run()

        file_name, extension = os.path.basename(input_file).rsplit(".", 1)
        actual, expected = get_expected_and_actual_files_locations(
            file_name=file_name,
            extension=extension,
            test_output=setup
        )
        ignore_fields_in_json_file(files_paths=[actual], ignore_fields=["source_file"])
        assert filecmp.cmp(actual, expected)
