from setuptools import setup

setup(
    name='status_api',
    version='1.1.1',
    packages=['status_api'],
    package_dir={'': 'src'},
    url='https://github.com/cromefire/status_api',
    license='MPL-2.0',
    author='Tim Langhorst',
    author_email='tim.l@nghorst.net',
    description='Simple api to check if an (internal) endpoint is up, without exposing data or a '
                'port. ',
    install_requires=['requests', "flask", "PyYAML"]
)
