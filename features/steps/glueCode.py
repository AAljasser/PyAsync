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
staff = sClient()
pOne = sClient()
pTwo = sClient()

'''
Scenario: Staff member creation of a Patron

Reference to Library.userLogin() & sServer (Line: 68-80)
'''
@given(u'Staff member logged into terminal')
def step_impl(context):
    staff.send('staff,s1000')

'''
Reference to Library.userLogin() & sServer (Line: 95-106)
'''
@when(u'Staff sends \'crpatron,p2020,NAME\' command')
def step_impl(context):
    staff.send('crpatron,p2020,NAME')

'''
Reference to Library.patronExists())
A wait will usually appear before the @then (Validation step) due to
the fact that Behave execute all of the scenario's steps asynchronously 
'''
@then(u'Validate \'p2020\' has been created')
def step_impl(context):
    if Library().patronExists('p2020'):
        logging.info("(Staff member creation of a Patron) has executed successfully")
    else:
        logging.fatal("(Staff member creation of a Patron) has failed in Valid path testing!")
        raise SystemError("(Staff member creation of a Patron) has failed in Valid path testing!")

'''
Reference to Library.userLogin() & sServer (Line: 68-80)
'''
@given(u'Patron logged into terminal')
def step_impl(context):
    pOne.send('patron,p1000')



'''
Scenario: Patron Borrowing a Book

Reference to Library.bookExists
'''
@given(u'book \'b1001\' exists')
def step_impl(context):
    if not Library().bookExists('b1001'):
        raise SystemError("(Patron Borrowing a Book) Book does not exists in the Library invalidating the scenario")

'''
Reference to Library.borrow & sServer Line 120-129
'''
@when(u'Patron send \'borrow,b1001\' command')
def step_impl(context):
    pOne.send('borrow,b1001')

'''
Reference to Library.checkout  & sServer Line 138-146
'''
@when(u'Patron send \'checkout\' command')
def step_impl(context):
    pOne.send('checkout')

'''
Reference to Patron.bExists
'''
@then(u'Validate Patron has taken the b1001')
def step_impl(context):
    if not Library().getPatron('p1000').bExists('b1001'):
        raise SystemError("(Patron Borrowing a Book) Book hasn't been borrowed")

'''
Reference to Library.bookExists
'''
@then(u'Validate Library removal of b1001')
def step_impl(context):
    if Library().bookExists('b1001'):
        raise SystemError("(Patron Borrowing a Book) Book hasn't been removed after borrowing")


'''
Scenario: Patron registration of newly created Event with book b2020

The following scenario is provided to allow for better understanding of the system processing

Beginning with staff creation of an event referencing Library.createEvent & sServer Line: 89-94
'''
@given(u'Staff creating e2020 using \'crevent,e2020\' command')
def step_impl(context):
    staff.send('cevent,e2020')

'''
The following command has important reference as this has an optional addition of including a book
Library.regEvent(patron,event,**Optional**=Book) is a thread safe that allows registration and borrowing of a book
sServer Lines: 152-180
'''
@given(u'Patron failed attempt to register to event with non existing book b2020')
def step_impl(context):
    pOne.send('event,e2020,b2020') #Validate correctness through logs

'''
Library.addBook & sServer line: 108-119
'''
@when(u'Staff create Book \'addbook,b2020,TestingScenarioBook\'')
def step_impl(context):
    staff.send('addbook,b2020,TestingScenarioBook')

'''Similar to the previous step'''
@when(u'Patron reattempt to register to event with b2020 using \'event,e2020,b2020\'')
def step_impl(context):
    pOne.send('event,e2020,b2020')

'''
Crucial function to validate correctness
Patron.bExists: Checks if the requested patron contain specified book
Patron.inE: Checked if patron is registered in Event E
'''
@then(u'Validate Patron registration and acquiring of book')
def step_impl(context):
    if not Library().getPatron('p1000').bExists('b2020'):
        raise SystemError("(Patron registration of newly created Event with book b2020) Book hasn't been borrowed")
    elif not Library().getPatron('p1000').inE('e2020'):
        raise SystemError("(Patron registration of newly created Event with book b2020) Patron hasn't registered in Event e2020")
    else:
        logging.info("(Patron registration of newly created Event with book b2020) has executed successfully")

'''
Scenario: Patron Listing Available Labs

This just to allow the idea of checking eventing by sending a single word like (event,lab,etc...) 
'''
@given(u'Patron loged into terminal')
def step_impl(context):
    pTwo.send('patron,p1001')


@when(u'Patron types \'lab\'')
def step_impl(context):
    pTwo.send('lab')


@then(u'Patron recieves a list of available labs')
def step_impl(context):
    None#Obserable through console

'''
Scenario: Two Patron queue to unopned lab

This is explaied when tackling queue and thread locking, but the main important function is
Library().getLab('l2020')(Lab.py).checkLab() which allowed us to let the thread get into the system
"and get into line for the lab" and we check that both are in and logging it
'''

@given(u'Staff creating a lab to be opened \'clab,l2020\'')
def step_impl(context):
    staff.send('clab,l2020')

@when(u'Patron One joins lab using \'lab,l2020\'')
def step_impl(context):
    pOne.send('lab,l2020')

@when(u'Patron Two joins lab using \'lab,l2020\'')
def step_impl(context):
    pTwo.send('lab,l2020')

@then(u'Validate Patron\'s entrance')
def step_impl(context):
    while not Library().getLab('l2020').checkLab():
        None # Looping until the lab has been opened
    if Library().getLab('l2020').isIn('p1000') and Library().getLab('l2020').isIn('p1001'):
        logging.info("(Two Patron queue to unopned lab) has executed successfully")
    else:
        raise SystemError("(Two Patron queue to unopned lab) Either patrons didn't get in")