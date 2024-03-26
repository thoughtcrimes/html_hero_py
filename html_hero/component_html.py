# File: html_hero/component_html.py
# Description: Simple components made from HTML and simple data injection.

"""Simple HTML based components that recieve json data (chtml)."""

import os
import logging
logger = logging.getLogger(__name__)

class ComponentHTML:
    """
    An object representation of a component text document (chtml).
    """

    def __init__(self, component_name, source_html):
        """
        Initializes the ComponentHTML instance.

        :param component_name: The name of the component.
        :param source_html: The HTML content of the component.
        """
        self.component_name = component_name
        self.source_html = source_html

    @property
    def name(self) -> str:
        """
        Property that returns the name of the component.

        :return: str - The name of the component.
        """
        return self.component_name

    @property
    def html(self) -> str:
        """
        Property that returns the HTML content of the component.

        :return: str - The HTML content.
        """
        return self.source_html


def get_components_from_dir(component_dir:str) -> list[ComponentHTML]:
    """
    Scans a directory for .chtml files and creates a list of ComponentHTML objects from them.

    :param component_dir: str - The directory to scan for component HTML files (.chtml).
    :return: list[ComponentHTML] - A list of ComponentHTML objects found in the directory.
    """

    logger.info("Discovering ComponentHTMLS (.chtml) in dir: %s... ", component_dir)
    components:list[ComponentHTML] = []

    for file in sorted(os.listdir(component_dir), reverse=True):
        if file.endswith('.chtml'):
            file_path = os.path.join(component_dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
                components.append(ComponentHTML(os.path.splitext(file)[0], html))
    logger.info("Total components: %s", len(components))
    output = ""
    for component in components:
        output += component.name+" "
    logger.info("Components: %s", output)
    return components
