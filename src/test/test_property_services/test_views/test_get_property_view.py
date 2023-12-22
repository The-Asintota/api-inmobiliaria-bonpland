from typing import Dict
from rest_framework import status
from django.urls import reverse
from test.test_property_services import BaseTestCase
from parameterized import parameterized
from bson import ObjectId, Decimal128
from parameterized import parameterized
from datetime import datetime


class TestGetPropertyView(BaseTestCase):
    """
    This class contains unit tests for the `GetPropertyView`. It inherits from the `BaseTestCase` class which sets up the necessary test environment.

    The tests are divided into three categories:
    1. Handling valid requests
    2. Handling invalid requests
    3. Handling requests for non-existent properties
    """
    
    @parameterized.expand(
        input=[
            ({
                'pk': str(ObjectId()),
            },),
            ({
                'pk': str(ObjectId()),
            },),
        ]
    )
    def test_handle_valid_request(self, data: Dict[str, str]) -> None:
        """
        This test checks if the GetPropertyView correctly handles `valid requests`. It does this by creating a document with the provided primary key (pk) and then sending a GET request to the view. The response is then checked for the correct status code and data.

        Args:
        - data (Dict[str, str]) : A dictionary that contains the primary key (pk) of the document that will later be used as an `argument in the path`.
        """
        
        # A document is created with the pk to test
        self.collection.insert_one(
            document=self.factory.get_data(pk=data['pk'])
        )
        
        # Check response
        response = self.client.get(reverse('get_property', kwargs=data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Compare response data with database data
        query_data: Dict = self.collection.find_one(
            filter = {'pk': ObjectId(data['pk'])},
            projection={'_id': 0}
        )
        response_data = response.data
        for key in query_data.keys():
            if isinstance(query_data[key], ObjectId):
                self.assertEqual(response_data[key], str(query_data[key]))
                continue
            elif isinstance(query_data[key], Decimal128):
                self.assertEqual(response_data[key], str(query_data[key].to_decimal()))
                continue
            elif isinstance(query_data[key], datetime):
                self.assertEqual(response_data[key], query_data[key].isoformat())
                continue
            self.assertEqual(response_data[key], query_data[key])
    
    @parameterized.expand(
        input=[
            ({
                'pk': '325003-9e04812-bc726449651105',
            },),
            ({
                'pk': 'pk',
            },),
            ({
                'pk': 1252584,
            },),
            ({
                'pk': ' ',
            },),
            ({
                'pk': None,
            },),
        ]
    )
    def test_handle_invalid_request(self, data: Dict[str, str]) -> None:
        """
        This test checks if the GetPropertyView correctly handles `invalid requests`. It does this by sending a GET request to the view with invalid data and then checking the response for the correct status code.

        Args:
        - data (Dict[str, str]) : A dictionary that contains the primary key (pk) of the document that will later be used as an `argument in the path`.
        """
        
        # Check response
        response = self.client.get(reverse('get_property', kwargs=data))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_handle_not_found_property(self) -> None:
        """
        This test checks if the GetPropertyView correctly handles requests for `non-existent properties`. It does this by sending a GET request to the view with a non-existent primary key (pk) and then checking the response for the correct status code.
        """
        
        # Check response
        response = self.client.get(reverse('get_property', kwargs={'pk': str(ObjectId())}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)