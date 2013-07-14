import pypissh 
pypissh.monkeypatch()

from setuptools import setup

setup(
    name='rembed',
    version='0.1.0',
    author='Matt Thomson',
    author_email='matt.thomson@cantab.net',
    license='MIT',
    description='Python OEmbed consumer library with automatic discovery of producers',
    long_description=open('README.txt').read(),

    provides=['rembed'],
    py_modules=['rembed'],

    install_requires=open('requirements/install.txt').readlines(),
    test_requires=open('requirements/test.txt').readlines(),
)