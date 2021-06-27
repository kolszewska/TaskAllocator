from enum import Enum
from typing import List

import pandas


class SpecTypes(Enum):
    ARCHITECT = "architect"
    ENGINEER = "engineer"


def get_non_allocated_tasks_for_spec(
    available_tasks: pandas.DataFrame, spec: str
) -> pandas.DataFrame:
    """Get non allocated tasks for spec that were not given to some employees by management."""
    tasks_for_spec = available_tasks[available_tasks["type"] == spec]
    return tasks_for_spec[tasks_for_spec["user"] == "None"]


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


def _allocate_task_per_spec(
    tasks: pandas.DataFrame, employees: dict, spec: str
) -> pandas.DataFrame:
    non_allocated_tasks = get_non_allocated_tasks_for_spec(tasks, spec)
    available_employees = [k for k, v in employees.items() if v == spec]

    if len(available_employees) == 0:
        return tasks

    employees_size = len(available_employees)
    tasks_size = non_allocated_tasks.shape[0]

    tasks_per_employee = get_number_of_tasks_per_employee(tasks_size, employees_size)
    employee_index = 0
    current_row = 0
    while employee_index < employees_size:
        employee_name = available_employees[0]
        tasks_number_to_allocate = tasks_per_employee[employee_index]
        start_row = current_row
        end_row = current_row + tasks_number_to_allocate
        non_allocated_tasks.loc[start_row:end_row, "user"] = employee_name
        current_row = end_row
        employee_index += 1

    return non_allocated_tasks


def allocate_tasks(tasks: pandas.DataFrame, employees: dict) -> pandas.DataFrame:
    """Allocate tasks to employees."""
    final_task_allocation = pandas.DataFrame()
    for spec_type in list(SpecTypes):
        allocated_tasks = _allocate_task_per_spec(
            tasks, employees, spec=spec_type.value
        )
        final_task_allocation = pandas.concat([allocated_tasks, final_task_allocation])
    allocated_tasks = get_allocated_tasks(tasks)
    return pandas.concat([final_task_allocation, allocated_tasks])
