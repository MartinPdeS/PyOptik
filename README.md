# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/MartinPdeS/PyOptik/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                 |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|------------------------------------- | -------: | -------: | -------: | -------: | ---------: | --------: |
| PyOptik/catalog.py                   |      324 |       58 |      106 |       31 |     76.98% |49, 83-84, 108, 113, 165, 193-\>195, 242, 245, 287-291, 298-307, 319-326, 331, 339, 344, 349, 352, 354, 368, 392-\>exit, 488, 490, 492, 536-538, 575, 579, 607, 611, 653, 662, 682-690, 697-698, 703-\>705, 706, 708-711, 715-\>702, 719, 757 |
| PyOptik/discovery.py                 |       97 |        2 |       38 |        2 |     97.04% |    84, 87 |
| PyOptik/material/base\_class.py      |      113 |       13 |       30 |        9 |     81.82% |161-167, 178, 189-\>191, 192-\>194, 217, 218-\>exit, 238-239, 258, 284, 430, 432 |
| PyOptik/material/dataset.py          |      129 |        9 |       52 |        8 |     90.61% |34, 49, 52, 58, 141-142, 144, 152, 155, 166-\>150 |
| PyOptik/material/sellmeier\_class.py |      143 |       26 |       48 |        6 |     82.20% |62, 75, 80-81, 84, 179, 186, 219, 251-252, 279-305, 316 |
| PyOptik/material/tabulated\_class.py |      195 |       28 |       56 |        7 |     85.26% |56, 75, 95, 104, 125, 164, 186, 314, 346-381, 392 |
| PyOptik/thin\_film.py                |      125 |        1 |       24 |        1 |     98.66% |       234 |
| PyOptik/tui.py                       |       61 |       53 |       10 |        2 |     14.08% |13-14, 20-104 |
| PyOptik/utils.py                     |       48 |        9 |       12 |        4 |     75.00% |61, 64-67, 71-72, 78-\>exit, 106-108 |
| **TOTAL**                            | **1267** |  **199** |  **392** |   **70** | **82.22%** |           |

2 files skipped due to complete coverage.


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