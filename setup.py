import sys
from setuptools import setup, find_packages


install_requires = [
    'pytz',
    'requests',
    'lxml',
    'python-dateutil',
    'parsedatetime',
    'cached-property',
    'click',
]


entry_points = {
    'console_scripts': [
        'poker = poker.scripts:poker',
    ]
}


setup(
    name = 'poker',
    version = '0.21.0',
    description = 'Poker Framework',
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
    ],
    keywords = 'poker',
    author = "Kiss György",
    author_email = "kissgyorgy@me.com",
    url = "https://github.com/pokerregion/poker",
    license = "MIT",
    packages = find_packages(),
    install_requires = install_requires,
    entry_points = entry_points,
    tests_require = ['pytest', 'coverage', 'coveralls'],
)
