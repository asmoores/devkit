import pytest
import os

from shutil import copyfile
from pathlib import Path

from devkit import devkit_cli


@pytest.fixture
def basic_resource_file(tmpdir):
    os.mkdir(tmpdir.join('resources'))
    basic_resource_file = tmpdir.join('resources/basic_devkit.yml')
    file = open(str(basic_resource_file), 'w')
    file.write('{"test": "value"}')
    file.close()
    return basic_resource_file


@pytest.fixture()
def resource_file(tmpdir):
    resource_file = tmpdir.join('resources/devkit.yml')
    cwd = os.getcwd()
    print("cwd:: " + os.getcwd())
    print("parent:: " + str(Path().resolve().parent))
    print("dest:: " + str(resource_file))
    os.mkdir(tmpdir.join('resources'))
    copyfile(str(Path().resolve().parent) + '/resources/devkit.yml', str(resource_file))
    os.chdir(tmpdir)
    for entry in os.scandir(os.curdir):
        if entry.is_file():
            print("fixture found file:: " + entry.name)
        else:
            print("fixture found dir:: " + entry.name)
    yield resource_file
    os.chdir(cwd)


def test_setup(resource_file):
    # WHEN
    devkit_cli.run(resource_file)

    # THEN
    for entry in os.scandir(os.curdir + "/sandbox"):
        if entry.is_file():
            print("test found file:: " + entry.name)
        else:
            print("test found dir:: " + entry.name)
            assert(any(entry.name in x for x in ['deployer', 'lookup-service', 'publish-service', 'webui']))
    assert(1 == 1)


def test_yaml_loader(basic_resource_file):
    # WHEN
    test_result = devkit_cli.yaml_loader(str(basic_resource_file))

    # THEN
    assert test_result == {"test": "value"}
