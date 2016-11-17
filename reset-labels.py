import json
import sys
import getpass
import urllib
import httplib 

import requests

def api_url(path_template, keys):
  # print path_template % tuple(map(urllib.quote_plus, keys))
  return 'https://api.github.com' + path_template % tuple(map(urllib.quote, keys))

def api_get(path_template, *keys):
  url = api_url(path_template, keys)
  return requests.get(url).json()
  
def api_delete(path_template, *keys):
  url = api_url(path_template, keys)
  print 'delete: %s' % url
  requests.delete(url, auth=(username, password))
  

repos = sys.argv[2:]
if not repos:
  print 'USAGE: %s TEAM REPO1 [ REPO2 ... ]' % sys.argv[0]
  sys.exit(1)
team = sys.argv[1]
username = raw_input('Github username: ')
password = getpass.getpass()

for repo in repos:
  print 'repo: %s' % repo
  labels = map(lambda label_info: label_info['name'], api_get('/repos/%s/%s/labels', team, repo))
  print 'labels: %s' % labels
  labeled_issues = api_get('/repos/%s/%s/issues?filter=all&state=all&labels=%s', team, repo, ','.join(labels))
  if labels and labeled_issues:
    print 'Labels are already in use on issues in %s: %s. Deleting them would be destructive.' % (repo, labeled_issues)
    sys.exit(1)
  for label in labels:
    api_delete('/repos/%s/%s/labels/%s', team, repo, label)
  