from adresses import *
from chrome import *
from time import sleep
from sys import argv

GEN_URL = 'https://media.interieur.gouv.fr/deplacement-covid-19/'

# ARGS
personne = ''
if argv[1] == 'robin':
    personne = 'robin'
elif argv[1] == 'maman':
    personne = 'maman'
elif argv[1] == 'papa':
    personne = 'papa'
elif argv[1] == 'dupont':
    personne = 'dupont'
else:
    print('[FAIL] Please use "main.py [name]" as stated in adresses.py')
    exit()
# ARGS END

print('[LOG] Profile selected:', adresses[personne]['prenom'], adresses[personne]['nom'])

driver = open_chrome(set_options())
open_page(driver, GEN_URL)
fill(driver, personne)

driver.quit()
exit()