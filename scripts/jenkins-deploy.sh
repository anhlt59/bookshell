export BRANCH=Ver1.0.1/CINCPAW03-75
export STAGE=tr0-1
export STACK=paweb
export REGION=eu-central-1

git stash
git fetch -a
git checkout $BRANCH
git reset --h origin/$BRANCH
git push paw

export CRUMB=$(curl -u 'anhlt87:12345678' -s 'http://18.198.120.144:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,": ",//crumb)')
curl -u "anhlt87:12345678" -H $CRUMB \
    -X POST http://18.198.120.144:8080/job/PAW/job/DEVELOPMENT/job/deploy.slave-node/buildWithParameters?stack=${STACK}&stage=${STAGE}&region=${REGION}&branch=${BRANCH}
