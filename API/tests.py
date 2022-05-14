import unittest
from django.test import Client
import API.models
from rest_framework import status 
from rest_framework.test import APITestCase
import logging
import datetime

logger = logging.getLogger(__name__)

# Create your tests here.
class ResortTests(unittest.TestCase):

    def setupTestObjects(self):
        self.client = Client()
        logger.debug('Adding Users to DB for testing, DateTime:${}'.format(datetime.datetime.now()))
        for x in range (0, 3):
            self.test_create_resort(x)

    def test_list_resorts(self):
        logger.debug('Test (API Endpoint): LIST All Resort')
        self.client = Client()
        self.setupTestObjects() 
        response = self.client.get("rest_api/resort", follow=True)
        #logger.debug('Test(API Endpoint): LIST All Users, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, 200)
    
    def test_create_resort(self, x):
        logger.debug('Test (API Endpoint): CREATE New Resort')
        self.client = Client()
        data = {
                'name':'Test{}'.format(x), 
                'address':'{} CREATE, Test, The Three Valleys'.format(x),
                'lon':'{}'.format(45.4203 + x),
                'lat':''.format(6.61409 + x)
                }
        
        response = self.client.post("/rest_api/resort", data,format='json', follow=True)
        #logger.debug('Test(API Endpoint): CREATE New User, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, 201)
    
    def test_delete_resort(self):
        logger.debug('Test (API Endpoint): DELETE Resort')
        self.client = Client()
        self.test_create_resort(1)
        response = self.client.delete("/rest_api/resort", 1,follow=True)
        self.assertEqual(response.status_code, 204)

    def test_put_resort(self):
        logger.debug('Test (API Endpoint): PUT/UPDATE Resort')
        self.client = Client()
        #test
        self.test_create_resort(2)

        data = {
                'name':'Test{}'.format(6.9), 
                'address':'{} PUT, Test, The Three Valleys'.format(6.9),
                'lon':'{}'.format(45.4203 + 6.9),
                'lat':''.format(6.61409 + 6.9)
                }
        
        response = self.client.put("/rest_api/resort", data, format='json', follow=True)
        self.assertEqual(response.status_code, 204)

        

        
        
    

