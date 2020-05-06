from adresses import *
from chrome import *
from time import sleep
import argparse

GEN_URL = 'https://media.interieur.gouv.fr/deplacement-covid-19/'

# ARGS
parser = argparse.ArgumentParser()
parser.add_argument("--robin", action="store_true")
parser.add_argument("--maman", action="store_true")
parser.add_argument("--papa", action="store_true")
parser.add_argument("--dupont", action="store_true")

args = parser.parse_args()

personne = ''
if args.robin is True:
    personne = 'robin'
elif args.maman is True:
    personne = 'maman'
elif args.papa is True:
    personne = 'papa'
elif args.dupont is True:
    personne = 'dupont'
else:
    print('[FAIL] Précisez la personne à attester (--help)')
    exit()
# ARGS END

print('[LOG] Profil sélectionné :', adresses[personne]['prenom'])

driver = open_chrome(set_options())
open_page(driver, GEN_URL)
fill(driver, personne)

driver.quit()
exit()