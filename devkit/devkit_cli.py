import sys
import os
import yaml

from subprocess import call

from git import Repo
from tabulate import tabulate


# Show branches
# Commit and push all changes in all repos
# Run a docker compose?
# Checkout same branch in all repos
# Housekeep - remote prune

def load(file_descriptor):
    return yaml.load(file_descriptor, Loader=yaml.Loader)


def run(config_file):
    config = yaml_loader(config_file)

    home = config['manage']['base_dir']
    print("home is: ", home)

    repos = config['manage']['repositories'].items()

    for repo_name, repo_url in repos.__iter__():
        print("name: ", repo_name)
        print("value: ", repo_url)
        Repo.clone_from(repo_url, home + repo_name)


def yaml_loader(filepath):
    """Loads a yaml file"""
    with open(filepath, "r") as file_descriptor:
        print("file descriptor is: ", file_descriptor)
        data = load(file_descriptor)
    return data


def dispatcher(command):
    if command == ['update']:
        update("options")
    elif command == ['build']:
        build("options")
    elif command == ['info']:
        info()
    elif command == ['setup']:
        setup()


def init():
    config = yaml_loader("resources/devkit.yml")
    home = config['manage']['base_dir']
    print("home is: ", home)
    repos = config['manage']['repositories'].items()
    return home, repos


def info():
    home, repos = init()

    t = []
    for repo_name, repo_url in repos.__iter__():
        repo = Repo(home + repo_name)
        res = repo.active_branch
        t.append([repo_name, res.name, repo.is_dirty()])
    print(tabulate(t, headers=['repo', 'branch', 'changes?']))


def update(options):
    print("update the repos with ", options)

    home, repos = init()

    for repo_name, repo_url in repos.__iter__():
        print("updating: " + home + repo_name)
        repo = Repo(home + repo_name)
        res = repo.git.pull("--rebase")
        print(res)


def build(options):
    print("build project with ", options)

    home, repos = init()

    print("--------------------------------")
    for repo_name, repo_url in repos.__iter__():
        with open(os.devnull, "w") as f:
            print("Building " + repo_name, end='')
            res = call(["./gradlew", "build"], cwd=str(home + repo_name), stdout=f)
            if res == 0:
                print("\t\u2713")
            else:
                print('X')
        print("--------------------------------")


def setup():
    run("resources/devkit.yml")


def main():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    dispatcher(command=sys.argv[1:])


if __name__ == '__main__':
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    dispatcher(sys.argv[1:])
