from PyOptik.utils import download_yml_file

urls = dict(
    ZBLAN='https://refractiveindex.info/?shelf=glass&book=ZBLAN&page=Gan',
    BK7='https://refractiveindex.info/?shelf=glass&book=BK7&page=SCHOTT',
    borosilicate='https://refractiveindex.info/?shelf=glass&book=SCHOTT-BK&page=N-BK7',
    silica='https://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson',
    BAK1='https://refractiveindex.info/?shelf=glass&book=BAK1&page=SCHOTT',
    SF5='https://refractiveindex.info/?shelf=glass&book=SF5&page=SCHOTT',
    fluoring_doped_silica_1='https://opg.optica.org/directpdfaccess/d4c1352d-90ca-4c3e-a7545be751547d7a_26968/ao-22-19-3102.pdf?da=1&id=26968&seq=0&mobile=no',
    fluoring_doped_silica_2='https://opg.optica.org/directpdfaccess/d4c1352d-90ca-4c3e-a7545be751547d7a_26968/ao-22-19-3102.pdf?da=1&id=26968&seq=0&mobile=no'
)

for name, url in urls.items():

    download_yml_file(
        url='https://refractiveindex.info/database/data-nk/main/SiO2/Malitson.yml',
        filename='test_2'
    )