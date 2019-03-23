# devkit

## Overview

A tool for setup and lifecycle management of projects made up of components in multiple git repositories and using a variety of development tools.

TODO:
1. Define system software required to be installed, e.g. homebrew, sdkman, docker
2. Define which repos need to be pulled from git

## Quick start

### Create a virtual environment for use with devkit

Create a folder for all your virtual environments if you don't already have one.  In your virtual environments
folder create a new virtual environment for devkit:

1. Create a virtual environment `python3 -m venv devkit`
2. Activate the virtual environment `source devkit/bin/activate`
3. Get the latest version of pip `pip install --upgrade pip`
4. Install latest version of pipenv into virtual environment `pip install pipenv`

### Configure the virtual environment for devkit

Assuming you have at least python 3.6 installed in an activated virtual environment.

1. `pipenv install` download the packages defined in `Pipfile`
2. Test installation by setting up the example projects `./devkit.sh setup`

This will clone the projects listed in `resources\devkit.yml`.  The example configuration
uses a folder called sandbox which is assumed to be a sub-folder of the folder from
which the `devkit.sh` shell script is executed.

## Utilities

1. Script to build all the repos.
2. docker-compose definition to run the applications locally
3. Script to update all repos

## Additional information

1. What branches to build from?
2. What tools to use to build.  Could detect this.

## Improvements

1. Config file to define:
    * the projects being managed (i.e. git urls) 
    * the default branch to work from in each repo
    * project specific branch overrides
    * define relationships between services to allow docker-compose to be auto-generated?
2. Command line utility that takes commands and options.  devkit update --all --exclude=<proj> devkit update <proj>
3. Option to pipe logs to log file or dev/null and just see a summary for builds
4. Halt the build all if a module build fails
5. An info command that summarises what's checked out, what has pending changes, etc.
