import json

from Database.DatabaseAdministrator import DatabaseAdministrator
from Styles.styles import Styles

db_admin: DatabaseAdministrator
styles: Styles

with open("Styles/styles.json") as file:
    styles = json.load(file)

with open("Files/primary_keys.json") as file:
    primary_key_properties = json.load(file)

with open("Files/secondary_keys.json") as file:
    secondary_key_properties = json.load(file)
