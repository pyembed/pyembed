import pypissh 
pypissh.monkeypatch()

from distutils.core import setup

setup(
    name='rembed',
    version='0.1.0',
    author='Matt Thomson',
    author_email='matt.thomson@cantab.net',
    packages=['rembed',],
    license='MIT',
    description='Python OEmbed consumer library with automatic discovery of producers',
    long_description=open('README.txt').read()
)