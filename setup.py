import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'requirements.txt')) as f:
    requirements = [line.strip() for line in f.readlines()]


setup(
    name='namecom',
    version='0.1.0',
    description='Python Library for Name.com v4 API',
    author='Tianhong Chu',
    author_email='cthesky13@gmail.com',
    url='https://github.com/CtheSky/namecom',
    packages=find_packages(exclude=("tests", "tests.*")),
    license='MIT',
    platforms=['any'],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!3.3.*',
    install_requires=requirements
)
