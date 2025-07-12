# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyOptik/\_\_main\_\_.py              |        5 |        5 |        2 |        0 |      0% |       1-7 |
| PyOptik/material/base\_class.py      |       31 |        4 |       14 |        3 |     84% |16, 29, 40, 56->exit, 83 |
| PyOptik/material/sellmeier\_class.py |       79 |        2 |       24 |        2 |     96% |   86, 164 |
| PyOptik/material/tabulated\_class.py |       60 |        3 |        2 |        1 |     94% | 74, 88-89 |
| PyOptik/material\_bank.py            |      148 |        4 |       54 |       10 |     93% |124, 270->273, 275->exit, 345-347, 355->361, 361->349, 409->413, 415->419, 419->423, 468->472 |
| PyOptik/material\_type.py            |        4 |        0 |        0 |        0 |    100% |           |
| PyOptik/units.py                     |       18 |        0 |        4 |        0 |    100% |           |
| PyOptik/utils.py                     |       44 |       10 |       10 |        2 |     74% |56, 70->exit, 84-91, 93-94 |
|                            **TOTAL** |  **389** |   **28** |  **110** |   **18** | **90%** |           |


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