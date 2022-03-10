"""Tests on Data"""

import pytest

from monitoring_project_api.models import Data

DUMMY_ID = 15463

DATA = {
    "id": DUMMY_ID,
    "path": "https://dummy_url.com"
}


class TestModelData:

    def test_model_data(self, database):
        item = Data(**DATA)
        database.session.add(item)
        database.session.commit()

        # Test Data repr
        assert (
                repr(item) == f"<Data("
                              f"id={DUMMY_ID}"
                              f", path={DATA['path']}"
                              ")>"
        )

    @pytest.mark.data_quantity(quantity=1)
    @pytest.mark.data_information(path='https://url.com')
    def test_model_data_get_by_id(self, database, generate_data):
        # Get generated data
        generated_data = generate_data

        result = Data.get(generated_data[0])

        assert result.id == generated_data[0]
        assert result.path == 'https://url.com'
