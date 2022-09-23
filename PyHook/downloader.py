"""
downloader for PyHook
~~~~~~~~~~~~~~~~~~~~~~~
Simple file downloader
:copyright: (c) 2022 by Dominik Wojtasik.
:license: MIT, see LICENSE for more details.
"""

import re
import sys
from os.path import basename, exists, getsize
from urllib.parse import unquote, urlparse

import requests

_CHUNK_SIZE = 4096
_FILENAME_REGEX = re.compile(r"^.*?filename=\"(.*?)\";.*$")


def _print(text: str) -> None:
    """Prints directly to OS console.

    Args:
        text (str): Text to print.
    """
    sys.stdout.write(text)
    sys.stdout.flush()


def download_file(url: str, directory: str) -> None:
    """Download file from given url and save it into directory.

    Args:
        url (str): The url to given file.
        directory (str): The directory to save downloaded file.
    """
    response_stream = requests.get(url, stream=True, timeout=10)
    response_stream.raise_for_status()
    if url.startswith("https://drive.google.com"):
        filename = _FILENAME_REGEX.match(response_stream.headers["Content-Disposition"]).group(1)
    else:
        filename = unquote(basename(urlparse(url).path))
    filepath = f"{directory}\\{filename}"
    filesize = int(response_stream.headers["Content-Length"])
    byte_count = 0
    if not exists(filepath) or getsize(filepath) != filesize:
        with open(filepath, "wb") as d_file:

            _print(f"--- Downloading file: {filename}\n")
            for chunk in response_stream.iter_content(_CHUNK_SIZE):
                d_file.write(chunk)
                byte_count += _CHUNK_SIZE
                if byte_count > filesize:
                    byte_count = filesize
                _print(f"---- Progress: {byte_count / filesize * 100:.2f}%\r")
            _print("\n")
