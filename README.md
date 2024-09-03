# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                              |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|---------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyOptik/\_\_main\_\_.py           |        4 |        4 |        2 |        0 |      0% |       1-6 |
| PyOptik/base\_class.py            |        5 |        1 |        0 |        0 |     80% |        21 |
| PyOptik/data/sellmeier/default.py |        1 |        0 |        0 |        0 |    100% |           |
| PyOptik/data/tabulated/default.py |        1 |        0 |        0 |        0 |    100% |           |
| PyOptik/material.py               |       55 |        2 |       32 |       16 |     79% |43->42, 57, 62, 67->66, 72->71, 77->76, 82->81, 87->86, 92->91, 97->96, 102->101, 107->106, 112->111, 117->116, 122->121, 127->126 |
| PyOptik/sellmeier\_class.py       |       85 |        6 |       38 |        6 |     90% |52, 67->exit, 92, 126-127, 141, 146 |
| PyOptik/tabulated\_class.py       |       60 |        4 |       10 |        2 |     91% | 67, 84-86 |
| PyOptik/utils.py                  |       59 |        6 |       30 |        8 |     82% |34-37, 67, 69->74, 72, 74->exit, 76->exit, 114->118, 118->122, 161->165 |
|                         **TOTAL** |  **270** |   **23** |  **112** |   **32** | **85%** |           |


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