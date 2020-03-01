from behave import *
from runBG import runBG
from main.Library import Library
import unittest
from main.sClient import sClient
import time
import logging

logging.basicConfig(filename='logs/library.log',level=logging.INFO)
runBG()
pOne = sClient()
pTwo = sClient()


@given('Library contain book bOne')
def step_impl(context):
    Library().bookExists('b1001')

@given('PatreonOne is logged into the terminal')
def step_impl(context):
    pOne.sendO('patreon,p1001')

@given('PatreonTwo is logged into the terminal')
def step_impl(context):
    pTwo.sendO('patreon,p1002')

@when('PatreonOne and PatreonTwo borrows bOne simultaneously')
def step_impl(context):
    pOne.sendO('borrow,b1001')
    pTwo.sendO('borrow,b1001')


@Then('Either PatreonOne or PatreonTwo successfully borrow bOne')
def step_impl(context):
    print(Library().getPatreon('p1001').printBBooks())
    print(Library().getPatreon('p1002').printBBooks())
    if Library().getPatreon('p1001').bExists('b1001'):
        print('Patreon one has successfully borrowed the book')
    elif Library().getPatreon('p1002').bExists('b1001'):
        print('Patreon two has successfully borrowed the book')
    else:
        print('Neither patreon borrowed the book')
