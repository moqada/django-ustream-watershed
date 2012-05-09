# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-ustream-watershed',
    version='0.1.0',
    description='SOAP web service for Ustream watershed',
    author='Masahiko Okada',
    author_email='moqada@gmail.com',
    url='http://github.com/moqada/django-ustream-watershed/',
    license='BSD License',
    classifiers=[
        'Development Status :: 2 - Pref-Alpha',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'PySimpleSOAP',
        'phpserialize',
        'python-dateutil',
    ],
    )
