import pymrio

# 0. define constants
PATH = '/home/julien/PycharmProjects/exiobase2/'

# 1. Load and parse exiobase2 database
# (https://www.exiobase.eu/index.php/data-download/exiobase2-year-2007-full-data-set)
exio2 = pymrio.parse_exiobase2(path=PATH + 'mrIOT_IxI_fpa_coefficient_version2.2.2',
                               charact=True, popvector='exio2')

# 2. Calculate missing input-output tables
exio2.calc_all()

# 3. Export tables for later use (see "analyse_results.py")
exio2.save_all(path=PATH)
