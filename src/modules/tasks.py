import logging
from datetime import datetime
from functools import cmp_to_key
import requests

from src.config import CONFIG
from src.utils import log

class Tasks:

    def __init__(self):
        self.bearer_key = CONFIG["tasks"]["todoist_api_key"]
        self.api_url = "https://api.todoist.com/rest/v2"

    @staticmethod
    def can_be_loaded():
        return bool(CONFIG["tasks"]) and bool(CONFIG["tasks"]["todoist_api_key"])

    def get(self):
        headers = {
            'Authorization': f'Bearer {self.bearer_key}',
            'lang': 'es'
        }
        response = requests.get(self.api_url + '/tasks', headers=headers)
        response.raise_for_status()
        data = response.json()

        log(f"TASKS Module: Received data: {data}", logging.DEBUG)
        result_tasks = []
        for todoist_task in data:
            result_tasks.append({
                'id': todoist_task['id'],
                'priority_number': todoist_task['priority'],
                'priority': get_priority(todoist_task['priority']),
                'order': todoist_task['order'],
                'title': todoist_task['content'],
                'description': todoist_task['description'],
                'due': todoist_task['due']
            })

        return sorted(result_tasks, key=cmp_to_key(sort_tasks))


def get_priority(priority):
    if priority == 1:
        return "⚪ Sin prioridad"
    elif priority == 2:
        return "🔵 Prioridad baja"
    elif priority == 3:
        return "🟡 Prioridad media"
    elif priority == 4:
        return "🔴 Prioridad alta"
    else:
        return "❔ Prioridad desconocida"


def sort_tasks(task1, task2):
    if task1["priority_number"] != task2["priority_number"]:
        return -1 if task1["priority_number"] > task2["priority_number"] else 1

    if task1["due"] and not task2["due"]:
        return -1

    if task2["due"] and not task1["due"]:
        return 1

    if task1["due"] and task2["due"]:
        duedate_task1 = datetime.strptime(task1["due"]["date"], '%Y-%m-%d')
        duedate_task2 = datetime.strptime(task1["due"]["date"], '%Y-%m-%d')

        if duedate_task1 != duedate_task2:
            return -1 if duedate_task1 > duedate_task2 else 1

    return -1 if task1["order"] > task2["order"] else 1