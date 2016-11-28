import sys
import getpass
import urllib
import requests


def api_url(path_template, keys):
    # print path_template % tuple(map(urllib.quote_plus, keys))
    return 'https://api.github.com' + path_template % tuple(map(urllib.quote, keys))

def api_get(path_template, *keys):
    url = api_url(path_template, keys)
    return requests.get(url, auth=(username, password)).json()

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
    labels = map(lambda label_info: label_info['name'], api_get('/repos/%s/%s/labels', team, repo))
    print 'old labels: %s' % labels
    for label in labels:
        labeled_issues = api_get('/repos/%s/%s/issues?filter=all&state=all&labels=%s', team, repo, label)
        if labeled_issues:
            print 'Keeping "%s" in "%s" because it is in use' % (label, repo)
        else:
            print 'Deleting label "%s"' % label
            api_delete('/repos/%s/%s/labels/%s', team, repo, label)

new_labels = [ # (Same structure as https://api.github.com/repos/phovea/phovea.github.io/labels)
  {
    "name": "Layer: API",
    "color": "bbbbbb"
  },
  {
    "name": "Layer: Client",
    "color": "aaaaaa"
  },
  {
    "name": "Layer: Server",
    "color": "999999"
  },
  {
    "name": "Layer: UI",
    "color": "cccccc"
  },
  {
    "name": "Severity: Critical",
    "color": "fbca04"
  },
  {
    "name": "Severity: Important",
    "color": "fef2c0"
  },
  {
    "name": "Type: Bug",
    "color": "db2d1a"
  },
  {
    "name": "Type: Enhancement",
    "color": "09457f"
  },
  {
    "name": "Type: Feature",
    "color": "1779dc"
  },
  {
    "name": "Type: Question",
    "color": "76429a"
  },
  {
    "name": "Type: Technical Debt",
    "color": "9c2011"
  }
]

for repo in repos:
    for label in new_labels:
        print 'Creating label "%s"' % label['name']
        api_create('/repos/%s/%s/labels', team, repo, label['name'], label['color'])
