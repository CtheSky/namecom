from setuptools import setup, find_packages


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
)
