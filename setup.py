from setuptools import setup

setup(
    name="goodgit",
    author="Evgeny Khoroshavin",
    entry_points={
        'console_scripts': [
            'goodgit = main:main'
        ],
    }
)
