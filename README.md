## About The Project

This project is an open-source Python package for existing NCHLT core technologies for ten South African 
languages (Afrikaans, isiNdebele, isiXhosa, isiZulu, Sesotho sa Leboa, Sesotho, Setswana, Siswati, Tshivenḓa, Xitsonga). The technologies include the following: Tokenisers, Sentence Separators, Part of Speech Taggers, Named Entity 
Recognisers, Phrase Chunkers, Optical Character Recognisers, Universal Part of Speech Taggers, Lemmatisers, and a Language Identifier. The package also includes a Morphological Analyser for isiNdebele, isiZulu, isiXhosa, and Siswati, totalling 85 technologies.

## Getting Started

To get a local copy installed and running, follow these steps.

### Prerequisites

* Python 3.8+ (https://www.python.org/downloads/)
* Java OpenJDK 17+ (https://openjdk.org)
* Requests 2.32.3 (https://pypi.org/project/requests/2.32.3/)

### Installation

### pip

```sh
pip install ctextcore
```

### GitHub

```
# Download the source code from GitHub
git clone https://github.com/ctextdev/ctextcore.git

# Install from source
cd ctextcore
py -m pip install .

# Install from source in Development Mode
cd ctextcore
py -m pip install -e .
```

## Usage 

### Importing the CTexT Core library

```Python
from ctextcore.core import CCore as core
server = core()
```

The core method accepts the following configuration arguments:

```Python
port: 8079              # Set the port the server should use
timeout: 60000          # Set the timeout of HTTP requests
threads: 5              # Set the total number of threads to use
memory: "4G"            # Set the maximum memory allowed to be used by the server
be_quiet: False         # Set the logging output from the server
max_char_length: 10000  # Set the maximum character length 

server = core(port=8081,memory="16G",...)
```

### Language codes

* Afrikaans -> af
* isiNdebele -> nr
* isiXhosa -> xh
* isiZulu -> zu
* Sesotho sa Leboa -> nso
* Sesotho -> st
* Setswana -> tn
* Siswati -> ss
* Tshivenḓa -> ve
* Xitsonga -> ts

### Downloading models

#### Download all language models for a specific technology

```Python
# This call will download all the language models for POS.
server.download_model(tech='pos', language='all')
```

#### Download all technologies for a specific language

```Python
# This call will download all the technology models for isiZulu.
server.download_model(tech='all', language='zu')
```
    
#### Download a specific language model for a specific technology

```Python
# This call will download the POS technology model for Sesotho sa Leboa.
server.download_model(tech='pos', language='nso')
```

### Using a model

```Python
# This call will run the isiZulu POS tagger on the input text 'E uma lungekho usuku olufakiwe, usuku lwakho lokubhalisa luyofakwa nge-othomathikhi kube usuku lokuqala lwenyanga elandelayo ukuze kungadaleki izikweletu.'.
output_process = server.process_text(text_input='E uma lungekho usuku olufakiwe, usuku lwakho lokubhalisa luyofakwa nge-othomathikhi kube usuku lokuqala lwenyanga elandelayo ukuze kungadaleki izikweletu.', language='zu', tech='pos')
print(output_process)

from pathlib import Path # Path needs to be imported to be able to use OCR

# This call will run the Sesotho sa Leboa OCR on the image or pdf path provided in the text_input argument.
output_process = server.process_text(text_input=Path('<path-to-image-or-pdf>'), language='nso', tech='ocr')
print(output_process)

# This call will run LID on the input text 'Sizoqhubeka ukwenza ngcono ukusebenza kukagesi wethu kanye nokuthembela kugesi ophinde uvuseleleke.' and the confidence level should be above 50%.
output_process = server.process_text(text_input='Sizoqhubeka ukwenza ngcono ukusebenza kukagesi wethu kanye nokuthembela kugesi ophinde uvuseleleke.', tech='lid', confidence=0.5)
print(output_process)
```

#### Output formats

The ctextcore package offers three different output formats (JSON, Delimited, List), the default output format is JSON and can be changed by providing the output_format argument in the process_text method. An extra argument, delimiter, can be used together with the delimited output format to change the delimiter used in the output. The default delimiter is _.

```Python

# This call will run the Afrikaans POS tagger on the input text 'Hierdie is ''n voorbeeldsin om die funksionaliteit te toets.' and will return a delimited output.
output_process = server.process_text(text_input='Hierdie is \'n voorbeeldsin om die funksionaliteit te toets.', language='af', tech='pos', output_format="delimited", delimiter="|")
print(output_process)

```

#### Output examples:

```Python

# JSON
[{'doc': {'p': {'lid': 'NONE', 'tokenised': True, 'sent': {'tokens': [{'start_char': 0, 'pos': 'PA', 'end_char': 7, 'id': 1, 'text': 'Hierdie'}, {'start_char': 8, 'pos': 'VTHOK', 'end_char': 10, 'id': 2, 'text': 'is'}, {'start_char': 11, 'pos': 'LO', 'end_char': 13, 'id': 3, 'text': "'n"}, {'start_char': 14, 'pos': 'NSE', 'end_char': 26, 'id': 4, 'text': 'voorbeeldsin'}, {'start_char': 27, 'pos': 'SVS', 'end_char': 29, 'id': 5, 'text': 'om'}, {'start_char': 30, 'pos': 'LB', 'end_char': 33, 'id': 6, 'text': 'die'}, {'start_char': 34, 'pos': 'NSE', 'end_char': 49, 'id': 7, 'text': 'funksionaliteit'}, {'start_char': 50, 'pos': 'UPI', 'end_char': 52, 'id': 8, 'text': 'te'}, {'start_char': 53, 'pos': 'VTHOG', 'end_char': 58, 'id': 9, 'text': 'toets'}, {'start_char': 58, 'pos': 'ZE', 'end_char': 59, 'id': 10, 'text': '.'}]}}}}]

# List
[('Hierdie', 'PA'), ('is', 'VTHOK'), ("'n", 'LO'), ('voorbeeldsin', 'NSE'), ('om', 'SVS'), ('die', 'LB'), ('funksionaliteit', 'NSE'), ('te', 'UPI'), ('toets', 'VTHOG'), ('.', 'ZE')]

# Delimited
['Hierdie|PA', 'is|VTHOK', "'n|LO", 'voorbeeldsin|NSE', 'om|SVS', 'die|LB', 'funksionaliteit|NSE', 'te|UPI', 'toets|VTHOG', '.|ZE']


```

## Testing

The ctextcore package uses pytest version 8.0.0 or above as a testing framework and is a required prerequisite to be able to run the unit tests of the package.

### Running all the unit tests of the ctextcore package

```sh
py -m pytest --pyargs ctextcore.tests
```

### Running individual unit tests of the ctextcore package

The ctextcore package contains the following unit tests:

* zalid
* ner
* ocr
* pc
* pos
* upos
* sent
* tok
* morph
* lemma

#### Running an individual unit test

```sh
py -m pytest --pyargs ctextcore.tests.test_name
```

#### Example

```sh
py -m pytest --pyargs ctextcore.tests.test_zalid
```

## License

Licensed under the Apache License, Version 2.0. See `LICENSE.txt` for more information.

## Contact

Centre for Text Technology (CTexT) - ctext@nwu.ac.za - https://humanities.nwu.ac.za/ctext

