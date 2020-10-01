from behave import *
from main.runBG import runBG
from main.Library import Library
import unittest
from main.sClient import sClient
import time
import logging
from datetime import datetime

logging.basicConfig(filename='logs/library.log',level=logging.INFO)
logging.info("\n\n\n\n\n\n\n\n"+str(datetime.now()))
runBG()
pOne = sClient()
pTwo = sClient()

'''
Simple introduction to thread locking (Solution to race condition)
Solution provided locks all processes then release after individual process has been completed
sServer:Line 54: Introduces thread lock acquiring
sServer:Line 146: Introduces thread lock releasing

Commenting of those lines would produce race condition when the scenario asyncBookBorrow.feature is executed
'''

@given('Library contain book bOne')
def step_impl(context):
    Library().bookExists('b1001')

@given('PatronOne is logged into the terminal')
def step_impl(context):
    pOne.sendO('patron,p1001')

@given('PatronTwo is logged into the terminal')
def step_impl(context):
    pTwo.sendO('patron,p1002')

@when('PatronOne and PatronTwo borrows bOne simultaneously')
def step_impl(context):
    time.sleep(1)
    pOne.sendO('borrow,b1001')
    pTwo.sendO('borrow,b1001')

@Then('PatronOne persumed to be successful borrower')
def step_impl(context):
    time.sleep(2)
    if Library().getPatron('p1001').bExists('b1001'):
        print('Patron one has successfully borrowed the book')
    elif Library().getPatron('p1002').bExists('b1001'):
        print('Patron two has borrowed bOne due to the fact of race condition')
        logging.fatal('Patron two has borrowed bOne due to the fact of race condition')
    else:
        print('Neither patron borrowed the book')
