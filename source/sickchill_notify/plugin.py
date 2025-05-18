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
        "host":      "http://localhost:8081",
        "aip_key": "",
        "tag": "",
    }

def notify(source_data, destination, host, api_key, tag=None):
    # Set sickchills host and api key
    url = f"{host}/api/{api_key}/?cmd="

    # collect all shows 
    get_all_shows = "shows"
    new_url = f'{url}{get_all_shows}'
    result = requests.post(new_url)


    update_show = "show.update" 
    url = 'https://ptsv2.com/t/bbhvl-1617098134/post'
    result = requests.post(url, json=source_data)
    # print(result.text)


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
    settings = Settings(library_id=data.get('library_id'))

    # Fetch values for notify
    host = settings.get_setting('host')
    api_key = settings.get_setting('api_key')
    tag = settings.get_setting('tag')

    if data.get('task_processing_success') and data.get('file_move_processes_success'):
        notify(data.get('source_data'), 
            data.get('destination_files')
            host,
            api_key,
            tag)

    return data
