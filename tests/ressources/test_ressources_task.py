"""Tests on tasks routes"""

import copy
from datetime import datetime
from datetime import timedelta

import pytest

from monitoring_project_api.models import Data
from monitoring_project_api.models import Task
from monitoring_project_api.models import TaskByProperty
from monitoring_project_api.models import TaskProperty

NEW_TASK = {
    "name": "Task name",
    "description": "Task description",
    "task_frequency": 10,
    "next_run_time": (datetime.now() +
                      timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S'),
    "target_data": {
        "path": "http://localhost:34"
    },
    "properties": {
        "black_ip_address": [
            '192.168.0.0'
        ]
    }
}

TASK_URL = '/tasks/'

SCHEDULER_API_URL = '/scheduler/'

DUMMY_ID = 42

TASK_DB = {
    "name": "Task name",
    "description": "Task description",
    "task_frequency": timedelta(seconds=1800),
    "next_run_time": datetime.strptime("2021-12-31 00:00:00", '%Y-%m-%d '
                                                              '%H:%M:%S')
}


class TestViewsTasks:

    @pytest.mark.data_quantity(quantity=2)
    def test_get_task_list(self, client, database, generate_data):
        # GET
        ret = client.get(TASK_URL)
        assert ret.status_code == 200
        assert len(ret.json) == 0

        # Retrieve generated data
        generated_data = generate_data
        # Add tasks
        item_1 = Task(**TASK_DB, target_data_id=generated_data[0])
        item_2 = Task(**TASK_DB, target_data_id=generated_data[1])
        database.session.add_all([item_1, item_2])
        database.session.commit()

        # GET
        ret = client.get(TASK_URL)
        assert ret.status_code == 200
        assert len(ret.json) == 2

        for task in ret.json:
            assert task['name'] == TASK_DB['name']
            assert task['description'] == TASK_DB['description']
            assert task['task_frequency'] == 1800
            assert task['next_run_time'] == '2021-12-31T00:00:00'

    # noinspection PyUnusedLocal
    def test_post_task(self, client, database):
        # POST
        ret = client.post(TASK_URL, json=NEW_TASK)
        assert ret.status_code == 201
        data = ret.json
        task_id = data.pop('id')
        target_data_id = data['target_data'].pop('id')
        last_run_time = data.pop('last_run_time')
        is_active = data.pop('is_active')
        expected_data = copy.deepcopy(NEW_TASK)
        assert data == NEW_TASK

        # Check properties
        task_properties = database.session.query(
            TaskProperty
        ).filter(
            TaskProperty.name.in_(NEW_TASK['properties'].keys())
        )
        task_by_properties = database.session.query(TaskByProperty)
        assert task_by_properties.count() == len(NEW_TASK['properties'])
        for property_name, property_value in NEW_TASK['properties'].items():
            task_property = task_properties.filter(
                TaskProperty.name == property_name).first()
            assert task_property.name == property_name
            db_property = task_by_properties.filter(
                TaskByProperty.task_property_id == task_property.id)
            assert db_property.count()
            assert db_property.first().value == str(property_value)

        # Check scheduler
        scheduler_api_response = client.get(f'{SCHEDULER_API_URL}jobs')
        assert scheduler_api_response.status_code == 200
        json_response = scheduler_api_response.json
        assert len(json_response) == 2
        assert json_response[0]['args'] == []
        assert json_response[0]['id'] == 'auto_check_job'
        assert json_response[0]['name'] == 'auto_check'
        assert json_response[1]['args'] == [task_id]
        assert f'individual_check_job_{task_id}' in json_response[1]['id']
        assert f'individual_check_job_{task_id}' in json_response[1]['name']
        for scheduler_task in json_response:
            assert scheduler_task['kwargs'] == {}

        # Check target data
        target_data = Data.get(target_data_id)
        assert target_data is not None
        assert NEW_TASK['target_data']['path'] == target_data.path

        # Post without properties
        task_without_properties = copy.deepcopy(NEW_TASK)
        task_without_properties.pop('properties')
        ret = client.post(TASK_URL, json=task_without_properties)
        assert ret.status_code == 201

        ret = client.get(TASK_URL)
        assert ret.status_code == 200
        assert len(ret.json) == 2

        # Post without target data
        task_without_target_data = copy.deepcopy(NEW_TASK)
        task_without_target_data.pop('target_data')
        ret = client.post(TASK_URL, json=task_without_target_data)
        assert ret.status_code == 422
        assert ret.json['errors']['json']['target_data'] == ['Missing data '
                                                             'for required '
                                                             'field.']

        # Post with incorrect `next_run_time`
        incorrect_task = copy.deepcopy(NEW_TASK)
        incorrect_task['next_run_time'] = \
            str(datetime.now() - timedelta(minutes=1))

        ret = client.post(TASK_URL, json=incorrect_task)
        assert ret.status_code == 422
        assert ret.json['status'] == 'Unprocessable Entity'
        assert ret.json['errors']['json']['next_run_time'][0] == 'Next run ' \
                                                                 'time must ' \
                                                                 'be greater '\
                                                                 'than the ' \
                                                                 'actual ' \
                                                                 'time.'
