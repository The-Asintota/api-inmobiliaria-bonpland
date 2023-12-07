from typing import Dict, List
from test.test_property_services import BaseTestCase
from services.property.models.constants import PropertyType, AvailabilityType
from rest_framework  import status
from django.urls import reverse
from parameterized import parameterized
from backend.settings.base import REST_FRAMEWORK


class TestSearchView(BaseTestCase):
    """
    Test case for the SearchView.

    Attributes:
    - url (str): URL for the search property view.
    """
    
    url=reverse('search_property')
    
    
    @parameterized.expand(
        input=[({
                'type_property': [
                    PropertyType.HOME.value,
                    PropertyType.DEPARTMENT.value,
                ],
                'availability_type': [
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                ],
            },),
        ]
    )
    def test_handle_valid_request(self, query_params:Dict[str, List[str]]) -> None:
        query_params_list=[]
        for key, value in query_params.items():
            for n in value:
                query_params_list.append(f'{key}={n}')
        complete_url=self.url + '?' + '&'.join(query_params_list)
        response=self.client.get(complete_url)
        if response.status_code != status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        elif response.data['count'] > REST_FRAMEWORK['PAGE_SIZE']:
            self.assertIsNotNone(response.data['next'])
            self.assertIsNone(response.data['previous'])
            response=self.client.get(response.data['next'])
            self.assertTrue(1 <= len(response.data['results']) <= REST_FRAMEWORK['PAGE_SIZE'])
    
    
    @parameterized.expand(
        input=[({
                'type_property':['home'],
                'availability_type':['buy'],
                'type_local':['commercial'],
                'rooms':['6'],
                'bathrooms':['6'],
                'floors':['6'],
                'parking_lot':['si'],
                'garden':['si'],
                'garages':['si'],
                'all':['si'],
                'price_usd':['0_-810.00'],
            },),
        ]
    )
    def test_handle_invalid_request(self, query_params:Dict[str, List[str]]) -> None:
        query_params_list=[]
        for key, value in query_params.items():
            for n in value:
                query_params_list.append(f'{key}={n}')
        complete_url=self.url + '?' + '&'.join(query_params_list)
        response=self.client.get(complete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)