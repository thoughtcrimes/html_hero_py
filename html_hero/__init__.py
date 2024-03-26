# File: html_hero/__init__.py
# Description: The bottom most package __init__.py for html_hero.

"""Package for html_hero."""

import logging
logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)

from . import apply_components_task as _apply_components

def apply_components_from_dirs(page_dir,component_dir,output_dir):
    """
    Helper function to start the process of applying the components into the pages.

    :param page_dir: str - Directory to get pages from.
    :param component_dir: str - Directory to get components from.
    :param output_dir: str - Directory to output the baked pages to.
    """

    apply_components = _apply_components.ApplyComponentsTask()
    apply_components.apply_components_from_dirs(page_dir,component_dir,output_dir)
