# File: html_hero/apply_components_task.py
# Description: Task to apply HTML components into pages.

"""This module provides classes and functions for managing HTML components."""

import os
import json
import logging
import re
from . import component_html,page_html

logger = logging.getLogger(__name__)

class ApplyComponentsTask:
    """
    The task which applys components into pages.
    """

    def __init__(self):
        """
        Initializes the ApplyComponentsTask instance.
        """
        self.component_objs = []
        self.page_objs = []

    def get_component_obj_by_name(self, component_name:str) -> component_html.ComponentHTML:
        """
        Gets a registered component by name.

        :param component_name: str - The name of the component.
        :return: ComponentHTML - The ComponentHTML or None if it's not found.
        """

        for component_obj in self.component_objs:
            if component_obj.name == component_name:
                return component_obj
        return None


    def apply_components_from_dirs(self, page_dir:str, component_dir:str, output_dir:str):
        """
        Starts the process of applying the components into the pages.

        :param page_dir: str - Directory to get pages from.
        :param component_dir: str - Directory to get components from.
        :param output_dir: str - Directory to output the baked pages to.
        """

        logger.info("ApplyComponentsTask apply_components...")
        logger.info("page_dir: %s", page_dir)
        logger.info("component_dir: %s", component_dir)
        logger.info("output_dir: %s", output_dir)

        if not os.path.exists(page_dir):
            logger.error("The page_dir does not exist.")
            return

        if not os.path.exists(component_dir):
            logger.error("The component_dir does not exist.")
            return

        if not os.path.exists(output_dir):
            logger.error("The output_dir does not exist.")
            return

        self.component_objs = component_html.get_components_from_dir(component_dir)
        self.page_objs = page_html.get_pages_from_dir(page_dir)


        logger.info("Applying components to pages...")
        baked_page_objs:list[page_html.PageHTML] = []

        for page_obj in self.page_objs:
            # Replace patterns using the process_json method
            baked_html = re.sub(r'<!--JSON(\{.+?\})-->',
                            lambda match: self.process_json(match.group(1)),
                            page_obj.html)

            baked_page_objs.append(page_html.PageHTML(page_obj.name,baked_html))

        logger.info("Outputing pages...")
        for baked_page_obj in baked_page_objs:
            page_obj_output_dir = os.path.join(output_dir, baked_page_obj.output_file_path())
            os.makedirs(os.path.dirname(page_obj_output_dir), exist_ok=True)
            with open(page_obj_output_dir, 'w', encoding='utf-8') as f:
                f.write(baked_page_obj.html)

        logger.info("Apply Components complete!\n")

    def process_json(self, json_string:str):
        """
        Processes the extracted json string from a component insertion.

        :param json_string: str - The json string extracted from the component data.
        """

        valid_json_string = json_string.replace("'", '"')
        json_data = json.loads(valid_json_string)
        if json_data['type'] == 'component':
            component_obj = self.get_component_obj_by_name(json_data['id'])
            if component_obj:
                return component_obj.html
        return "<!-- JSON " + json_string + " -->"


def apply_components_from_dirs(page_dir,component_dir,output_dir):
    """
    Helper function to start the process of applying the components into the pages.

    :param page_dir: str - Directory to get pages from.
    :param component_dir: str - Directory to get components from.
    :param output_dir: str - Directory to output the baked pages to.
    """
    apply_components = ApplyComponentsTask()
    apply_components.apply_components_from_dirs(page_dir,component_dir,output_dir)
