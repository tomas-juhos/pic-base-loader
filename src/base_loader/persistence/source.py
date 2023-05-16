"""Source."""
import logging
import os
from pathlib import Path
import pyarrow.parquet as pq
from typing import List, Tuple

logger = logging.getLogger(__name__)


class Source:
    """Source class."""

    source_dir: str

    def __init__(self, source: str) -> None:
        self.source = self.set_source(source)

    @staticmethod
    def set_source(source: str):
        """Sets path to the directory 'local_data'.

        Returns:
            Absolute path to the source .
        """
        local_data_path = os.path.join(
            Path(os.path.abspath(os.curdir)).parent.parent, source
        )

        return local_data_path

    def set_source_dir(self, source_dir: str):
        """Sets path to the directory 'local_data'.

        Returns:
            Absolute path to the source directory.
        """
        self.source_dir = os.path.join(Path(self.source, source_dir))

    def set_source_file(self, file_name: str) -> str:
        """Sets path to the desired target directory in 'local_data'.

        Args:
            file_name: source directory inside 'local_data'.

        Returns:
            Absolute path to the source file.
        """
        local_data_path = self.source_dir
        return os.path.join(local_data_path, file_name)

    def get_records(
        self, file_name, unflatten: bool, transpose: bool = False
    ) -> List[Tuple]:
        """Returns all records from file in the source directory.

        Returns:
            List of records, which are lists.
        """
        file_path = self.set_source_file(file_name)
        logger.info("Unpacking file...")
        table = pq.read_table(file_path)
        logger.info("Building dataframe...")
        df = table.to_pandas()
        if transpose:
            df = df.transpose()
        if unflatten:
            logger.info("Unflattening...")
            records = self.unflatten(df)
        else:
            records = df.to_records()
        del df
        logger.info("Records generated.")

        return records

    @staticmethod
    def unflatten(df) -> List[Tuple]:
        dictionary = df.to_dict()
        records = []
        i = 0
        for gvkey in dictionary.keys():
            if i % 1000 == 0:
                logger.debug(f"{i}/{len(dictionary.keys())} gvkeys resolved.")
            for date in dictionary[gvkey].keys():
                records.append((gvkey, date, dictionary[gvkey][date]))
            i += 1
        return records
