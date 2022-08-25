from setuptools import setup
from codecs import open
from os import path
from setuptools import find_packages

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ejtraderRL',
    packages=find_packages(),

    version='1.0.2',

    license='Apache-2.0 License',

    install_requires=['numpy', "ta", "pandas", "pandas_datareader", "matplotlib","IPython"],

    author='traderpedroso',
    author_email='info@ejtrader.com',

    url='https://github.com/ejejtraderRLabs/',  

    description='Reinforcement learning Trading envoriments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='ejtraderRL',

)
