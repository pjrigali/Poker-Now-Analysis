import os
from setuptools import setup

current_path = os.path.abspath('.')


def read_file(*parts):
    with open(os.path.join(current_path, *parts), encoding='utf-8') as reader:
        return reader.read()


setup(
    name='poker_now_analysis',
    version='1.0.1',
    packages=["poker", ],
    author='Peter Rigali',
    author_email='peterjrigali@gmail.com',
    license='MIT',
    description='A package for analyzing past performance and player habits from Poker Now.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='None',
)
