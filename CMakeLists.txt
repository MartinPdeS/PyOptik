cmake_minimum_required(VERSION 3.4...3.18)

#Upload Pypi package-----------------------------------------------------------------------
add_custom_command(
  OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/Upload.txt
  COMMAND rm -rf dist/*
  COMMAND python3 setup.py bdist_wheel --NewMinor
  COMMAND python3 -m twine upload --password $ENV{PyPiPassword} --username $ENV{PyPiToken} --repository pypi dist/*
  COMMENT "Upload on Pypi")
add_custom_target(Upload DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/Upload.txt)
