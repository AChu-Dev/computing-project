import unittest
from django.test import Client
import API.models
from rest_framework import status 
from rest_framework.test import APITestCase
import logging
import datetime

logger = logging.getLogger(__name__)

# Create your tests here.
class userTests(unittest.TestCase):
    def setupTestObjects(self):
        logger.debug('Adding Users to DB for testing, DateTime:${}'.format(datetime.datetime.now()))
        for x in range (0, 3):
            test_create_user(x)

    def test_list_users(self):
        logger.debug('Test(API Endpoint): LIST All Users')
        self.setupTestObjects()
        
        response = self.client.post("rest_api/user/list", follow=True)
        #logger.debug('Test(API Endpoint): LIST All Users, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self, x):
        logger.debug('Test(API Endpoint): CREATE New User')
        
        data = {
                'name':'Test{}'.format(x), 
                'firstName':'Test{}_F'.format(x),
                'lastName':'Test{}_S'.format(x),
                'email':'test{}@snowcore.org.uk'.format(x),
                'password':'password'
                }
        
        response = self.client.post("/rest_api/user/create", data,format='json', follow=True)
        #logger.debug('Test(API Endpoint): CREATE New User, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    

