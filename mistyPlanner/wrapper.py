from pyshop import *
import os.path
import os
from os import path
import json
from pathlib import Path
import sys

#ctrl + k + c == comment
#ctrl + k + u == uncomment 

'''Used for psiPyShopServer.py'''
def psiConditions(name, itemHelp, engagement, levelHelp, userLocation, taskLocation, objLocation, urgencyLevel):

    ps = PyShop('init')
    filePath = "robotBehaviors.hddl"

    ps.declare_methods(filePath)   
    ps.declare_operators(filePath)  
    
    ps.print_operators()
    ps.print_methods()
 
    state1 = State("agent")
    plan = psiStateGenerator(state1, ps, name, itemHelp, engagement, levelHelp, userLocation, taskLocation, objLocation, urgencyLevel)
    
    finalList = []

    print("\nPlan for task\n_________________________\n")    

    if plan != None:
        for list in plan:
            actionList = {}
            print(list[0])
            temp = []
            for i in range(len(list[0])-1):
                temp.append(list[0][i+1])
            actionList[list[0][0]] = temp
          
            finalList.append(actionList)

    mistyList = fixList(finalList)
     
    description = "" #can optionally add a description to the JSON file
    actionScript = {"intent": itemHelp, "description" : description, "actionList": mistyList}

    #temp fileName
    fileName = "temp"
    with open(os.path.join(r"C:\xampp\htdocs", fileName + ".json"), "w") as convert_file:
        convert_file.write(json.dumps(actionScript))

    return actionScript

'''Selects the text correlating to the item of help. Can add more items to the function and eventually generalize down'''
def textSelector(itemHelp, levelHelp):
    
    itemHelp.lower()

    if itemHelp == "vanilla":
        if levelHelp == '1':
            infoText = "Keep up the great work!"
        elif levelHelp == '2':
            infoText = "An ingredient is still missing!"
        elif levelHelp == '3':
            infoText = "You still need to add the vanilla to your recipe!"
        else:
            infoText = "The missing vanilla is right over there! By the flour!"

    if itemHelp == "chocolate":
        if levelHelp == '1':
            infoText = "Keep up the great work!"
        elif levelHelp == '2':
            infoText = "Something is still missing!"
        elif levelHelp == '3':
            infoText = "You still need to add the chocolate to your recipe!"
        else:
            infoText = "The missing chocolate is right over there! By the butter!"

    return infoText

'''generates the state of the task and user from psiPyShopServer input'''
def psiStateGenerator(state1, ps, name, itemHelp, engagement, levelHelp, userLocation, taskLocation, objLocation, urgencyLevel):

    state1.add(["user", name])

    engagement.lower()

    if engagement != "no":
        state1.add(["userEngaged", name])

    #level of help
    state1.add(["level", levelHelp])
    state1.add(["eq", "1", "1"])
    state1.add(["eq", "2", "2"])
    state1.add(["eq", "3", "3"])
    state1.add(["eq", "4", "4"])

    state1.add(["eq","thinking","thinking"])

    urgencyLevel.lower()
    if urgencyLevel == "high":
        state1.add(["urgencyLevel", "high"])

    #Manner
    state1.add(["manner", "polite"])

    #Location information
    state1.add(["userLocation", userLocation])
    state1.add(["taskLocation", taskLocation])
    state1.add(["objectLocation", objLocation])

    infoText = textSelector(itemHelp,levelHelp)
   
    plan = ps.pyshop(state1, [["GiveHelp",itemHelp, levelHelp, infoText]], 0)

    return plan

def initialState(state1, ps):

    name = str(input("Enter the user's name: "))

    state1.add(["user", name])

    userEngagement = str(input("\nIs the user engaged? Yes or No \n")) 
    userEngagement.lower()

    if userEngagement != "no":
        state1.add(["userEngaged", name])

    itemHelp = str(input("What item does the user need help with?\n"))

    level = str(input("What is the level of help from 1-4?\n"))

    #level of help
    state1.add(["level", level])
    state1.add(["eq", "1", "1"])
    state1.add(["eq", "2", "2"])
    state1.add(["eq", "3", "3"])
    state1.add(["eq", "4", "4"])

    #state1.add(["urgencyLevel", "high"])

    state1.add(["eq","thinking","thinking"])

    #Manner
    state1.add(["manner", "polite"])

    #Location information
    state1.add(["userLocation", "center"])
    state1.add(["taskLocation", "down"])
    state1.add(["objectLocation", "lowerLeft"])

    #Picks the text relevant to the item and level
    infoText = textSelector(itemHelp,level)
   
    plan = ps.pyshop(state1, [["GiveHelp","vanilla", level, infoText]], 0)

    return plan


def getActionList(intent):
    ps = PyShop('init')
    filePath = intent + ".hddl"

    ps.declare_methods(filePath)   
    ps.declare_operators(filePath)  
    
    ps.print_operators()
    ps.print_methods()
 
    state1 = State("agent")

    #Terminal interactive plan generation with inputted state conditions
    plan = initialState(state1,ps)
    
    finalList = []

    print("\nPlan for task\n_________________________\n")    

    if plan != None:
        for list in plan:
            actionList = {}
            print(list[0])
            temp = []
            for i in range(len(list[0])-1):
                temp.append(list[0][i+1])
            actionList[list[0][0]] = temp
          
            finalList.append(actionList)

    
    return finalList


#Adds the "name" and "args" keys for the actionList to execute properly on Misty    
def fixList(list):

    finalList = []

    for item in list:
        temp_dict = {}
        for key in item.keys(): #gets the name of the actions
            temp_name = key

        temp_args = item.get(temp_name)

        temp_dict["name"] = temp_name
        temp_dict["args"] = temp_args
        finalList.append(temp_dict)

        #print("FINAL LIST: ",finalList)


        #print("ARGS: ",temp_args)
        #print("item: ", item)

    return finalList

def createFile(fileName, intent, description = None):
    
    list = getActionList(intent)
    mistyList = fixList(list)
     
    actionScript = {"intent": intent, "description" : description, "actionList": mistyList}

    with open(os.path.join(fileName + ".json"), "w") as convert_file:
        convert_file.write(json.dumps(actionScript))
    

def main():
    #for command line input
    #interactive = str(sys.argv[1])

    #To activate the terminal interactive mode before running the psiPyShopServer
    interactive = str(input("Would you like the interactive terminal version? yes or no\n")) 

    if interactive == "yes":

        print("Interactive", interactive)
        print("Misty's interface\n")
    
        intent = str(input("Intent: ")) #set as intent's value in the dict. currently have missingPiece2 and notDone4
        fileName = str(input("File Name: ")) #this is the fileName which will be saved onto the computer

        '''Ensures that files don't get overwritten''' 
        while (path.exists(fileName + ".json")):
            option = int(input("\nThat file already exists. \nPress 1 to overwrite the existing file or 2 to enter a new file name: "))
            if option == 1:
                os.remove(fileName + ".json")   
                break
            elif option == 2:
                fileName = str(input("File Name: "))

        print("\n")

        createFile(fileName, intent)
    else:
        pass

main()  
