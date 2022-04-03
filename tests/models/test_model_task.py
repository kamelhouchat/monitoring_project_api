"""Tests on Task"""

import copy
from datetime import datetime
from datetime import timedelta

import pytest

from monitoring_project_api.models import Data
from monitoring_project_api.models import Task

DUMMY_ID = 15463

TASK = {
    "id": DUMMY_ID,
    "name": "Task name",
    "description": "Task description",
    "task_frequency": timedelta(seconds=1800),
    "next_run_time": datetime.strptime("2021-12-31 00:00:00", '%Y-%m-%d '
                                                              '%H:%M:%S')
}


class TestModelTask:

    @pytest.mark.data_quantity(quantity=2)
    def test_model_task(self, database, generate_data):
        # Get generated data id
        generated_data = generate_data
        TASK['target_data_id'] = generated_data[0]

        # Add task
        item = Task(**TASK)
        database.session.add(item)
        database.session.commit()

        # Test Task repr
        assert (
                repr(item) == f"<Task(id={DUMMY_ID}, name=Task name, "
                              "description=Task description, "
                              "task_frequency=0:30:00, "
                              "next_run_time=2021-12-31 00:00:00, "
                              "last_run_time=None, is_active=True)>"
        )

        # Test target_data property
        assert item._target_data is None

        _ = item.target_data
        assert item._target_data is not None
        assert item.target_data.id == generated_data[0]

        # Test get with valid parameter
        get_result = Task.get(item.id)
        assert get_result.name == item.name
        assert get_result.description == item.description
        assert get_result.task_frequency == item.task_frequency
        assert get_result.next_run_time == item.next_run_time

        # Test get with invalid parameter
        invalid_id = 5653
        with pytest.raises(ValueError, match=f'{invalid_id} is not a '
                                             f'valid id.'):
            Task.get(invalid_id)

        # Get related data
        related_data = Data.get(generated_data[0])
        assert related_data.id == item.target_data.id
        assert related_data.os_host == item.target_data.os_host
        assert related_data.os_port == item.target_data.os_port
        assert related_data.is_using_ssl == item.target_data.is_using_ssl

        # Test `get_all` method
        # Add deleted Task
        deleted_task_args = copy.deepcopy(TASK)
        deleted_task_args.pop('id')
        deleted_task_args['is_active'] = False
        deleted_task_args['target_data_id'] = generated_data[1]

        database.session.add(Task(**deleted_task_args))
        database.session.commit()

        with_deleted = Task.get_all(active_only=False)
        assert len(with_deleted) == 2
        assert not with_deleted[1].is_active

        without_deleted = Task.get_all()
        assert len(without_deleted) == 1
        assert without_deleted[0].is_active

        # Test `remaining_time_to_execute` method
        assert item.remaining_time_to_execute_task() == 0

        # Test `is_to_process` method
        assert item.is_to_process()
