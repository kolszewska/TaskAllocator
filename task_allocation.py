from pandas import DataFrame, concat


def get_non_allocated_tasks(available_tasks: DataFrame) -> DataFrame:
    """Get non allocated tasks that were not given to some employees by management."""
    return available_tasks[available_tasks["user"] == "None"]


def get_allocated_tasks(available_tasks: DataFrame) -> DataFrame:
    """Get allocated tasks that were given to some employees by management."""
    return available_tasks[available_tasks["user"] != "None"]


def allocate_tasks(available_employees: dict, available_tasks: DataFrame) -> DataFrame:
    """Allocate tasks to employees."""
    non_allocated_tasks = get_non_allocated_tasks(available_tasks)
    allocated_tasks = get_allocated_tasks(available_tasks)

    employees_size = len(available_employees.keys())
    tasks_size = non_allocated_tasks.size
    number_of_tasks_allocated_to_employee = int(tasks_size / employees_size)

    for i in range(0, tasks_size, number_of_tasks_allocated_to_employee):
        employee_name = available_employees.popitem()[0]
        non_allocated_tasks.loc[
            i : i + number_of_tasks_allocated_to_employee, "user"
        ] = employee_name
    return concat([non_allocated_tasks, allocated_tasks])
