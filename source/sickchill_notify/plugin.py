#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
example_postprocessor_task_results

Docs:
    https://docs.unmanic.app/docs/plugins/writing_plugins/plugin_runner_types/#post-processor---marking-task-successfailure

"""
import requests
from unmanic.libs.unplugins.settings import PluginSettings


class Settings(PluginSettings):
    settings = {
        "host": "https://localhost:8081",
        "api_key": "",
        "verify_ssl": False,
    }


def notify(source_data, destination, settings):
    # Set sickchills host and api key
    url = f"{settings['host']}/api/{settings['api_key']}/?cmd="

    # collect all shows
    abs_path = [i for i in source_data["abspath"].split("/") if i]
    get_all_shows = f"{url}shows"
    result = requests.get(get_all_shows, verify=settings["verify_ssl"])
    show = None
    if "data" in result.json():
        data_selection = result.json()["data"]
        for r in data_selection:
            show_name = data_selection[r]["show_name"].lower()
            if abs_path[-2].lower() in show_name:
                show = data_selection[r]

    if show:
        print(show)
        update_show = f"{url}show.update"
        result = requests.post(
            update_show, json={"tvdbid": show["tvdbid"]}, verify=settings["verify_ssl"]
        )
    return


def on_postprocessor_task_results(data):
    """
    Runner function - provides a means for additional postprocessor functions based on the task success.

    The 'data' object argument includes:
        task_processing_success         - Boolean, did all task processes complete successfully.
        file_move_processes_success     - Boolean, did all postprocessor movement tasks complete successfully.
        destination_files               - List containing all file paths created by postprocessor file movements.
        source_data                     - Dictionary containing data pertaining to the original source file.

    :param data:
    :return:
    """
    # Setup the settings
    settings = Settings(library_id=data.get("library_id"))

    # Fetch values for notify

    if data.get("task_processing_success") and data.get("file_move_processes_success"):
        notify(
            data.get("source_data"),
            data.get("destination_files"),
            settings.get_setting(),
        )

    return data
