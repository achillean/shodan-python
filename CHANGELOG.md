CHANGELOG
=========

1.8.0
-----
* Shodan CLI now installs properly on Windows (#66)
* Improved output of "shodan host" (#64, #67)
* Fixed bug that prevented an open port from being shown in "shodan host" (#63)
* No longer show an empty page if "shodan search" didn't return results (#62)
* Updated docs to make them Python3 compatible

1.7.7
-----
* Added "shodan data download" command to help download bulk data files

1.7.6
-----
* Add basic support for the Bulk Data API

1.7.5
-----
 * Handle Cloudflare timeouts

1.7.4
-----
 * Added "shodan radar" command

1.7.3
-----
 *  Fixed the bug #47 which was caused by the CLI using a timeout value of "0" which resulted in the "requests" library failing to connect

1.7.2
-----
 * stream: automatically decode to unicode, fixes streaming on python3 (#45)
 * Include docs in packages (#46)
 * stream: handle timeout=None, None (default) can't be compared with integers (#44)

1.7.1
-----
 * Python3 fixes for outputting images (#42)
 * Add the ability to save results from host lookups via the CLI (#43)

1.7.0
-----
 * Added "images" convert output format to let users extract images from Shodan data files (#42)
