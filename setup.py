try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name = 'kokoropy',
    packages = ['kokoropy'], # this must be the same as the name above
    version = '0.0.1',
    description = 'MVC web framework based on Bottle',
    long_description=open('README.md').read(),
    license='LICENSE.txt',
    author = 'Go Frendi Gunawan',
    author_email = 'gofrendiasgard@gmail.com',
    url = 'https://github.com/goFrendiAsgard/kokoropy', # use the URL to the github repo
    download_url = 'https://github.com/goFrendiAsgard/kokoropy/tarball/0.1', # download url
    install_requires=["bottle","beaker","sqlalchemy","alembic","colorama"],
    keywords = ['web','mvc'], # arbitrary keywords
    classifiers = [],
)