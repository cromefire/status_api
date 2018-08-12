from os.path import exists, abspath, dirname, join
from importlib.util import spec_from_file_location, module_from_spec

bp = dirname(__file__)

main_spec = spec_from_file_location("status_api.__main__", join(bp, "__main__.py"))
main = module_from_spec(main_spec)
main_spec.loader.exec_module(main)

config_files = [
    abspath(join(bp, "../../eps.yaml")),
    abspath(join(bp, "../../eps.json")),
    "/etc/status_api.yaml",
    "/etc/status_api.json"
]

file = None
for f in config_files:
    if exists(f):
        file = f
        break

assert isinstance(file, str), "There has to be a config file in one of the following locations: " \
                              "%s" % ", ".join("\"%s\"" % cf for cf in config_files)

application = main.generate_app(file)
