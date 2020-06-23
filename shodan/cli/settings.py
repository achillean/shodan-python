from os import path

if path.exists(path.expanduser("~/.config/shodan")):
    SHODAN_CONFIG_DIR="~/.config/shodan/"
else:
    SHODAN_CONFIG_DIR = '~/.shodan/'

COLORIZE_FIELDS = {
    'ip_str': 'green',
    'port': 'yellow',
    'data': 'white',
    'hostnames': 'magenta',
    'org': 'cyan',
    'vulns': 'red',
}
