import shutil
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.utils import Copyist


@pytest.fixture()
def create_dirs(tmpdir):
    tmpdir.mkdir("source")
    tmpdir.mkdir("replica")
    dirs = (
        "dir",
        "dir/file",
        "dir/file_1",
        "some_folder",
        "folder",
        "some_folder/file",
    )
    for directory in dirs:
        tmpdir.mkdir(Path("source") / directory)
    return tmpdir, dirs


def test_get_files_and_dirs(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    res = instance._get_files_and_dirs()
    assert sorted((map(str, res[0]))) == sorted(dirs)
    assert res[1] == {}


def test_create_or_copy_from_replica(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    instance._create_or_copy_object_from_source()
    source, replica = instance._get_files_and_dirs()
    for element_source, element_replica in zip(source, replica):
        assert element_replica == element_source


def test_delete_object_from_source(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    instance._create_or_copy_object_from_source()
    shutil.rmtree(f"{base_name}/source/dir/file")
    instance._delete_objects_from_replica()
    source, replica = instance._get_files_and_dirs()
    assert f"{base_name}/source/dir/file" not in source
    for element_source, element_replica in zip(source, replica):
        assert element_replica == element_source


def test_match_source_and_replica(create_dirs):
    logger = Mock()
    base_name, dirs = create_dirs
    instance = Copyist(f"{base_name}/source", f"{base_name}/replica", logger)
    instance.match_source_and_replica()
    source, replica = instance._get_files_and_dirs()
    for element_source, element_replica in zip(source, replica):
        assert element_replica == element_source
