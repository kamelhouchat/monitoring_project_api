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

        # Get related data
        related_data = Data.get(generated_data[0])
        assert related_data.id == item.target_data.id
        assert related_data.path == item.target_data.path

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
