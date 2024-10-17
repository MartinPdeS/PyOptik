import yaml
from PyOptik import MaterialBank

# MaterialBank.build_library('classics')
# MaterialBank.only_sellmeier = True

MaterialBank.set_filter(only_sellmeier=False)

# mater = MaterialBank.gold

# MaterialBank.print_available()

print(MaterialBank.all)
