import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


install_requires = [
    'pytz',
    'requests',
    'beautifulsoup4',
    'lxml',
    'python-dateutil',
    'parsedatetime'
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name = 'poker',
    version = '0.10.0',
    description = 'Poker Framework',
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Poker",
    ],
    keywords = 'poker',
    author = "Kiss György",
    author_email = "kissgyorgy@me.com",
    url = "https://github.com/pokerregion/poker",
    license = "MIT",
    packages = find_packages(),
    install_requires = install_requires,
    tests_require = ['pytest', 'coverage', 'coveralls'],
    cmdclass = {'test': PyTest},
)
