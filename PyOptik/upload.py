from PyOptik.utils import download_yml_file

urls = dict(
    ZBLAN='https://refractiveindex.info/database/data-nk/glass/misc/ZBLAN/Gan.yml',
    BK7='https://refractiveindex.info/database/data-nk/glass/schott/N-BK7.yml',
    silica='https://refractiveindex.info/database/data-nk/main/SiO2/Malitson.yml',
    BAK1='https://refractiveindex.info/database/data-nk/glass/schott/N-BAK1.yml',
    SF5='https://refractiveindex.info/database/data-nk/glass/schott/N-SF5.yml',
)

for name, url in urls.items():
    download_yml_file(
        url=url,
        filename=name
    )