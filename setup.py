from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['rembed']
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='rembed',
    version='0.1.1',
    author='Matt Thomson',
    author_email='matt.thomson@cantab.net',
    license='MIT',
    description='Python OEmbed consumer library with automatic discovery of producers',
    long_description=open('README.rst').read(),

    provides=['rembed'],
    packages=['rembed'],

    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    tests_require=[
        'PyHamcrest',
        'mock',
        'pytest'
    ],
    
    cmdclass = {'test': PyTest}
)
