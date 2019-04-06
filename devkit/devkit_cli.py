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

    projects = config['manage']['projects']

    for project in projects.__iter__():
        print("name: ", project['name'])
        print("value: ", project['url'])
        Repo.clone_from(project['url'], home + project['name'])


def yaml_loader(filepath):
    """Loads a yaml file"""
    with open(filepath, "r") as file_descriptor:
        # print("file descriptor is: ", file_descriptor)
        data = load(file_descriptor)
    return data


def dispatcher(command):
    """
    Dispatcher function that passes control to the function that implements the required command.

    :param command: String name of command
    :return: nothing

    This approach works until we need to pass options to the commands.

    Create a dictionary (each time so not performant) and use the command call parameter to index
    into the dictionary and execute the function stored as the value of the key value pair. Provide
    a default function to avoid a KeyError

    """

    {
        'update': update,
        'build': build,
        'info': info,
        'setup': setup,
        'status': status,
        'clean': housekeeping,
    }.get(command, default_command)()


def default_command():
    print("Explain what commands are available")


def init():
    config = yaml_loader("resources/devkit.yml")
    home = config['manage']['base_dir']
    print("home is: ", home)
    projects = config['manage']['projects']
    return home, projects


def info():
    home, projects = init()

    t = []
    for project in projects.__iter__():
        repo = Repo(home + project['name'])
        t.append([project['name'], project['url'], project['build']])
    print(tabulate(t, headers=['project', 'url', 'build']))


def status():
    home, projects = init()

    t = []
    for project in projects.__iter__():
        repo = Repo(home + project['name'])
        # If HEAD is a detached then gitpython returns TypeError, this error happens if a tag is checked out
        try:
            branch_or_tag = repo.active_branch.name
        except TypeError:
            branch_or_tag = repo.git.describe()
        t.append([project['name'], branch_or_tag, repo.is_dirty(), repo.head.commit.summary])
    print(tabulate(t, headers=['project', 'branch', 'local changes', 'latest commit']))


def update(options):
    print("update the repos with ", options)

    home, projects = init()

    for project in projects.__iter__():
        print("updating: " + home + project['name'])
        repo = Repo(home + project['name'])
        res = repo.git.pull("--rebase")
        print(res)


def build(options):
    print("build project with ", options)

    home, projects = init()

    print("--------------------------------")
    for project in projects.__iter__():
        with open(os.devnull, "w") as f:
            print("Building " + project['name'], end='')
            if project['build'] == 'gradle':
                res = call(["./gradlew", "build"], cwd=str(home + project['name']), stdout=f)
            elif project['build'] == 'maven':
                res = call(["mvn", "clean", "install"], cwd=str(home + project['name']), stdout=f)
            else:
                print("Unknown type of build.")
                res = 1
            if res == 0:
                print("\t\u2713")
            else:
                print('X')
        print("--------------------------------")


def housekeeping():
    print("housekeeping")

    home, projects = init()

    for project in projects.__iter__():
        print("cleaning: " + home + project['name'])
        repo = Repo(home + project['name'])
        result = repo.git.remote("prune", ".")
        print(result)


def setup():
    run("resources/devkit.yml")


def main():
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    dispatcher(command=sys.argv[1:][0])


if __name__ == '__main__':
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    dispatcher(sys.argv[1:])
