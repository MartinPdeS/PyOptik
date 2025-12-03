# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|------------------------------------- | -------: | -------: | -------: | -------: | ---------: | --------: |
| PyOptik/material/base\_class.py      |       51 |        5 |       14 |        4 |     86.15% |13, 16, 29, 40, 56->exit, 83 |
| PyOptik/material/sellmeier\_class.py |       75 |        1 |       24 |        1 |     97.98% |        85 |
| PyOptik/material/tabulated\_class.py |       57 |        4 |        4 |        2 |     90.16% |72, 85-86, 114 |
| PyOptik/material\_bank.py            |      164 |        7 |       62 |       11 |     91.15% |191-192, 237, 241, 318->321, 323->exit, 392-394, 402->408, 408->396, 456->460, 462->466, 466->470, 515->519 |
| PyOptik/utils.py                     |       44 |        1 |       10 |        2 |     94.44% |58, 72->exit |
|                            **TOTAL** |  **395** |   **18** |  **114** |   **20** | **92.14%** |           |

1 file skipped due to complete coverage.


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