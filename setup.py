import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


def read_lines(file_name):
    with open(file_name) as f:
        return f.readlines()

setup(
    name="Automator",
    version="0.0.4",
    author="Vitalii Lebedynskyi",
    author_email="vetal.lebed@gmail.com",
    description="Application helps use vk.com and automate public creation",
    license="Apache 2",
    url="https://github.com/VLebedinskyi/automator",
    setup_requires=read_lines("requirements.txt"),
    # entry_points={'console_scripts': ['ato = automator.start:do_start']}
)