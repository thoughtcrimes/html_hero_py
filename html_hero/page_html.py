# File: html_hero/page_html.py
# Description: This module defines the PageHTML class and related functions.
# Clarity: A page represents a classic .html page that can receive components.

"""This module defines the PageHTML class and related functions."""

import os
import logging
logger = logging.getLogger(__name__)


class PageHTML:
    """
    An object representation of a page text document (html).
    """

    def __init__(self, page_name:str, html_content:str):
        """
        Initializes the HTMLPage instance.

        :param name: The page_name of the page.
        :param html_content: The HTML content of the page.
        """
        self.page_name = page_name
        self.html_content = html_content

    def output_file_path(self) -> str:
        """
        Returns the relative file path intended for the output of the processed HTML page.

        :return: str - The relative file path for the output HTML page.
        """
        return self.page_name

    @property
    def name(self) -> str:
        """
        Property that returns the name of the HTML page.

        :return: str - The name of the page.
        """
        return self.page_name

    @property
    def html(self) -> str:
        """
        Property that returns the HTML content of the page.

        :return: str - The HTML content.
        """
        return self.html_content


def get_pages_from_dir(page_dir:str)  -> list[PageHTML]:
    """
    Recursively scans a directory for .html files, creating a list of PageHTML objects.

    :param page_dir: str - The directory to scan for page HTML files (.html).
    :return: list[PageHTML] - A list of PageHTML objects representing the HTML pages found.
    """

    logger.info("Discovering PageHTMLS (.html) in dir: %s",  page_dir)
    page_htmls:list[PageHTML] = []

    def scan_directory(cur_dir):
        for file in os.listdir(cur_dir):
            file_path = os.path.join(cur_dir, file)
            if os.path.isdir(file_path):
                scan_directory(file_path)
            elif file.endswith('.html'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                    relative_file_path = os.path.relpath(file_path, page_dir)
                    page_htmls.append(PageHTML(relative_file_path, html))
    scan_directory(page_dir)
    logger.info("Total pages found: %s", len(page_htmls))
    page_html_names = ""
    for page_html in page_htmls:
        page_html_names += page_html.name+" "
    logger.info("Pages: %s", page_html_names)
    return page_htmls
