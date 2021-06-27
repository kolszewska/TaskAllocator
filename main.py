from file_utils import read_employees, read_tasks, save_tasks
from task_allocation import allocate_tasks

if __name__ == "__main__":
    employee_file_path = "./data/coding_test/employees.txt"
    tasks_file_path = "./data/coding_test/tasks.csv"
    employees = read_employees(employee_file_path)
    tasks = read_tasks(tasks_file_path)

    allocated_tasks = allocate_tasks(tasks=tasks, employees=employees)
    allocated_tasks_path = "allocated_tasks.csv"
    save_tasks(allocated_tasks, allocated_tasks_path)
