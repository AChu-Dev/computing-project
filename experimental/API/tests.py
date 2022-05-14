
from django.test import TestCase
import API.models
from rest_framework import status 
from rest_framework.test import APITestCase
import logging
import datetime

logger = logging.getLogger(__name__)

# Create your tests here.
class userTests(TestCase):
    @classmethod
    def setupTestObjects(self):
        logger.debug('Adding Users to DB for testing, DateTime:${}'.format(datetime.datetime.now()))
        self.user1 = models.User(name='Test1', firstName='Test1_F',
                lastName='Test1_S', email='test1@snowcore.org.uk', password='password')
        self.user2 = models.User(name='Test2', firstName='Test2_F',
                lastName='Test2_S', email='test2@snowcore.org.uk', password='password')
        self.user3 = models.User(name='Test3', firstName='Test3_F',
                lastName='Test3_S', email='test3@snowcore.org.uk', password='password')

    def test_list_users(self):
        logger.debug('Test(API Endpoint): LIST All Users')
        self.setupTestObjects()
        
        response = self.client.post("127.0.0.1:8000/rest_api/user/list")
        #logger.debug('Test(API Endpoint): LIST All Users, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_users(self):
        logger.debug('Test(API Endpoint): CREATE New User')
        
        data = {
                'name':'Test4', 
                'firstName':'Test4_F',
                'lastName':'Test4_S',
                'email':'test4@snowcore.org.uk',
                'password':'password'
                }
        
        response = self.client.post("/rest_api/user/create", data,format='json')
        #logger.debug('Test(API Endpoint): CREATE New User, Response:${}, Status_Code:${}'.format(response.json(), response.status_code))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    

