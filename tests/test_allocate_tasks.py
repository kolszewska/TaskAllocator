import pandas
import pytest

from task_allocation import (
    get_non_allocated_tasks_for_spec,
    get_allocated_tasks,
    allocate_tasks,
)


@pytest.fixture
def tasks():
    return pandas.DataFrame(
        data={
            "task_id": ["1", "2"],
            "type": ["engineer", "engineer"],
            "description": ["A", "B"],
            "version": ["1", "2"],
            "user": ["Hagrid", "None"],
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
            "user": ["Harry Potter", "Ron Weasley"],
        }
    )


@pytest.fixture
def employees():
    return {"Harry Potter": "architect", "Ron Weasley": "engineer"}


class TestAllocateTasks:
    def test_allocate_even_number_of_tasks_per_employee(
        self, non_allocated_tasks, employees
    ):
        result = allocate_tasks(non_allocated_tasks.head(2), employees)
        assert result.shape[0] == 2
        self._assert_expected_task(
            expected_user="Ron Weasley",
            expected_type="engineer",
            user=result.user[0],
            _type=result.type[0],
        )
        self._assert_expected_task(
            expected_user="Harry Potter",
            expected_type="architect",
            user=result.user[1],
            _type=result.type[1],
        )

    def test_allocate_uneven_number_of_tasks_per_employee_adds_task_to_first_employee(
        self, non_allocated_tasks, employees
    ):
        result = allocate_tasks(non_allocated_tasks, employees)
        assert result.shape[0] == 3
        self._assert_expected_task(
            expected_user="Ron Weasley",
            expected_type="engineer",
            user=result.user[0],
            _type=result.type[0],
        )
        self._assert_expected_task(
            expected_user="Harry Potter",
            expected_type="architect",
            user=result.user[1],
            _type=result.type[1],
        )
        self._assert_expected_task(
            expected_user="Harry Potter",
            expected_type="architect",
            user=result.user[2],
            _type=result.type[2],
        )

    def test_fixing_mistakes_in_allocated_tasks_changes_assignment(
        self, allocated_tasks, employees
    ):
        result = allocate_tasks(allocated_tasks, employees)
        assert result.shape[0] == 2
        self._assert_expected_task(
            expected_user="Harry Potter",
            expected_type="architect",
            user=result.user[0],
            _type=result.type[0],
        )
        self._assert_expected_task(
            expected_user="Harry Potter",
            expected_type="architect",
            user=result.user[1],
            _type=result.type[1],
        )

    def test_returns_concatenated_results_of_non_and_allocated_tasks(
        self, allocated_tasks, non_allocated_tasks, employees
    ):
        input_tasks = pandas.concat([allocated_tasks, non_allocated_tasks])
        result = allocate_tasks(input_tasks, employees)

        assert allocated_tasks.shape == (2, 5)
        assert non_allocated_tasks.shape == (3, 5)
        assert result.shape == (5, 5)

    def test_does_not_allocate_tasks_if_employee_spec_does_not_match(
        self, non_allocated_tasks
    ):
        employees = {"Lord Voldemort": "evil madman"}
        result = allocate_tasks(non_allocated_tasks, employees)
        assert "Lord Voldemort" not in list(result.user.values)

    @staticmethod
    def _assert_expected_task(
        expected_user: str, expected_type: str, user: str, _type: str
    ):
        assert user == expected_user
        assert _type == expected_type


class TestGetTasks:
    def test_get_non_allocated_tasks_return_correct_tasks(self, tasks):
        filter_out_tasks = get_non_allocated_tasks_for_spec(tasks, spec="engineer")
        assert filter_out_tasks.shape[0] == 1
        assert filter_out_tasks.user.values[0] == "None"
        assert filter_out_tasks.type.values[0] == "engineer"

    def test_get_allocated_tasks_return_tasks_with_employee(self, tasks):
        filter_out_tasks = get_allocated_tasks(tasks)
        assert filter_out_tasks.shape[0] == 1
        assert filter_out_tasks.user.values[0] == "Hagrid"
