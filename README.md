# AttestAuto

Automatically download attestation for you and/or your family!

Download from here : https://media.interieur.gouv.fr/deplacement-covid-19/

Into your default download folder

# Running from source

You need `selenium` and `chromedriver`:

 - `pip install selenium`
 - download `chromedriver` [here](https://chromedriver.chromium.org/getting-started) and put in your `PATH`

Create `adresses.py`, it will contains your and your family's adresses in a dictionnary:
```python
adresses = dict(
dad=dict(prenom='Dad First Name',
             nom='Dad Last Name',
             date_de_naissance='01/01/1970',
             lieu_de_naissance='Lyon',
             adresse='999 avenue du Parc',
             ville="Paris",
             code_postal='75009'),
mom=dict(prenom='Mom First Name',
             nom='Mom Last Name',
             date_de_naissance='01/01/1970',
             lieu_de_naissance='Lyon',
             adresse='999 avenue du Parc',
             ville="Paris",
             code_postal='75009')
)
```

In `main.py`, change `if` statements to match your dictionnary:
```python
personne = ''
if argv[1] == 'dad':
    personne = 'dad'
elif argv[1] == 'mom':
    personne = 'mom'
```

Then, in `chrome.py`, set your default download folder (customized folder does not work for now...):
```python
DEFAULT_DL_PATH = r"path\to\default\download\folder"
```