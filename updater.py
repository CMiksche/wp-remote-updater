'''
WP Remote Updater

Copyright 2017 - 2020 Christoph Daniel Miksche
All rights reserved.

License: GNU General Public License
'''
import os
import zipfile
import ftplib
import shutil
import configparser
from urllib.request import urlopen
import fire
import mechanize
from wronnay_search_lib.crawler import Crawler


def get_generator(site):
    '''
    Get the generator meta tag which includes the WP Version
    :param site: The wordpress site
    :return:
    '''
    crawl = Crawler(site)
    meta = crawl.getMetaTags()
    return meta['generator']


def ftp_upload(ftp, path):
    '''
    Upload files via ftp
    :param ftp:
    :param path:
    :return:
    '''
    # List of local files
    files = os.listdir(path)
    # Change to local dir
    os.chdir(path)
    for file in files:
        if os.path.isfile(file):
            file_handler = open(file, 'rb')
            ftp.storbinary('STOR %s' % file, file_handler)
            file_handler.close()
        elif os.path.isdir(file):
            try:
                ftp.mkd(file)
            except (OSError, FileExistsError, IsADirectoryError, NotADirectoryError):
                pass
            ftp.cwd(file)
            ftp_upload(ftp, file)
    ftp.cwd('..')
    os.chdir('..')


def wp_login(config, browser):
    '''
    Login to WordPress
    :param config: The config object
    :param browser: The mechanize browser instance
    :return:
    '''
    browser.open(config.get('WordPress', 'site') + '/wp-login.php')
    browser.select_form(nr=0)
    browser.form['user_login'] = config.get('WordPress', 'username')
    browser.form['user_pass'] = config.get('WordPress', 'password')
    browser.submit()


def click_on_update(browser):
    '''
    Click on the update button
    :param browser:
    :return:
    '''
    # Start DB Update
    try:
        req = browser.click_link(text='WordPress-Datenbank aktualisieren')
        browser.open(req)
    except mechanize.LinkNotFoundError:
        pass
    try:
        req = browser.click_link(text='Update WordPress Database')
        browser.open(req)
    except mechanize.LinkNotFoundError:
        pass


def update(settings='settings.ini'):
    '''
    Update the WordPress Site
    :param settings:
    :return:
    '''
    # Config
    config = configparser.ConfigParser()
    config.read(settings)
    if (
            get_generator(config.get('WordPress', 'refsite')) >
            get_generator(config.get('WordPress', 'site'))
    ):
        # Download Wordpress
        file = urlopen(config.get('WordPress', 'wpurl'))
        data = file.read()
        with open("wp.zip", "wb") as code:
            code.write(data)

        # Unzip WordPress
        zip_handler = zipfile.ZipFile('wp.zip')
        zip_handler.extractall()
        # Remove ZIP file
        os.remove('wp.zip')

        # Upload to the FTP-Directory
        my_ftp = ftplib.FTP(
            config.get('FTP', 'server'),
            config.get('FTP', 'username'),
            config.get('FTP', 'password')
        )

        # Change to FTP WordPress dir
        my_ftp.cwd('/'+config.get('FTP', 'workdir'))
        my_path = os.getcwd()+'/wordpress/'
        ftp_upload(my_ftp, my_path)

        # Remove WordPress Dir
        shutil.rmtree('wordpress')

        browser = mechanize.Browser()

        click_on_update(browser)
        wp_login(config, browser)
        click_on_update(browser)


def main():
    '''
    Main function
    :return:
    '''
    fire.Fire(update)


if __name__ == '__main__':
    main()
