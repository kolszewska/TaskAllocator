from typing import List

import pandas


def get_non_allocated_tasks(available_tasks: pandas.DataFrame) -> pandas.DataFrame:
    """Get non allocated tasks that were not given to some employees by management."""
    return available_tasks[available_tasks["user"] == "None"]


def get_allocated_tasks(available_tasks: pandas.DataFrame) -> pandas.DataFrame:
    """Get allocated tasks that were given to some employees by management."""
    return available_tasks[available_tasks["user"] != "None"]


def get_number_of_tasks_per_employee(tasks_size: int, employees_size: int) -> List[int]:
    """Get number of tasks that will be allocated to given employee."""
    min_number_of_tasks_allocated_to_employee = int(tasks_size / employees_size)
    employees_with_additional_tasks = int(tasks_size % employees_size)

    tasks_per_employee = [min_number_of_tasks_allocated_to_employee] * employees_size
    for i in range(0, employees_with_additional_tasks):
        tasks_per_employee[i] += 1
    return tasks_per_employee


def allocate_tasks(tasks: pandas.DataFrame, employees: dict) -> pandas.DataFrame:
    """Allocate tasks to employees."""
    non_allocated_tasks = get_non_allocated_tasks(tasks)
    allocated_tasks = get_allocated_tasks(tasks)

    available_employees = employees
    employees_size = len(available_employees.keys())
    tasks_size = non_allocated_tasks.shape[0]
    tasks_per_employee = get_number_of_tasks_per_employee(tasks_size, employees_size)

    employee_index = 0
    current_row = 0
    while employee_index < employees_size:
        employee_name = available_employees.popitem()[0]
        tasks_number_to_allocate = tasks_per_employee[employee_index]
        start_row = current_row
        end_row = current_row + tasks_number_to_allocate
        non_allocated_tasks.loc[start_row:end_row, "user"] = employee_name
        current_row = end_row
        employee_index += 1

    return pandas.concat([non_allocated_tasks, allocated_tasks])
