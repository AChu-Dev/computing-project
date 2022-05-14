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
        logger.debug('Test(API Endpoint): LIST All Users')
        self.setupTestObjects() 
        response = self.client.post("rest_api/resort/list", follow=True)
        #logger.debug('Test(API Endpoint): LIST All Users, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, 200)
    
    def test_create_resort(self, x):
        logger.debug('Test(API Endpoint): CREATE New User')
        
        data = {
                'name':'Test{}'.format(x), 
                'address':'{} Test, Test, The Three Valleys'.format(x),
                'lon':'{}'.format(45.4203 + x),
                'lat':''.format(6.61409 + x)
                }
        
        response = self.client.post("/rest_api/resort/create", data,format='json', follow=True)
        #logger.debug('Test(API Endpoint): CREATE New User, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, 201)
    
    
        
    

