"""Tests on Data"""

import pytest

from monitoring_project_api.models import Data

DUMMY_ID = 15463

DATA = {
    "id": DUMMY_ID,
    "os_host": "localhost",
    "os_port": 1522,
    "is_using_ssl": True,
    "auth_user_name": 'Dummy user',
    "auth_password": 'Dummy password',
    "indice": 'Dummy indice'
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
                              f", os_host={DATA['os_host']}"
                              f", os_port={DATA['os_port']}"
                              f", is_using_ssl={DATA['is_using_ssl']}"
                              f", indice={DATA['indice']}"
                              ")>"
        )

    @pytest.mark.data_quantity(quantity=1)
    @pytest.mark.data_information(os_host='https://url.com')
    def test_model_data_get_by_id(self, database, generate_data):
        # Get generated data
        generated_data = generate_data

        result = Data.get(generated_data[0])

        assert result.id == generated_data[0]
        assert result.os_host == 'https://url.com'

        # Test with invalid parameter
        invalid_id = 45423
        with pytest.raises(ValueError, match=f'{invalid_id} is not '
                                             f'a valid id.'):
            Data.get(invalid_id)
