# WordPress Remote Updater

Gets the version of a reference site and update the wordpress site, if the reference site has a higher version.

It downloads the latest wordpress version and upload it via ftp. After login, it clicks on the "Update WordPress Database" link.

## Procedure
* Checks if the reference site has a higher version.
* Download the new wp version.
* Unzip the wordpress zip file.
* Upload the new files.
* Login to update the database.
* Update the wordpress database.

## General Information
License: GNU General Public License

Author: Christoph Daniel Miksche (m5e.de)

## Installation

1. Use the following command to install all dependencies.

  ```
  pip install BeautifulSoup4 lxml mechanize
  ```

2. Then clone the git repository.

3. After that, please change the variables in the settings.py file.

4. Enter the command `python updater.py` in your commandline.

5. If you want to schedule your updates, edit your /etc/crontab file.
