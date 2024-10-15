import yaml
from PyOptik.directories import data_path

file_path = data_path / 'classic'

file_path = file_path.with_suffix('.yml')


with open(file_path.with_suffix('.yml'), 'r') as file:
    data_dict = yaml.safe_load(file)

for element, url in data_dict['sellmeier'].items():
    print(element)

