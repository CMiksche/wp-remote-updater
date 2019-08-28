'''
WP Remote Updater

Copyright 2017, 2018 Christoph Daniel Miksche
All rights reserved.

License: GNU General Public License
'''
from wronnay_search_lib.crawler import Crawler
import zipfile
import ftplib
import os
import shutil
import mechanize
import configparser
import fire
from urllib.request import urlopen


def getGenerator(site):
    crawl = Crawler(site)
    meta = crawl.getMetaTags()
    return meta['generator']


def update(settings='settings.ini'):
    # Config
    config = configparser.ConfigParser()
    config.read(settings)
    if (getGenerator(config.get('WordPress', 'refsite')) > getGenerator(config.get('WordPress', 'site'))):

        # Download Wordpress
        f = urlopen(config.get('WordPress', 'wpurl'))
        data = f.read()
        with open("wp.zip", "wb") as code:
            code.write(data)

        # Unzip WordPress
        zip = zipfile.ZipFile('wp.zip')
        zip.extractall()
        # Remove ZIP file
        os.remove('wp.zip')

        # Upload to the FTP-Directory
        myFTP = ftplib.FTP(config.get('FTP', 'server'), config.get('FTP', 'username'), config.get('FTP', 'password'))

        # Change to FTP WordPress dir
        myFTP.cwd('/'+config.get('FTP', 'workdir'))

        myPath = os.getcwd()+'/wordpress/'
        def uploadThis(path):
            # List of local files
            files = os.listdir(path)
            # Change to local dir
            os.chdir(path)
            for f in files:
                if os.path.isfile(f):
                    fh = open(f, 'rb')
                    myFTP.storbinary('STOR %s' % f, fh)
                    fh.close()
                elif os.path.isdir(f):
                    try:
                        myFTP.mkd(f)
                    except:
                        pass
                    myFTP.cwd(f)
                    uploadThis(f)
            myFTP.cwd('..')
            os.chdir('..')
        uploadThis(myPath)

        # Remove WordPress Dir
        shutil.rmtree('wordpress')

        # Login to WordPress
        browser = mechanize.Browser()
        browser.open(settings.site+'/wp-login.php')
        browser.select_form(nr = 0)
        browser.form['user_login'] = config.get('WordPress', 'username')
        browser.form['user_pass'] = config.get('WordPress', 'password')
        browser.submit()

        # Start DB Update
        try:
            req = browser.click_link(text='WordPress-Datenbank aktualisieren')
            browser.open(req)
        except:
            pass
        try:
            req = browser.click_link(text='Update WordPress Database')
            browser.open(req)
        except:
            pass


def main():
    fire.Fire(update)


if __name__ == '__main__':
  main()