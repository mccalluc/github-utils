#!/bin/bash
set -o errexit
set -o nounset
#set -o verbose
#set -o xtrace
set -o pipefail

### Helper functions

die() { echo "$@" 1>&2; exit 1; }
warn() { echo "$@" 1>&2; }

## Main

# With nounset, we need to assign defaults here.
export VERSION=${1:-''} # Needs to be visible in perl subprocess below.
MESSAGE=${2:-''}

if [[ $VERSION != 'v0.0.'* ]] || [[ $MESSAGE != *' '* ]]; then
  die "USAGE: $0 v0.0.X 'Multi-word message'"
fi

REPOS='phovea_core phovea_d3 phovea_vis'
BRANCH=`whoami`/$VERSION # Branch name must be distinct from tag name

WORKSPACE=/tmp/phovea-version-workspace/`date +"%Y-%m-%d_%H-%M-%S"`
mkdir -p $WORKSPACE
cd $WORKSPACE
echo "Temporary files in $WORKSPACE"

for REPO in $REPOS; do
  git clone --depth 1 git@github.com:phovea/$REPO.git -b master
done

for REPO in $REPOS; do
  pushd $REPO
  git checkout -b $BRANCH
  perl -i -pne 's{(github:phovea/\w+#)v\d+\.\d+\.\d+}{$1$ENV{VERSION}}' package.json
  git add .
  git commit -m 'update dependencies' || warn "No dependencies updated in $REPO"
  npm version $VERSION -m "$MESSAGE"
  popd
done

# Make sure everything has worked for all repos before trying to push.
for REPO in $REPOS; do
  pushd $REPO
  git push --follow-tags origin $BRANCH
  popd
done
echo
for REPO in $REPOS; do
  echo "Make PR: https://github.com/phovea/$REPO/compare/$BRANCH?expand=1"
done


