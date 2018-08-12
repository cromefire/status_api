# Import app from external module

# noinspection PyUnresolvedReferences
from os.path import exists, abspath

from .__main__ import generate_app

config_files = [
    abspath("../../status_api.yaml"),
    abspath("../../status_api.json"),
    "/etc/eps.yaml",
    "/etc/eps.json"
]

file = None
for f in config_files:
    if exists(f):
        file = f
        break

assert isinstance(file, str), "There has to be a config file in one of the following locations: " \
                              "%s" % ", ".join("\"%s\"" % cf for cf in config_files)

application = generate_app(file)
