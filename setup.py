try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='kokoropy',
    version='0.0.0',
    author='Go Frendi Gunawan',
    author_email='gofrendiasgard@gmail.com',
    packages=['kokoropy'],
    url='http://github.com/goFrendiAsgard/kokoropy/',
    license='LICENSE.txt',
    description='Kokoro Kara MVC web framework.',
    long_description=open('README.md').read(),
    install_requires=["bottle","beaker","sqlalchemy","alembic","colorama"],
)