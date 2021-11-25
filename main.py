import time

import click

from src.log import configure_logging
from src.utils import Copyist


@click.command()
@click.option("--catalog-source", type=str)
@click.option("--catalog-replica", type=str)
@click.option("--period", type=int)
@click.option("--path-log", type=str)
def run(catalog_source: str, catalog_replica: str, period: int, path_log: str) -> None:
    logger = configure_logging(path_log)
    instance = Copyist(catalog_source, catalog_replica, logger)
    while True:
        instance.match_source_and_replica()
        time.sleep(period)


if __name__ == "__main__":
    run()
