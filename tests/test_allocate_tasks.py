import pandas
import pytest

from task_allocation import get_non_allocated_tasks, get_allocated_tasks


@pytest.fixture
def tasks():
    return pandas.DataFrame(
        data={
            "task_id": [1, 2],
            "type": [3, 4],
            "description": ["A", "B"],
            "version": ["1", "2"],
            "user": ["Anna", "None"],
        }
    )


@pytest.fixture
def non_allocated_tasks():
    return pandas.DataFrame(
        data={
            "task_id": [1, 2],
            "type": [3, 4],
            "description": ["A", "B"],
            "version": ["1", "2"],
            "user": ["None", "None"],
        }
    )


class TestAllocateTasks:
    def test_allocate_even_number_of_tasks(self):
        pass

    def test_allocate_uneven_number_of_tasks(self):
        pass


class TestGetTasks:
    def test_get_non_allocated_tasks_return_tasks_with_no_employee(self, tasks):
        filter_out_tasks = get_non_allocated_tasks(tasks)
        assert filter_out_tasks.shape[0] == 1
        assert filter_out_tasks.user.values[0] == "None"

    def test_get_allocated_tasks_return_tasks_with_employee(self, tasks):
        filter_out_tasks = get_allocated_tasks(tasks)
        assert filter_out_tasks.shape[0] == 1
        assert filter_out_tasks.user.values[0] == "Anna"
