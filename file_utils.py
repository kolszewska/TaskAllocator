import json

import pandas


def read_employees(file_path: str) -> dict:
    """Read available employees from a file under a given path."""
    employees_file = open(file_path)
    employees_str = employees_file.read().replace("'", '"')
    return json.loads(employees_str)


def read_tasks(file_path: str) -> pandas.DataFrame:
    """Read available tasks from a file under a given path."""
    return pandas.read_csv(file_path)


def save_tasks(tasks: pandas.DataFrame, file_path: str):
    """Save allocated tasks under a given file path."""
    tasks.to_csv(file_path)
