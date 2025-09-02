# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyOptik/\_\_main\_\_.py              |       17 |       17 |        6 |        0 |      0% |      1-37 |
| PyOptik/material/base\_class.py      |       51 |       12 |       14 |        2 |     69% |16, 29, 40, 56->exit, 80-89 |
| PyOptik/material/sellmeier\_class.py |       75 |        1 |       24 |        1 |     98% |        85 |
| PyOptik/material/tabulated\_class.py |       57 |        4 |        4 |        2 |     90% |72, 85-86, 114 |
| PyOptik/material\_bank.py            |      161 |       13 |       60 |       10 |     87% |130, 229-239, 313->316, 318->exit, 387-389, 397->403, 403->391, 451->455, 457->461, 461->465, 510->514 |
| PyOptik/material\_type.py            |        4 |        0 |        0 |        0 |    100% |           |
| PyOptik/utils.py                     |       44 |       10 |       10 |        2 |     74% |58, 72->exit, 86-93, 95-96 |
|                            **TOTAL** |  **409** |   **57** |  **118** |   **17** | **82%** |           |


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