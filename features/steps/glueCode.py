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
The objective of this scenario testing to highlight the impact of thread locking when functions aren't developed to be
thread safe when used in multi-threaded applications. The two main functions in questions are Library.Borrow and Library.regEvent
which are commenting on the checks required to turn our methods into thread safe functions.

Commenting of the solution will induce a crash in DeadLockExOne.feature and induce a Deadlock in DeadLockExTwo.feature
'''

@given('Library contain book bOne')
def step_impl(context):
    Library().bookExists('b1001')

@given('pOne is logged into the terminal')
def step_impl(context):
    pOne.sendO('patron,p1001')

@given('pTwo is logged into the terminal')
def step_impl(context):
    pTwo.sendO('patron,p1002')

#Reference to Library.borrow
@given('pOne borrows bOne')
def step_impl(context):
    pOne.sendO('borrow,b1001')

#Reference to Library.borrow & Library.checkout
@when('pOne checks out cart books before pTwo tries to borrow bOne')
def step_impl(context):
    pOne.sendO('checkout')
    # time.sleep(1)
    pTwo.sendO('borrow,b1001')

@then('pOne gets the book and pTwo receives unavailable book')
def step_impl(context):
    time.sleep(1)
    if Library().getPatron('p1001').bExists('b1001'):
        print('Patron one has successfully borrowed the book')
    else:
        print('Something weird occurred')
#Reference to Library.checkout
@then('pTwo sends a checkout request and nothing is taken')
def step_impl(context):
    time.sleep(1)
    pTwo.send('checkout')
#Reference to Library.regEvent(bid='b1001')
@when('pTwo registers for eventOne with bOne')
def step_impl(context):
    pTwo.sendO('event,e1001,b1001')
#Reference to Library.regEvent(bid=None)
@when('pOne register for eventOne without book request')
def step_impl(context):
    pOne.sendO('event,e1001')
#Reference to Library.checkOut
@when('pOne checksout book')
def step_impl(context):
    pOne.sendO('checkout')

@then('pTwo denied registration pOne registering and owns book')
def step_impl(context):
    time.sleep(1)
    print("If pOne doesn't have true for Book & Event then therefore a deadlock has occurred")
    print("pOne Book One Status:" +str(Library().getPatron('p1001').bExists('b1001')))
    print("pOne Event Reg Status:" +str(Library().getPatron('p1001').inE('e1001')))
    print("pTwo Book One Status:" +str(Library().getPatron('p1002').bExists('b1001')))
    print("pTwo Event Reg Status:" +str(Library().getPatron('p1002').inE('e1001')))