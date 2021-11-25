import os
import shutil
from logging import Logger
from pathlib import Path
from typing import List


class CatalogExistException(BaseException):
    pass


class Copyist:
    """Class that matching catalog source and catalog replica

    :param catalog_source: path to catalog source
    :param catalog_replica: path to catalog replica
    :param logger: instance of logger object
    """

    def __init__(self, catalog_source: str, catalog_replica: str, logger: Logger):
        self.logger = logger
        if not Path.exists(Path(catalog_source)) or not Path.exists(
            Path(catalog_replica)
        ):
            self.logger.error(
                f"{CatalogExistException} Catalogs {catalog_source} "
                f"or {catalog_replica} are not exist"
            )
            raise CatalogExistException(
                f"Catalogs {catalog_source} or " f"{catalog_replica} are not exist"
            )
        self.catalog_source = Path(catalog_source)
        self.catalog_replica = Path(catalog_replica)

    def _get_files_and_dirs(self) -> List:
        """Return list with files in catalog source
        and catalog replica directories

        :return: list with files in catalog source in index 0 and
         list with files in catalog replica in index 1"""
        result = []
        for catalog in (self.catalog_source, self.catalog_replica):
            result.append(
                {
                    file.relative_to(catalog): os.path.getmtime(file)
                    for file in catalog.glob("**/*")
                }
            )
        return result

    def _delete_objects_from_replica(self) -> None:
        """Delete objects in replica that not exist in source"""

        files_source, files_replica = self._get_files_and_dirs()
        for obj in sorted(files_replica):
            if obj not in files_source:
                if (self.catalog_replica / obj).is_dir():
                    self.logger.info(f"Delete directory {obj}")
                    shutil.rmtree(self.catalog_replica / obj)
                else:
                    if (self.catalog_replica / obj).exists():
                        self.logger.info(f"Delete file {obj}")
                        os.remove(self.catalog_replica / obj)

    def _create_or_copy_object_from_source(self) -> None:
        """Create or copy objects from source to replica"""

        files_source, files_replica = self._get_files_and_dirs()
        for obj in sorted(files_source):
            if obj not in files_replica:
                if (self.catalog_source / obj).is_dir():
                    self.logger.info(f"Create directory {obj}")
                    new_directory = self.catalog_replica / obj
                    new_directory.mkdir()
                else:
                    self.logger.info(f"Copy file {obj}")
                    shutil.copy(self.catalog_source / obj, self.catalog_replica / obj)
            else:
                if not (self.catalog_source / obj).is_dir():
                    if files_source[obj] > files_replica[obj]:
                        self.logger.info(f"Copy modified file {obj}")
                        shutil.copy(
                            self.catalog_source / obj, self.catalog_replica / obj
                        )

    def match_source_and_replica(self) -> None:
        """Match replica and source folders"""

        self._delete_objects_from_replica()
        self._create_or_copy_object_from_source()
