"""File loader."""

import logging
import os
from sys import stdout
from typing import List

import base_loader.model as model
from base_loader.model.entity import Entity
from base_loader.persistence import source, target
import base_loader.queries as queries

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s [%(filename)s:%(lineno)d]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=stdout,
)

logger = logging.getLogger(__name__)


class Loader:
    """Loader class for astec files data."""

    _entities = {
        "astec": Entity.ASTEC,
        "market_cap": Entity.MARKET_CAP,
        "returns": Entity.RETURNS,
        "shares_out": Entity.SHARES_OUT,
        "volume": Entity.VOLUME
    }

    _source_dirs = {
        Entity.ASTEC: "astec",
        Entity.MARKET_CAP: "market_cap",
        Entity.RETURNS: "returns",
        Entity.SHARES_OUT: "shares_out",
        Entity.VOLUME: "volume"
    }

    _model_type = {
        Entity.ASTEC: model.Astec,
        Entity.MARKET_CAP: model.MarketCap,
        Entity.RETURNS: model.Returns,
        Entity.SHARES_OUT: model.SharesOut,
        Entity.VOLUME: model.Volume,
    }

    _queries = {
        Entity.ASTEC: queries.AstecQueries,
        Entity.MARKET_CAP: queries.MarketCapQueries,
        Entity.RETURNS: queries.ReturnsQueries,
        Entity.SHARES_OUT: queries.SharesOutQueries,
        Entity.VOLUME: queries.VolumeQueries,
    }

    def __init__(self) -> None:
        self.source = source.Source(os.environ.get("SOURCE"))
        self.target = target.Target(os.environ.get("TARGET"))

    def run(self, true_base=False) -> None:
        """Persists tables."""
        for entity in self._entities.values():
            logger.info(f"Starting to process {entity}...")

            transpose = False
            if entity == Entity.SHARES_OUT:
                transpose = True

            unflatten = True
            if entity == Entity.ASTEC:
                unflatten = False

            self.source.set_source_dir(self._source_dirs[entity])
            i = 0
            for file in os.listdir(self.source.source_dir):
                logger.info(f"{i}/{len(os.listdir(self.source.source_dir))} files persisted.")
                raw_records = self.source.get_records(
                    file_name=file, unflatten=unflatten, transpose=transpose
                )
                raw_records = self.list_slicer(raw_records, 1_000_000)
                n = len(raw_records)

                while raw_records:
                    logger.info(f"Processed {n - len(raw_records)}/{n} million records")
                    logger.info("Modeling...")
                    records = []
                    for r in raw_records[0]:
                        record = self._model_type[entity].build_record(r)
                        if not record.is_empty and not record.is_weekend:
                            if not true_base:
                                if entity == Entity.RETURNS:
                                    record.move_date_backwards()
                                else:
                                    record.move_date_forward()
                            records.append(record.as_tuple())
                    del raw_records[0]

                    records = self.list_slicer(records, 250_000)
                    j = 0
                    logger.info("Executing records")
                    for records_slice in records:
                        logger.debug(f"{j * 250_000}/{1_000_000} records executed.")
                        if not true_base:
                            self.target.execute(self._queries[entity].UPSERT.format(tbl='daily_base'), records_slice)
                        else:
                            self.target.execute(self._queries[entity].UPSERT.format(tbl='true_base'), records_slice)
                        j += 1

                self.target.commit_transaction()
                i += 1
            logger.info(f"{entity} persisted.")

        logger.info("Process finished.")

    def cleanup(self):
        """Restricts universe to U.S. and removes every useless records from the data"""
        # CHANGE VOLUME CONSTRAINTS BELOW IF NEEDED
        query1 = (
            "DELETE "
            "FROM daily_base "
            "WHERE market_cap < 100 "
            "OR volume < 1000000 "
            "OR market_cap IS NULL "
            "OR volume IS NULL "
            "OR rtn IS NULL;"
        )
        query2 = (
            "DELETE "
            "FROM daily_base "
            "WHERE utilization_pct IS NULL "
            "AND bar IS NULL "
            "AND age IS NULL "
            "AND tickets IS NULL "
            "AND units IS NULL "
            "AND market_value_usd IS NULL "
            "AND loan_rate_avg IS NULL "
            "AND loan_rate_max IS NULL "
            "AND loan_rate_min IS NULL "
            "AND loan_rate_range IS NULL "
            "AND loan_rate_stdev IS NULL;"
        )
        query3 = (
            "DELETE "
            "FROM daily_base "
            "WHERE (gvkey) IN (VALUES %s);"
        )
        logger.info("Cleaning daily_base table...")
        logger.info("Removing invalid records (no market_cap/no volume/returns data/below thresholds)...")
        self.target.execute_query(query1)
        self.target.commit_transaction()

        logger.info("Removing invalid records (no astec data)...")
        self.target.execute_query(query2)
        self.target.commit_transaction()

        logger.info("Restricting to U.S. gvkeys only...")
        us_keys = set(self.target.fetch_us_keys())
        keys = set(self.target.fetch_keys())
        invalid_keys = list(keys - us_keys)
        n = len(invalid_keys)

        invalid_keys = self.list_slicer(invalid_keys, 100)
        i = 0
        for keys_slice in invalid_keys:
            logger.debug(f"Deleted {i * 100}/{n} invalid keys.")
            self.target.execute(query3, keys_slice)
            self.target.commit_transaction()
            i += 1

        logger.debug(f"Deleted {n}/{n} invalid keys.")
        logger.info("daily_base is now composed only of valid U.S. records.")

    @staticmethod
    def list_slicer(lst: List, slice_len: int) -> List[List]:
        """Slice list into list of lists.

        Args:
            lst: list to slice.
            slice_len: size of each slice.

        Returns:
            Sliced list.
        """
        res = []
        i = 0
        while i + slice_len < len(lst):
            res.append(lst[i : i + slice_len])  # noqa
            i = i + slice_len
        res.append(lst[i:])
        return res


loader = Loader()
loader.run()
loader.cleanup()

loader.run(true_base=True)
