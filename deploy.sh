#!/bin/bash

VERSION=`python -c "import sys ; print('{0}.{1}'.format(sys.version_info.major, sys.version_info.minor))"` 

if [ $VERSION == '2.7' ]; then
    rm -rf .git*
    gem install heroku
      # Turn off warnings about SSH keys:
    echo "Host heroku.com" >> ~/.ssh/config
    echo "   StrictHostKeyChecking no" >> ~/.ssh/config
    echo "   CheckHostIP no" >> ~/.ssh/config
    echo "   UserKnownHostsFile=/dev/null" >> ~/.ssh/config
    # Clear your current Heroku SSH keys:
    heroku keys:clear
    # Add a new SSH key to Heroku
    yes | heroku keys:add
    # Add your Heroku git repo:
    git clone -b working git@heroku.com:creme-fraiche.git heroku
    cd heroku
    # Install the Heroku gem (or the Heroku toolbelt)
    wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
    heroku plugins:install https://github.com/ddollar/heroku-anvil
    heroku build -r creme-fraiche
fi