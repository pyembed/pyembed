from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['rembed']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='rembed',
    version='0.3.0',
    author='Matt Thomson',
    author_email='matt.thomson@cantab.net',
    url='https://github.com/matt-thomson/rembed',
    description='Python OEmbed consumer library with automatic discovery of ' +
        'producers',
    long_description=open('README.rst').read() + '\n\n' +
        open('CHANGES.rst').read(),
    download_url='https://pypi.python.org/pypi/rembed/',
    license=open('LICENSE.txt').read(),

    provides=['rembed.core'],
    packages=['rembed.core'],
    namespace_packages=['rembed'],

    install_requires=[
        'beautifulsoup4',
        'requests'
    ],
    tests_require=[
        'mock',
        'PyHamcrest',
        'pytest'
    ],

    cmdclass={'test': PyTest},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Text Processing'
    ]
)
