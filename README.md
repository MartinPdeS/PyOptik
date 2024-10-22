# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| PyOptik/\_\_main\_\_.py              |        5 |        0 |        2 |        1 |     86% |   5->exit |
| PyOptik/material/base\_class.py      |       31 |        2 |       14 |        2 |     91% |40, 56->exit, 83 |
| PyOptik/material/sellmeier\_class.py |       78 |        2 |       24 |        2 |     96% |   81, 158 |
| PyOptik/material/tabulated\_class.py |       57 |        3 |        2 |        1 |     93% | 64, 77-78 |
| PyOptik/material\_bank.py            |      145 |        1 |       54 |        9 |     95% |126, 270->273, 275->exit, 350->355, 355->344, 398->402, 404->408, 408->412, 453->457 |
| PyOptik/material\_type.py            |        4 |        0 |        0 |        0 |    100% |           |
| PyOptik/units.py                     |       18 |        0 |        4 |        0 |    100% |           |
| PyOptik/utils.py                     |       23 |        3 |        4 |        1 |     85% | 27-28, 44 |
|                            **TOTAL** |  **361** |   **11** |  **104** |   **16** | **94%** |           |


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