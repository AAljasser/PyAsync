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
pThree = sClient()
Library().createLab('l2045',10)

'''
Associated Test Unit for QueueRace.feature

The following will provide a description and a reference to the executed statement
'''

'''
The only precondition in the scenario is a Lab has been created and a timer has begun
that would execute Lab.openLab which will allow users to enter the lab

Also not included, the terminal for each of the patrons has been logged in
'''
@given("Lab initialized to be open in 10 seconds")
def step_impl(context):
    pOne.sendO('patron,p1000')
    pTwo.sendO('patron,p1001')
    pThree.sendO('patron,p1002')

'''
Reference Library.joinLab -> Lab.join
The following three consecutive statements are the request to enter the queue line for the lab
which will be opened after the timer has been reached
'''
@when("PatronOne request to join before the lab is opened")
def step_impl(context):
    pOne.sendO('lab,l2045')

@when("PatronTwo request to join before the lab is opened")
def step_impl(context):
    pTwo.sendO('lab,l2045')

@when("PatronThree request to join before the lab is opened")
def step_impl(context):
    pThree.sendO('lab,l2045')

'''
Before continuing the testing we must wait until the lab has been open
and the queue has been processed
'''
@then("The Lab has been opened")
def step_impl(context):
    while not Library().getLab('l2045').checkLab():
        None #Waiting until lab is opened

'''
After the lab has been open we observe the queue processing 
(If solution introduced in Lab.py has been commented out,we would produce a race condition invalidating the queue job)
'''
@then("Confirm PatronOne and PatronTwo are the users in the Lab")
def step_impl(context):
    time.sleep(5) #We must wait to ensure all queued
    if Library().getLab('l2045').isIn('p1002'):
        print("Patron One Status:"+str(Library().getLab('l2045').isIn('p1000'))+ "Patron Two Status:"+str(Library().getLab('l2045').isIn('p1001')))
        print("The presumption of a 'queue' is refuted by having last Patron waiting to enter the lab when two were ahead")
    else:
        print("Patron One Status:"+str(Library().getLab('l2045').isIn('p1000'))+ "Patron Two Status:"+str(Library().getLab('l2045').isIn('p1001')))
        print("The presumed  implementation of 'queue' has worked")