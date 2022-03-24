"""Tests on `task properties` routes"""

from monitoring_project_api.models import TaskProperty
from monitoring_project_api.models.init_db_values import \
    TASK_PROPERTY_DEFAULT_VALUES

TASK_PROPERTY_URL = '/task_properties/'

DUMMY_ID = 122131

TASK_PROPERTY = {
    "id": DUMMY_ID,
    "name": "Dummy name",
    "description": "Dummy description",
    "type": "String"
}


class TestViewsTaskProperties:

    def test_get_task_properties_list(self, client):
        # Get
        ret = client.get(TASK_PROPERTY_URL)
        assert ret.status_code == 200
        assert len(ret.json) == len(TASK_PROPERTY_DEFAULT_VALUES)

        for retrieved_property, real_property in zip(
                ret.json,
                TASK_PROPERTY_DEFAULT_VALUES
        ):
            assert retrieved_property['id'] == real_property['id']
            assert retrieved_property['name'] == real_property['name']
            assert retrieved_property['description'] == \
                   real_property['description']
            assert retrieved_property['type'] == real_property['type']


class TestTaskPropertyByIDViews:

    def test_get_task_property_by_id(self, client, database):
        # Add a new `data type`
        item = TaskProperty(**TASK_PROPERTY)
        database.session.add(item)
        database.session.commit()

        # Get
        ret = client.get(TASK_PROPERTY_URL + str(DUMMY_ID))
        assert ret.status_code == 200

        assert ret.json['id'] == DUMMY_ID
        assert ret.json['name'] == "Dummy name"
        assert ret.json['description'] == "Dummy description"
        assert ret.json['type'] == "String"
