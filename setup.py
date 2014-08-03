from setuptools import setup


setup(
    author = 'Walkman',
    name = 'handparser',
    version = '0.8.0',
    py_modules = ['handparser'],
    install_requires = ['pytz'],
    tests_require = ['pytest', 'coveralls'],
    classifiers = [
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Poker",
    ],
)
