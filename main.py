try:
    from adresses import adresses
except ModuleNotFoundError:
    print('[FAIL] You need to create adresses.py, please see README.md')
    exit()
from chrome import *
import time
from sys import argv
from mail import *

GEN_URL = 'https://media.interieur.gouv.fr/deplacement-covid-19/'

def print_adresses():
    print('[INFO] adresses.py contains:')
    print('name FirstName LastName')
    for e in adresses:
        print(e, adresses[e]['prenom'], adresses[e]['nom'])


# ARGS
if len(argv) != 2:
    print('[FAIL] Please use "main.py [name]" as stated in adresses.py')
    print_adresses()
    exit()
else:
    if argv[1] not in adresses:
        print(f'[FAIL] {argv[1]} not defined. Please use "main.py [name]" as stated in adresses.py')
        print_adresses()
        exit()
    else:
        personne = argv[1]
# ARGS END

print('[LOG] Profile selected:', adresses[personne]['prenom'], adresses[personne]['nom'])

driver = open_chrome(set_options())

open_page(driver, GEN_URL)

attestation_name = fill(driver, personne)

send_email(adresses[personne]['email'], DEFAULT_DL_PATH, attestation_name)

driver.quit()

delete = input('Do you want to delete the local file (y/n): ')
if delete != 'n':
    os.remove(DEFAULT_DL_PATH + attestation_name)
    print('[SUCESS] File removed !')

exit()