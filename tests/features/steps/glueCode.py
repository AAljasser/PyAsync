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
Library().createLab('l2045',45)

@given("Lab initialized to be open in 10 seconds")
def step_impl(context):
    pOne.sendO('patron,p1000')
    pTwo.sendO('patron,p1001')
    pThree.sendO('patron,p1002')

@when("PatronOne request to join before the lab is opened")
def step_impl(context):
    pOne.sendO('lab,l2045')

@when("PatronTwo request to join before the lab is opened")
def step_impl(context):
    pTwo.sendO('lab,l2045')

@when("PatronThree request to join before the lab is opened")
def step_impl(context):
    pThree.sendO('lab,l2045')


@then("The Lab has been opened")
def step_impl(context):
    while not Library().getLab('l2045').checkLab():
        None #Waiting until lab is opened

@then("Presume PatronOne and PatronTwo are the users in the Lab")
def step_impl(context):
    time.sleep(5) #We must wait to ensure all queued
    if Library().getLab('l2045').isIn('p1002'):
        print("Patron One Status:"+str(Library().getLab('l2045').isIn('p1000'))+ "Patron Two Status:"+str(Library().getLab('l2045').isIn('p1001')))
        print("The presumption of a 'queue' is refuted by having last Patron to be waiting to enter the lab to enter")
    else:
        print("Patron One Status:"+str(Library().getLab('l2045').isIn('p1000'))+ "Patron Two Status:"+str(Library().getLab('l2045').isIn('p1001')))
        print("The presumption of the implementation of 'queue' has worked")