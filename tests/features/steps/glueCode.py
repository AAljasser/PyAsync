from behave import *
from runBG import runBG
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


@given('Library contain book bOne')
def step_impl(context):
    Library().bookExists('b1001')

@given('pOne is logged into the terminal')
def step_impl(context):
    pOne.sendO('patreon,p1001')

@given('pTwo is logged into the terminal')
def step_impl(context):
    pTwo.sendO('patreon,p1002')

@given('pOne borrows bOne')
def step_impl(context):
    pOne.sendO('borrow,b1001')

@when('pOne checks out cart books before pTwo tries to borrow bOne')
def step_impl(context):
    pOne.sendO('checkout')
    # time.sleep(1)
    pTwo.sendO('borrow,b1001')



@then('pOne gets the book and pTwo receives unavailable book')
def step_impl(context):
    time.sleep(1)
    if Library().getPatreon('p1001').bExists('b1001'):
        print('Patreon one has successfully borrowed the book')
    else:
        print('Something weird occurred')

@then('pTwo sends a checkout request and nothing is taken')
def step_impl(context):
    time.sleep(1)
    pTwo.send('checkout')

@when('pTwo registers for eventOne with bOne')
def step_impl(context):
    pTwo.sendO('event,e1001,b1001')
@when('pOne register for eventOne without book request')
def step_impl(context):
    pOne.sendO('event,e1001')

@when('pOne checksout book')
def step_impl(context):
    pOne.sendO('checkout')

@then('pTwo denied registration pOne registering and owns book')
def step_impl(context):
    time.sleep(1)
    print("pOne Book One Status:" +str(Library().getPatreon('p1001').bExists('b1001')))
    print("pOne Event Reg Status:" +str(Library().getPatreon('p1001').inE('e1001')))
    print("pTwo Book One Status:" +str(Library().getPatreon('p1002').bExists('b1001')))
    print("pTwo Event Reg Status:" +str(Library().getPatreon('p1002').inE('e1001')))