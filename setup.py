'''
WP Remote Updater

Copyright 2017 - 2020 Christoph Daniel Miksche
All rights reserved.

License: GNU General Public License
'''
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name='wp_remote_updater',
    version='1.0.0',
    description='Gets the version of a reference site and updates the wordpress site,'
                ' if the reference site has a higher version.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/CMiksche/wp-remote-updater',
    author='Christoph Miksche',
    author_email='christoph@miksche.org',
    license='GPLv3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
    ],
    keywords=['wordpress', 'update', 'auto-update', 'upgrade'],
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'mechanize',
        'wronnay-search-lib'
        'fire',
        'configparser'
    ],
    py_modules=["updater"],
    entry_points={
        'console_scripts': ['wp-remote-updater=updater:main'],
    }
)
