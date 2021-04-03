#!/usr/bin/env python3

import argparse
import contextlib
import os
import sys
import glob
from typing import Tuple, Dict, List


def status_and_filename(line: str) -> Tuple[str, str]:
    if "Download complete" in line:
        completed = 1
    else:  # r'Download \w not complete' matches line:
        completed = 0
    filename = os.path.split(line)[1]

    return completed, filename


def missing_files_in_log(logname: str) -> Dict[str, str]:
    with open(logname, "r") as fin:
        filenames = {}
        for line in fin:
            if "NOTICE" in line:
                completed, filename = status_and_filename(line)

                # process multiple downloads
                name, ext = os.path.splitext(filename)
                unique_name = name.rsplit("_")[0] if "_" in name else name

                if unique_name not in filenames:
                    filenames[unique_name] = completed
                else:
                    filenames[unique_name] = max(completed, filenames[unique_name])

        return filenames


def main(args: List[str]) -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "mask",
        type=str,
        nargs="+",
        help="Folders that contains `data_{1,2,3,4,5}` subfolders",
    )
    parser.add_argument(
        "--strict",
        default=False,
        action="store_true",
        help="Whether to fail on file processing errors",
    )

    args = parser.parse_args()

    @contextlib.contextmanager
    def dummycontextmanager(enter_result=None):
        yield enter_result

    if args.strict:
        suppress = dummycontextmanager
    else:
        suppress = contextlib.suppress

    for logname in args.mask:
        with suppress(Exception):
            folder_name = os.path.split(os.path.dirname(os.path.realpath(logname)))[1]
            print(folder_name)
            filenames = missing_files_in_log(logname)
            for filename, downloaded in filenames.items():
                if not downloaded:
                    print(filename)


if __name__ == "__main__":
    main(sys.argv[1:])
