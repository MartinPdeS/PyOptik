# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                              |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyOptik/base\_class.py            |        5 |        1 |        0 |        0 |     80% |        19 |
| PyOptik/data/sellmeier/default.py |        1 |        0 |        0 |        0 |    100% |           |
| PyOptik/data/tabulated/default.py |        1 |        0 |        0 |        0 |    100% |           |
| PyOptik/download.py               |        3 |        3 |        2 |        0 |      0% |       1-5 |
| PyOptik/material.py               |       40 |       12 |       24 |       12 |     62% |23->22, 24, 27->26, 28, 31->30, 32, 35->34, 36, 39->38, 40, 43->42, 44, 47->46, 48, 51->50, 52, 55->54, 56, 59->58, 60, 63->62, 64, 67->66, 68 |
| PyOptik/sellmeier\_class.py       |       82 |        5 |       36 |        6 |     91% |52, 67->exit, 88, 125-126, 138->141, 142 |
| PyOptik/tabulated\_class.py       |       50 |        0 |        8 |        2 |     97% |57->60, 60->63 |
| PyOptik/utils.py                  |       23 |        9 |        8 |        0 |     52% |31-34, 40-46 |
|                         **TOTAL** |  **205** |   **30** |   **78** |   **20** | **80%** |           |


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