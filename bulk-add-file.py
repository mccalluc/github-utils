import sys
import getpass
import urllib
import requests
import subprocess
import os


def api_url(path_template, keys):
    # print path_template % tuple(map(urllib.quote_plus, keys))
    return 'https://api.github.com' + path_template % tuple(map(urllib.quote, keys))


def api_get(path_template, *keys):
    url = api_url(path_template, keys)
    return requests.get(url).json()


def api_delete(path_template, *keys):
    url = api_url(path_template, keys)
    requests.delete(url, auth=(username, password))

def api_create(path_template, team, repo, label, rgb):
    url = api_url(path_template, (team, repo))
    requests.post(url, auth=(username, password), json={'name': label, 'color': rgb})


repos = sys.argv[2:]
if not repos:
    print 'USAGE: %s TEAM REPO1 [ REPO2 ... ]' % sys.argv[0]
    sys.exit(1)
team = sys.argv[1]
username = raw_input('Github username: ')
password = getpass.getpass()

for repo in repos:
    print 'repo: %s' % repo
    url = 'git@github.com:%s/%s.git' % (team, repo)
    dest = '/tmp/github-utils/%s/%s' % (team, repo)
    subprocess.check_call(['git', 'clone', url, dest])
    os.chdir(dest)
    subprocess.check_call(['git', 'checkout', '-b', 'add-one-file'])
    f = open(dest + '/ISSUE_TEMPLATE.md', 'w')
    f.write('''\
* Release number or git hash: 
* Web browser version and OS: 
* Environment (local or deployed): 

### Steps to reproduce

1. 
2. 

### Observed behavior
* Any unexpected output or action (or lack of expected output or action)
* Web browser console errors (including tracebacks)
* Server errors (relevant messages and tracebacks)
* Static or animated images showing the UI behavior

### Expected behavior
*
''')
    f.close()
    subprocess.check_call(['git', 'add', '.'])
    subprocess.check_call(['git', 'commit', '-m', 'add issue template'])
    subprocess.check_call(['git', 'push', 'origin', 'add-one-file'])
