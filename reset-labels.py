import json
import sys
import getpass
import urllib2
import urllib

def api_read(path_template, *keys):
  url = 'https://api.github.com' + path_template % tuple(map(urllib.quote_plus, keys))
  return json.loads(urllib2.urlopen(url).read())

repos = sys.argv[2:]
if not repos:
  print 'USAGE: %s TEAM REPO1 [ REPO2 ... ]' % sys.argv[0]
  sys.exit(1)
team = sys.argv[1]
username = raw_input('Github username: ')
password = getpass.getpass()

for repo in sys.argv[2:]:
  print repo
  labels = map(lambda label_info: label_info['name'], api_read('/repos/%s/%s/labels', team, repo))
  labeled_issues = api_read('/repos/%s/%s/issues?filter=all&state=all&labels=%s', team, repo, ','.join(labels))
  if labeled_issues:
    print 'Labels are already in use on issues in %s. Deleting them would be destructive.'
    sys.exit(1)
    