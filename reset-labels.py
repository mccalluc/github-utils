import sys
import getpass
import urllib
import requests


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
    labels = map(lambda label_info: label_info['name'], api_get('/repos/%s/%s/labels', team, repo))
    print 'labels: %s' % labels
    labeled_issues = api_get('/repos/%s/%s/issues?filter=all&state=all&labels=%s', team, repo, ','.join(labels))
    if labels and labeled_issues:
        print 'Labels are already in use on issues in %s: %s. Deleting them would be destructive.' % (
        repo, labeled_issues)
        sys.exit(1)
    for label in labels:
        api_delete('/repos/%s/%s/labels/%s', team, repo, label)

new_labels = {
    # Type
    'Bug': 'db2d1a',
    'Technical Debt': '9c2011',
    'Question': '76429a',
    'Enhancement': '09457f',
    'Feature': '1779dc',
    # Severity
    'Critical': 'dc6b24',
    'Important': 'f28f2e'
}

for repo in repos:
    for label, rgb in new_labels.iteritems():
        api_create('/repos/%s/%s/labels', team, repo, label, rgb)
