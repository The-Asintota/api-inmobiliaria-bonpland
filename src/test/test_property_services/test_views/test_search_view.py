from typing import Dict, List
from test.test_property_services import BaseTestCase
from services.property.models.constants import PropertyType, AvailabilityType
from rest_framework import status
from django.urls import reverse
from parameterized import parameterized
from backend.settings.base import REST_FRAMEWORK


class TestSearchView(BaseTestCase):
    """
    Test case for the property search view.

    This class inherits from the BaseTestCase and tests the functionality of the property search view. It tests both valid and invalid requests to the search view.
    """

    url = reverse('search_property')

    @classmethod
    def __get_url(cls, query_params: Dict[str, List[str]]) -> str:
        """
        Complete the path based on the query parameters.
        """

        query_params_list = []
        for key, value in query_params.items():
            for n in value:
                query_params_list.append(f'{key}={n}')
        return cls.url + '?' + '&'.join(query_params_list)

    @parameterized.expand(
        input=[
            ({
                'type_property': [
                    PropertyType.HOME.value,
                    PropertyType.DEPARTMENT.value,
                ],
                'availability_type': [
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                ],
            },),
            ({
                'type_property': [
                    PropertyType.HOME.value,
                ],
                'availability_type': [
                    AvailabilityType.BUY.value,
                    AvailabilityType.RENT.value,
                ],
                'rooms': ['3'],
            },),
            ({
                'type_property': [
                    PropertyType.LOCAL.value,
                ],
                'parking_lot': ['true'],
            },),
        ]
    )
    def test_handle_valid_request(self, query_params: Dict[str, List[str]]) -> None:
        """
        This method tests the search view with a set of valid query parameters. It checks the response status code, and if the response contains the expected number of results. If the number of results exceeds the page size, it checks the presence of the 'next' link and the absence of the 'previous' link in the response.

        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to be used in the request.
        """

        # Check response
        response = self.client.get(self.__get_url(query_params))
        if response.status_code != status.HTTP_200_OK:
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        elif response.data['count'] > REST_FRAMEWORK['PAGE_SIZE']:
            self.assertIsNotNone(response.data['next'])
            self.assertIsNone(response.data['previous'])
            self.assertTrue(
                1 <= len(response.data['results']) <= REST_FRAMEWORK['PAGE_SIZE'])
            response = self.client.get(response.data['next'])
            self.assertTrue(
                1 <= len(response.data['results']) <= REST_FRAMEWORK['PAGE_SIZE'])

    @parameterized.expand(
        input=[
            ({
                'type_property': ['home'],
                'availability_type': ['buy'],
                'type_local': ['commercial'],
                'rooms': ['6'],
                'bathrooms': ['6'],
                'floors': ['6'],
                'parking_lot': ['si'],
                'garden': ['si'],
                'garages': ['si'],
                'all': ['si'],
                'price_usd': ['0_-810.00'],
            },)
        ]
    )
    def test_handle_invalid_request(self, query_params: Dict[str, List[str]]) -> None:
        """
        This method tests the search view with a set of invalid query parameters. It checks that the response status code is 400 (Bad Request).

        Args:
        - query_params (Dict[str, List[str]]) : The query parameters to be used in the request.
        """

        # Check response
        response = self.client.get(self.__get_url(query_params))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
