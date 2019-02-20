CHANGELOG
=========

1.11.0
----------
* New command **shodan scan list** to list recently launched scans
* New command **shodan alert triggers** to list the available notification triggers
* New command **shodan alert enable** to enable a notification trigger
* New command **shodan alert disable** to disable a notification trigger
* New command **shodan alert info** to show details of a specific alert
* Include timestamp, vulns and tags in CSV converter (#85)
* Fixed bug that caused an exception when parsing uncompressed data files in Python3
* Code quality improvements
* Thank you for contributions from @wagner-certat, @cclauss, @opt9, @voldmar and Antoine Neuenschwander

1.10.4
------
* Fix a bug when showing old banner records that don't have the "transport" property
* Code quality improvements (bare excepts)

1.10.3
------
* Change bare 'except:' statements to 'except Exception:' or more specific ones
* remove unused imports
* Convert line endings of `shodan/client.py` and `tests/test_shodan.py` to unix
* List file types in **shodan convert** (#80)

1.10.2
------
* Fix **shodan stats** formatting exception when faceting on **port**

1.10.1
------
* Support PUT requests in the API request helper method

1.10.0
------
* New command **shodan org**: manage enterprise access to Shodan for your team
* Improved unicode handling (#78)
* Remove deprecated API wrapper for shodanhq.com/api

1.9.1
-----
* The CHANGELOG is now part of the packages.
* Improved unicode handling in Python2 (#78)
* Add `tsv` output format for **shodan host** (#65)
* Show user-friendly error messages when running **shodan radar** without permission or in a window that's too small (#74)
* Improved exception handling to improve debugging **shodan init** (#77)

1.9.0
-----
* New optional parameter `proxies` for all interfaces to specify a proxy array for the requests library (#72)

1.8.1
-----
* Fixed bug that prevented **shodan scan submit** from finishing (#70)

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
