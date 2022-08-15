'''
Database testing script
'''
from xml.dom import ValidationErr
from django.test import TestCase, TransactionTestCase
from timeline.models import *
from django.db.utils import IntegrityError
from django.db import transaction
from django.core.exceptions import ValidationError


class CorrectDatabaseTests(TestCase):

    def test(self):
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

    

class IncorrectDatabaseTests(TransactionTestCase):

    def test(self):
        '''
        Object creation without relationships
        '''
        
        print()
        print('-------------OBJECTS WITHOUT RELATIONSHIPS TESTS-------------')
        print()

        #Create default data object without log
        
        data = Data(ID='1', statusCode='200', hostname='slave_4', ip='10.1.0.14', result='180', role='SLAVE')
        
        try:
            data.save()
            print('Test 1: FAILED, data created without log')
        except IntegrityError as e:
            print('Test 1: SUCCESS, data creation failed without log')
            #print(e)
        print()

        #Create default request object without log
        
        rq = Request(ID='1', requestType='POST', params='-X', 
        URL='http://10.1.0.14:5620/math/sum -d \'[82, 7, 9, 8, 74]\'')

        try:
            rq.save()
            print('Test 2: FAILED, request created without log')
        except IntegrityError as e:
            print('Test 2: SUCCESS, request creation failed without log')
            #print(e)
        print()

        #Create default log object (RECIEVED) without timeline
        
        log1 = Log(ID='1', dateTime='2022-07-04 07:14:29.531+01:00', type='RECIEVED', 
        restLogger='1139737886', hostname='master_1')

        try:
            log1.save()
            print('Test 3: FAILED, recieved log created without timeline')
        except IntegrityError as e:
            print('Test 3: SUCCESS, recieved log creation failed without timeline')
            #print(e)
        print()

        #Create default log object (SENT)
        
        log2 = Log(ID='2', dateTime='2022-07-04 07:14:29.523+01:00', type='SENT', 
        restLogger='1139737886', hostname='master_1')

        try:
            log2.save()
            print('Test 4: FAILED, sent log created without timeline')
        except IntegrityError as e:
            print('Test 4: SUCCESS, sent log creation failed without timeline')
            #print(e)
        print()

        print('-------------END OF TEST-------------')

class IncorrectAttributesTests(TransactionTestCase):

    def test(self):
        '''
        Create objects with incorrec attribute formats
        '''

        print()
        print('-------------OBJECTS WITH INCORRECT ATTRIBUTES-------------')
        print()

        # Timeline object

        tm = Timeline(IP='10.1.0.14:5620')
        tm.save()

        # Log with type too long

        log = Log(ID='1', dateTime='2022-07-04 07:14:29.523+01:00', type='TYPETOOLONG', 
        restLogger='1139737886', hostname='master_1', timeline=tm)

        try:
            log.full_clean()
            log.save()
            print('Test 1: FAILED, log created with type too long')
        except ValidationError as e:
            print('Test 1: SUCCESS, log creation failed with type too long')
        print()

        #-------------

        # Log object
        log = Log(ID='1', dateTime='2022-07-04 07:14:29.523+01:00', type='SENT', 
        restLogger='1139737886', hostname='master_1', timeline=tm)

        # Request with request type too long

        rq = Request(ID='1', requestType='SOMETHINGOTHERTHANGETORPOST', params='-X', 
        URL='http://10.1.0.14:5620/math/sum -d \'[82, 7, 9, 8, 74]\'', log=log)

        try:
            rq.full_clean()
            rq.save()
            print('Test 2: FAILED, request created with request type too long')
        except ValidationError as e: 
            print('Test 2: SUCCESS, request creation failed with request type too long')
        print()

        # Data with non-integer status code

        data = Data(ID='1', statusCode='200_', hostname='slave_4', ip='10.1.0.14', result='180', role='SLAVE')

        try:
            data.save()
            print('Test 3: FAILED, data created with non integer status code')
        except ValueError as e:
            print('Test 3: SUCCESS, data creation failed with non integer status code')
        print()

        print('-------------END OF TEST-------------')