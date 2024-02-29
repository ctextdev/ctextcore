"""OCR Pytest Unit Test"""

# Copyright 2024 Centre for Text Technology, North-West University.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__authors__ = 'askruger'

from ctextcore.core import CCore as core
from pathlib import Path
import json
import logging
import os
import pytest

LOGGER = logging.getLogger(__name__)
server = core()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE_NAME = ".input.test.jpg"
INPUT_DIR = CURRENT_DIR+"/data/input/"
EXPECTED_OUTPUT_FILE_NAME = ".ocr.output.expected."

test_params = []
technologies = server.list_available_techs()
languages = ["af", "nso", "nr", "ss", "st", "tn", "ts", "ve", "xh", "zu"]
levels = ["file"]
formats = ["json", "list", "delimited"]

LOGGER.info("Testing OCR for the followig languages: {0}".format(languages))

for lang in languages:
    if lang not in technologies["ocr"]:
        server.download_model(language=lang, tech="ocr")
    for level in levels:
        EXPECTED_OUTPUT_DIR = CURRENT_DIR+"/data/expected/{0}_level/ocr/".format(level)  # Check
        for output_format in formats:
            if output_format=="json":
                OUTPUT_FILENAME = str(lang+EXPECTED_OUTPUT_FILE_NAME+output_format+".json")
            else:
                OUTPUT_FILENAME = str(lang+EXPECTED_OUTPUT_FILE_NAME+output_format+".txt")
            #OCR only has file level and not line level
            server_output = server.process_text(text_input=Path(INPUT_DIR,str(lang+INPUT_FILE_NAME)), tech="ocr", language=lang,output_format=output_format)
            with open(Path(EXPECTED_OUTPUT_DIR, OUTPUT_FILENAME), 'r', encoding='UTF-8') as expected_file:
                if output_format=="json":
                    expected_output= json.load(expected_file)
                    server_output_str = server_output
                else:
                    expected_output= ''.join(expected_file.readlines())
                    server_output_str = str(server_output)
            test_params.append(tuple((lang,server_output_str,expected_output)))

@pytest.mark.parametrize("lang,test_input,expected", test_params)
def test_process_string(lang,test_input, expected):
    """OCR test_process_string function"""
    assert test_input == expected,"OCR failed for {0}".format(lang)