#!/usr/bin/env bash
# source: https://gist.github.com/davemo/88de90577a57698dd72d722bcfc44964
# works with a file called VERSION.txt in the current directory,
# the contents of which should be a semantic version number such as "1.2.3"

NOW="$(date +'%B %d, %Y')"
RED="\033[1;31m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
CYAN="\033[1;36m"
WHITE="\033[1;37m"
RESET="\033[0m"

LATEST_HASH=$(git log --pretty=format:'%h' -n 1)

WARNING_FLAG="${YELLOW}!"
NOTICE_FLAG="${CYAN}❯"

PUSHING_MSG="${NOTICE_FLAG} ${NOW} Pushing new version to the ${WHITE}origin${CYAN}..."

if [ -f VERSION.txt ]; then
    BASE_STRING=$(cat VERSION.txt)
    # shellcheck disable=SC2207 disable=SC2006
    BASE_LIST=(`echo "$BASE_STRING" | tr '.' ' '`)
    V_MAJOR=${BASE_LIST[0]}
    V_MINOR=${BASE_LIST[1]}
    V_PATCH=${BASE_LIST[2]}
    echo -e "${PUSHING_MSG}"
    echo -e "${NOTICE_FLAG} Current version: ${WHITE}$BASE_STRING"
    echo -e "${NOTICE_FLAG} Latest commit hash: ${WHITE}$LATEST_HASH"
    echo -e "${NOTICE_FLAG} V_MAJOR: ${WHITE}$V_MAJOR"
    echo -e "${NOTICE_FLAG} V_MINOR: ${WHITE}$V_MINOR"
    echo -e "${NOTICE_FLAG} V_PATCH: ${WHITE}$V_PATCH"

    if [[ $1 == "patch" ]]; then
        echo -e "Bump patch version"
        NEW_VERSION="$V_MAJOR.$V_MINOR.$((V_PATCH + 1))"
    elif [[ $1 == "minor" ]]; then
        echo -e "Bump minor version"
        NEW_VERSION="$V_MAJOR.$((V_MINOR + 1)).$V_PATCH"
    elif [[ $1 == "major" ]]; then
        echo -e "Bump major version"
        NEW_VERSION="$((V_MAJOR + 1)).$V_MINOR.$V_PATCH"
    else
        echo -e "Bump default patch version"
        NEW_VERSION="$V_MAJOR.$V_MINOR.$((V_PATCH + 1))"
    fi

    echo -e "${NOTICE_FLAG} Bumping to: ${GREEN}$NEW_VERSION"

    echo "$NEW_VERSION" > VERSION.txt
    git add -- VERSION.txt
    git commit -m "${NEW_VERSION}" -- VERSION.txt
    git tag -a -m "${NEW_VERSION}" "v$NEW_VERSION"
    git push origin --follow-tags
else
    echo -e "${WARNING_FLAG} Could not find a VERSION file."
    exit 1;
fi

echo -e "${NOTICE_FLAG} Finished."
