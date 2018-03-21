try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'frugl.com.au wrapper',
    'author': 'Jaime Ruiz',
    'url': 'http://ruizj.me',
    'download_url': '',
    'author_email': 'jaimeruizno@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['frugl'],
    'scripts': [],
    'name': 'frugl-wrapper'
}

setup(**config)
