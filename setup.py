from distutils.core import setup

setup(
    name='python-correios',
    version='0.0.1',
    author='Leandro T. de Souza',
    author_email='leandrotoledodesouza@gmail.com',
    packages=['correios', 'correios.test'],
    url='https://github.com/leandrotoledo/python-correios/',
    license='LICENSE.txt',
    description='API Python Correios para rastreamento de encomendas.',
    long_description=open('README.txt').read(),
)
