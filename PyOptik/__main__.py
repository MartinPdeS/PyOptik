from PyOptik import MaterialBank
import logging


if __name__ == '__main__':
    logging.info('Building material library')
    MaterialBank.build_library('classics')
