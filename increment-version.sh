#!/bin/bash
set -o errexit
set -o nounset
set -o verbose
#set -o xtrace
set -o pipefail

### Helper functions

die() { echo "$@" 1>&2; exit 1; }
warn() { echo "$@" 1>&2; }

## Main

WORKSPACE=/tmp/phovea-version-workspace/`date +"%Y-%m-%d_%H-%M-%S"`
mkdir -p $WORKSPACE
cd $WORKSPACE
echo "Temporary files in $WORKSPACE"

VERSION='v0.0.4'
MESSAGE='Trying to automate versioning'
REPOS='phovea_core phovea_d3 phovea_vis'
WHOAMI='mccalluc'
BRANCH="$WHOAMI/$VERSION"

for REPO in $REPOS; do
  git clone --depth 1 git@github.com:phovea/$REPO.git -b master
done

for REPO in $REPOS; do
  pushd $REPO
  git checkout -b $BRANCH
  # TODO: increment dependencies
  npm version $VERSION -m "$MESSAGE"
  git add .
  git push --follow-tags origin $BRANCH
  echo "Make PR: https://github.com/phovea/$REPO/compare/$BRANCH?expand=1"
  popd
done



