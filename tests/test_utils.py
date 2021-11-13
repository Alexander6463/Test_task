import shutil
from src.utils import Copyist
from unittest.mock import Mock
from pathlib import Path

import pytest


@pytest.fixture()
def create_dirs(tmpdir):
    tmpdir.mkdir("source")
    tmpdir.mkdir("replica")
    files_source = (
        "dir",
        "dir/file.txt",
        "dir/file_1.txt",
        "asdf",
        "qqwer",
        "asdf/file.txt")
    for file in files_source:
        tmpdir.mkdir(Path("source") / file)
    return tmpdir, files_source


def test_get_files_and_dirs(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    res = instance._get_files_and_dirs()
    assert sorted((map(str,res[0]))) == sorted(dirs)
    assert res[1] == set()


def test_create_or_copy_from_replica(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    instance._create_or_copy_object_from_source()
    source, replica = instance._get_files_and_dirs()
    assert source == replica


def test_delete_object_from_source(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    instance._create_or_copy_object_from_source()
    shutil.rmtree(f"{base_name}/source/dir/file.txt")
    instance._delete_objects_from_replica()
    source, replica = instance._get_files_and_dirs()
    assert f"{base_name}/source/dir/file.txt" not in source
    assert source == replica


def test_match_source_and_replica(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    instance.match_source_and_replica()
    source, replica = instance._get_files_and_dirs()
    assert source == replica