# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                              |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyOptik/base\_class.py            |        5 |        1 |        0 |        0 |     80% |        19 |
| PyOptik/data/sellmeier/default.py |        1 |        0 |        0 |        0 |    100% |           |
| PyOptik/data/tabulated/default.py |        1 |        0 |        0 |        0 |    100% |           |
| PyOptik/download.py               |        3 |        3 |        2 |        0 |      0% |       1-5 |
| PyOptik/material.py               |       55 |        2 |       32 |       16 |     79% |28->27, 30, 35, 39->38, 43->42, 47->46, 51->50, 55->54, 59->58, 63->62, 67->66, 71->70, 75->74, 79->78, 83->82, 87->86 |
| PyOptik/sellmeier\_class.py       |       84 |        6 |       36 |        6 |     90% |52, 67->exit, 90, 127-128, 141, 146 |
| PyOptik/tabulated\_class.py       |       58 |        4 |        8 |        2 |     91% | 62, 79-81 |
| PyOptik/utils.py                  |       23 |        4 |        8 |        0 |     81% |     31-34 |
|                         **TOTAL** |  **230** |   **20** |   **86** |   **24** | **85%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/MartinPdeS/PyOptik/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/MartinPdeS/PyOptik/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2FMartinPdeS%2FPyOptik%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.