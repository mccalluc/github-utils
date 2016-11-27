import sys
import getpass
import urllib
import requests
import subprocess
import os


repos = sys.argv[2:]
if not repos:
    print 'USAGE: %s TEAM REPO1 [ REPO2 ... ]' % sys.argv[0]
    sys.exit(1)
team = sys.argv[1]
branch = 'add-issue-template'
message = 'Add issue template'

for repo in repos:
    print 'repo: %s' % repo
    url = 'git@github.com:%s/%s.git' % (team, repo)
    dest = '/tmp/github-utils/%s/%s' % (team, repo)
    subprocess.check_call(['git', 'clone', '--depth', '1', url, dest])
    os.chdir(dest)
    subprocess.check_call(['git', 'checkout', '-b', branch])
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
    subprocess.check_call(['git', 'commit', '-m', message])
    subprocess.check_call(['git', 'push', 'origin', branch])
