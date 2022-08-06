'''
Database testing script
'''
from django.test import TestCase
from timeline.models import *


class DatabaseTests(TestCase):

    def test_1(self):
        '''
        Create timeline with two logs, one request and one data
        '''

        print()
        print('-------------CORRECT TIMELINE CREATION TEST-------------')
        print()

        #Create default timeline object
        
        tm = Timeline(IP='10.1.0.14:5620')

        try:
            tm.save()
            print('Test 1: SUCCESS, timeline created')
        except Exception as e:
            print('Test 1: FAILED, timeline failed')
            print(e)
        print()

    

        #Create default log object (SENT)
        
        log = Log(ID='1', dateTime='2022-07-04 07:14:29.523+01:00', type='SENT', 
        restLogger='1139737886', hostname='master_1', timeline=tm)

        try:
            log.save()
            print('Test 2: SUCCESS, sent log created')
        except Exception as e:
            print('Test 2: FAILED, sent log failed')
            print(e)
        print()


        
        #Create default request object
        
        rq = Request(ID='1', requestType='POST', params='-X', 
        URL='http://10.1.0.14:5620/math/sum -d \'[82, 7, 9, 8, 74]\'', log=log)

        try:
            rq.save()
            print('Test 3: SUCCESS, request created')
        except Exception as e:
            print('Test 3: FAILED, request failed')
            print(e)
        print()

        
        #Create default log object (RECIEVED)
        
        log2 = Log(ID='2', dateTime='2022-07-04 07:14:29.531+01:00', type='RECIEVED', 
        restLogger='1139737886', hostname='master_1', timeline=tm)

        try:
            log2.save()
            print('Test 4: SUCCESS, recieved log created')
        except Exception as e:
            print('Test 4: FAILED, recieved log failed')
            print(e)
        print()

        

        #Create default data object
        
        data = Data(ID='1', statusCode='200', hostname='slave_4', ip='10.1.0.14', result='180', role='SLAVE', log=log2)
        
        try:
            data.save()
            print('Test 5: SUCCESS, data created')
        except Exception as e:
            print('Test 5: FAILED, data failed')
            print(e)
        print()

        print('-------------END OF TEST-------------')

    

    def test2(self):
        '''
        Incorrect object creation
        '''
        #TODO