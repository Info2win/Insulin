"""
This program calculates the amount of additional insulin that five Type-1 diabetics should take for the blood glucose level to be above 120 mg/dl.

This program requires Python 3.9 or above.
This program flows from the main function.
Every input taken by this program have a pattern and user must obey the pattern.
"""
from typing import List, Pattern, Dict, Annotated, Iterable, Tuple
import re
from functools import reduce
import itertools

patientCount:Annotated[int,"Patient count that are in service."]
totalInsulin:Annotated[int,"Total insulin that is taken by a patient."] = 0
decreaseList: Annotated[List[int],"A list to hold how much blood sugar should decrease for values above 120."] = []
name: Annotated[str,"Temporary var to hold patient name"] = ""
namesList: Annotated[List[str],"List of the names of the patients that are in the service."] = []
glucoseValuesDict: Annotated[Dict[str,List[int]],"Keys: Patients' names, Values: Patient's 12-hour blood glucose values."]= {}
over120Dict: Annotated[Dict[str,List[int]],"Keys: Patients' names, Values: Patient's 12-hour blood glucose values that are over 120."] = {}
doesesList:Annotated[List[int],"Doses taken in 12 hours"] = []
unitsDict:Annotated[Dict[str,List[Tuple[float,int]]]," "] = {}
insulinTakenCount: Annotated[int,"Number of times insulin is taken in 12 hours and these insulin doses."]

patientCountPattern: Annotated[Pattern[str],"A input pattern to input patient count."] = re.compile(r"\s*\d\s*")
namePattern: Annotated[Pattern[str],"A input pattern to input names' of the patients."] = re.compile(r"\s*[a-zA-Z]+\s*")
values12HourPattern: Annotated[Pattern[str],"A input pattern to input the glucose values that are taken by the patient in 12 hours."] = re.compile(r"\s*(\d+\s){11}\d+\s*")
totalInsulinPattern:Annotated[Pattern[str],"A input pattern to input the number of times insulin is taken in 12 hours."] = re.compile(r"\s*\d\s*")


def main() -> None:
    """ Input how many patients in service.
    While input patient count is invalid, print error and request patient count again.
    For each patient reset the values of global variables.
    For each patient take patient's name and 12-hour blood glucose values.
    For each patient determine and print values above 120 mg/dl.
    For each patient input insulin doses taken in 12 hours.
    For each patient print 12-hour blood glucose values.
    For each patient's each blood glucose value that is above 120 mg/dl calculate and print the unit of insulin that they shoud take.
    """
    global patientCount,decreaseList,totalInsulin,doesesList 
    patientCount = input("Enter have many patients in service:")
    while not (re.fullmatch(patientCountPattern,patientCount)) :
        print("Please enter a valid patient count!")
        patientCount = input("Enter have many patients in service:")
    if re.fullmatch(patientCountPattern,patientCount):
        patientCount = int(patientCount)
        for _ in range(patientCount):
            decreaseList,doesesList = [],[] # empty the lists for each patient
            totalInsulin = 0 # reset total Insulin taken for each patient
            input_names()
            input_12_hour_glocuse_values()
            determine_glocuse_values_above_120()
            print_values_above_120()
            input_insulin_doses_taken_in_12_hours()
            calculate_total_insulin()
            calculateDecrease()
            calculate(totalInsulin,decreaseList)
    print("12-hour blood glucose values of patients in service:")
    print(glucoseValuesDict)
    print_insulin_needed()

def input_names() -> None:
    """Input name of a patient into a global variable called name."""
    global name
    name = input("Enter patient name: ")
    if re.fullmatch(namePattern,name):
        namesList.append(name)
    else:
        print("Plase enter a valid name!")
        input_names()
    
    
