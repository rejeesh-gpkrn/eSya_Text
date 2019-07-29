import setuptools
from distutils.core import setup
import py2exe, sys, os


setup( \
    windows=[{'script': '__main__.py'}], \
    options={ \
        'py2exe': { \
            'includes': [ \
                'Tkinter', \
                'tkFileDialog', \
                'os', \
                'sys' \
            ], \
            'bundle_files': 1, 'compressed': True \
        } \
    }, \
    zipfile=None,)
# setuptools.setup(
#   name='eSya',
#   version='1.0.0',
#   packages=setuptools.find_packages(),
#   url='',
#   license='',
#   author='Rejeesh Gopalakrishnan',
#   author_email='rejeesh.gpkrn@gmail.com',
#   description='eSya Text Editor'
# )
