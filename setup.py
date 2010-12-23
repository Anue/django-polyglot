# -*- encoding: utf-8 -*-
from setuptools import setup

setup(
    name='django-polyglot',
    version='0.1',
    description="Django database tables internationalization facilities.",
    long_description=open('README.txt').read(),
    author='Fabián E. Gallina',
    author_email='fabian@anue.biz',
    url='http://github.com/anue/django-polyglot',
    packages=['polyglot'],
    package_dir={'polyglot': 'polyglot'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
