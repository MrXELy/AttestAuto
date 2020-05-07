# AttestAuto

Automatically download attestation for you and/or your family, and email it!

Download from https://media.interieur.gouv.fr/deplacement-covid-19/ into your default download folder, and send an email.

# Running from source

You need `selenium` and `chromedriver`:

 - `pip install selenium`
 - download `chromedriver` [here](https://chromedriver.chromium.org/getting-started) and put in your `PATH`

Create `adresses.py`, it will contains your and your family's adresses in a dictionnary.
```python
adresses = dict(
dad=dict(prenom='Dad First Name',
             nom='Dad Last Name',
             date_de_naissance='01/01/1970',
             lieu_de_naissance='Lyon',
             adresse='999 avenue du Parc',
             ville="Paris",
             code_postal='75009',
             email='dad@mail'),
mom=dict(prenom='Mom First Name',
             nom='Mom Last Name',
             date_de_naissance='01/01/1970',
             lieu_de_naissance='Lyon',
             adresse='999 avenue du Parc',
             ville="Paris",
             code_postal='75009',
             email='mom@mail')
)
```

In `chrome.py`, set your default download folder (customized folder does not work for now...).
```python
DEFAULT_DL_PATH = r"path\to\default\download\folder\\"
# ! Last slash is important
```

Then, in `mail.py`, set the Gmail adress you want to send the attestation from.
```python
SENDER_EMAIL = "your@mail"
```

You can either store your password in a `password.py` file or wait for the password prompt.
```python
pw = 'yourpassword'
```