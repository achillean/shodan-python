CHANGELOG
=========

1.23.0
------
* Add new CLI command: shodan alert domain

1.22.1
------
* Fix bug when converting data file to CSV using Python3

1.22.0
------
* Add support for new vulnerability streaming endpoints

1.21.3
------
* Fix geo.json file converter

1.21.2
------
* Add support for paging through the domain information

1.21.1
------
* Add ``history`` and ``type`` parameters to ``Shodan.dns.domain_info()`` method and CLI command

1.21.0
------
* New API methods ``api.search_facets()`` and ``api.search_filters()`` to get a list of available facets and filters.

1.20.0
------
* New option "-S" for **shodan domain** to save results from the lookup
* New option "-D" for **shodan domain** to lookup open ports for IPs in the results

1.19.0
------
* New method to edit the list of IPs for an existing network alert

1.18.0
------
* Add library methods for the new Notifications API

1.17.0
------
* Fix bug that caused unicode error when printing domain information (#106)
* Add flag to let users get their IPv6 address **shodan myip -6**(#35)

1.16.0
------
* Ability to specify list of fields to include when converting to CSV/ Excel (#107)
* Filter the Shodan Firehose based on tags in the banner

1.15.0
------
* New option "--skip" for download command to help users resume a download

1.14.0
------
* New command **shodan version** (#104).
* Only change api_key file permissions if needed (#103)

1.13.0
------
* New command **shodan domain** to lookup a domain in Shodan's DNS database
* Override environment configured settings if explicit proxy settings are supplied (@cudeso)

1.12.1
------
* Fix Excel file conversion that resulted in empty .xlsx files

1.12.0
------
* Add new methods to ignore/ unignore trigger notifications

1.11.1
------
* Allow a single network alert to monitor multiple IP ranges (#93)

1.11.0
------
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
