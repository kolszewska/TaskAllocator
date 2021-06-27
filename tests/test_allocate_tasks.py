import pandas
import pytest

from task_allocation import get_non_allocated_tasks, get_allocated_tasks, allocate_tasks


@pytest.fixture
def tasks():
    return pandas.DataFrame(
        data={
            "task_id": ["1", "2"],
            "type": ["engineer", "engineer"],
            "description": ["A", "B"],
            "version": ["1", "2"],
            "user": ["Anna", "None"],
        }
    )


@pytest.fixture
def non_allocated_tasks():
    return pandas.DataFrame(
        data={
            "task_id": ["3", "4", "5"],
            "type": ["engineer", "architect", "architect"],
            "description": ["A", "B", "C"],
            "version": ["1", "2", "3"],
            "user": ["None", "None", "None"],
        }
    )


@pytest.fixture
def allocated_tasks():
    return pandas.DataFrame(
        data={
            "task_id": ["5", "6"],
            "type": ["architect", "architect"],
            "description": ["A", "B"],
            "version": ["1", "2"],
            "user": ["Hagrid", "Ron"],
        }
    )


@pytest.fixture
def employees():
    return {"Harry Potter": "engineer", "Ron Weasley": "architect"}


class TestAllocateTasks:
    def test_allocate_even_number_of_tasks_per_employee(
        self, non_allocated_tasks, employees
    ):
        result = allocate_tasks(non_allocated_tasks.head(2), employees)
        assert result.shape[0] == 2
        assert result.user[0] == "Ron Weasley"
        assert result.user[1] == "Harry Potter"

    def test_allocate_uneven_number_of_tasks_per_employee_adds_task_to_first_employee(
        self, non_allocated_tasks, employees
    ):
        result = allocate_tasks(non_allocated_tasks, employees)
        assert result.shape[0] == 3
        assert result.user[0] == "Ron Weasley"
        assert result.user[1] == "Ron Weasley"
        assert result.user[2] == "Harry Potter"

    def test_returns_concatenated_results_of_non_and_allocated_tasks(
        self, allocated_tasks, non_allocated_tasks, employees
    ):
        input_tasks = pandas.concat([allocated_tasks, non_allocated_tasks])
        result = allocate_tasks(input_tasks, employees)

        assert allocated_tasks.shape == (2, 5)
        assert non_allocated_tasks.shape == (3, 5)
        assert result.shape == (5, 5)


class TestGetTasks:
    def test_get_non_allocated_tasks_return_tasks_with_no_employee(self, tasks):
        filter_out_tasks = get_non_allocated_tasks(tasks)
        assert filter_out_tasks.shape[0] == 1
        assert filter_out_tasks.user.values[0] == "None"

    def test_get_allocated_tasks_return_tasks_with_employee(self, tasks):
        filter_out_tasks = get_allocated_tasks(tasks)
        assert filter_out_tasks.shape[0] == 1
        assert filter_out_tasks.user.values[0] == "Anna"