def input_12_hour_glocuse_values() -> None:
    """Input a patient's 12-hour blood glucose values into a global dictonary.
    Keys of the dictionary are the names of the patients.
    """
    global glucoseValuesDict
    intList:List[int] = []
    tempStrList: str = input("Enter patient's 12-hour blood glucose values: ")
    if re.fullmatch(values12HourPattern,tempStrList):
        for i in tempStrList.split():
            intList.append(eval(i))
        glucoseValuesDict[name] = intList
    else:
        print("Please enter valid values!")
        input_12_hour_glocuse_values()

def determine_glocuse_values_above_120() -> None:
    """Filteres a patient's glocuse values list by being above of 120."""
    global over120Dict
    filtered: List[int] = list(filter(is_above_120,glucoseValuesDict[name]))
    over120Dict[name] = filtered

def input_insulin_doses_taken_in_12_hours() -> None:
    """Inputs Number of times insulin is taken in 12 hours and these insulin doses in to a global variable which is a list of integers called doesesList"""
    global insulinTakenCount
    tempCount = input("How many times did you take insulin in 12 hours?:")
    if re.fullmatch(totalInsulinPattern,tempCount):
        insulinTakenCount = int(tempCount)
    else:
        print("Please enter a valid count!")
        input_insulin_doses_taken_in_12_hours()
    input_doeses(insulinTakenCount)

        
def input_doeses(insulinTakenCount:int) -> None:
    """Inputs the doses taken in 12 hours.
    While dose values are invalid, prints an error and request input again.
    
    Args: insulinTakenCount(int64): How many times that insulin is taken in 12 hours in integer format.
    """
    global doesesList
    inputDosesPattern: Annotated[Pattern[str],"Input pattern to input the doses taken in 12 hours"] = re.compile(r"(\s*\d\s*){" + str(insulinTakenCount-1) +"}\d\s*")
    doesesStr = input("Enter insulin doses: ")
    if re.fullmatch(inputDosesPattern,doesesStr):
        for i in doesesStr.split():
            doesesList.append(int(i))
    else:
        print("Invalid input. Please try again!")
        input_doeses(insulinTakenCount)

def calculate_total_insulin() -> None:
    """Calculates the total amount of insulin into a global variable called totalInsulin."""
    global totalInsulin, doesesList
    totalInsulin = int(reduce(lambda a,b: a+b ,doesesList))
def calculateDecrease() -> None:
     for value in over120Dict[name]:
        decreaseList.append(value-120)

def calculate(totalInsulin:int,decreaseList:List[int]) -> None:
    """Calculates how many mg/dl a unit of insulin lowers blood sugar.
    
    Args:
        totalInsulin(int64): Total amount of insulin that is taken by a patient in 12 hours in integer format.
        decreaseList(List[int64]): The difference between values above 120 mg/dl minus 120 in integer list format.
    """
    lowers:Annotated[int,"How many mg/dl a unit of insulin lowers blood sugar."] = 1800 // totalInsulin
    unitsDict[name] = []
    for (decreaseValue,value) in zip(decreaseList,over120Dict[name]):
        unitsDict[name].append(((decreaseValue / lowers),value))


def print_insulin_needed() -> None:
    """Prints how much unit insulin should be taken for each value that is above 120 mg/dl for the each patient."""
    for name in namesList:
        print(name + " should take")
        for i in range(len(over120Dict[name])):
            print("%.2f unit insulin for " % unitsDict[name][i][0] + str(unitsDict[name][i][1]) + " mg/dl")

def print_values_above_120() -> None:
    """Prints the patient names and glucose values that are above 120 mg/dl as a dictionary."""
    print("Glucose values over 120 mg/dl : ", end = " ")
    print(over120Dict[name])
def is_above_120(value:Annotated[int,"Patient's glucose value to be tested for being above of 120"])->bool:
    """Returns True if Patient's glucose value is above 120 mg/dl.
    Else returns False.
    
    Args:
        value(int64): Patient's glucose value in integer format.
    
    Returns:
        boolean: If patient's glucose value above of 120 or not.
    """
    if value > 120:
        return True
    else:
        return False

main()
