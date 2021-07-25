"""
Creater: @Saad Mahboob
Date: 03/27/2021
"""

import re, sys
from HDDLParser import HTNParsingLibrary
from HDDLParser import HTNMethod
from HDDLParser import HTNParameter
from HDDLParser import HTNOperator

class HTNParser:
    
    def __init__(self, filePath):
        self.filePath = filePath
        self.methods = []
        self.operators = []
        self.task = None

        fp = open(self.filePath, 'r')
        self.lines = fp.readlines()
        self.idx = 0
        self.extract(fp)
    
    def extract(self,fp):
        while(self.idx < len(self.lines)):
            line = self.lines[self.idx].strip()

            if HTNParsingLibrary.METHOD_START in line:
                #call method defination class and parse the whole method inside that
                #when creating method object, pass the list of lines so it can extract the code and also pass starting index
                #return the index for the next line that needs to be read and set idx = that so we parse from there on
                #push that specific method object that is created into the methods list.
                method = HTNMethod.HTNMethod(self.idx,self.lines)
                self.idx = method.index
                self.task = method.task
                self.methods.append(method)
                    
            elif HTNParsingLibrary.OPERATORS_START in line:
                #call operator defination class and parse the whole operator inside that
                #when creating operator object, pass the list of lines so it can extract the code and also pass starting index
                #return the index for the next line that needs to be read and set idx = that so we parse from there on
                #push that specific operator object that is created into the methods list
                operator = HTNOperator.HTNOperator(self.idx,self.lines)
                self.idx = operator.index
                self.operators.append(operator)
            self.idx +=1
        fp.close()    
        
    def get_methods(self):
        return self.methods

    def get_operators(self):
        return self.operators
        
    def get_relevant_methods(self, taskName, method_dictionary, state, parameters):
        
        #when checking the precondition, if we dont know the value then we go and find that value
        #in the facts of state and do the bindings
        #however if we already have a value of the precondition, we match that value 
        #from the facts at the state to see if they match
        #if they match then that method should be part of relevent methods, otherwise not

        #print("\n\nWhat are the parameters? ", parameters, "\n\n")

        all_methods = method_dictionary[taskName]
        relevant_methods = []    
        
        for method in all_methods:
            relevant = True

            #DEBUG
            #print("\nCurrent method: " + method.get_name())
            #print("\nPreconditions: ", method.preconditions)

            method.do_bindings(parameters)
            binding = method.bindings.get_bindings()
            found_preconditions = []
        
            precondition = method.preconditions

            for condition in precondition:
                #DEBUG
                #print("\nState Facts: ", state.facts) 
                for facts in state.facts:

                    if (len(facts) != 0) and (condition[0].strip() not in found_preconditions):
                        
                        if(condition[0].strip() == facts[0].strip()):
                            #print("---------Found precondition in state: " , facts)
                            relevant = True
                            
                            for i in range(1,len(condition)):
                                val = condition[i]
                                fac = facts[i]
                                if(relevant):                                
                                    if(val.find("?") != -1):

                                        if val in binding:
                                            cur = method.bindings.get_bindings()[val]
                                            if(fac == cur):
                                                relevant = True
                                                found_preconditions.append(condition[0].strip())
                                                #print("1-This is a relevant method because " + cur + " and " + fac + " match" )
                                            else:
                                                #print("2-This is not a relevant method because " + val + ":" +  cur + " and " + fac + " dont match" )

                                                relevant = False
                                                
                                        else:
                                            #print("3-This is relevant method because we just updated its bindings for " + condition[0].strip())  
                                            method.bindings.update_bindings(val, facts[i])
                                            relevant = True
                                            found_preconditions.append(condition[0].strip())
                
                                    else:
                                        if (val == fac):
                                            relevant = True
                                            found_preconditions.append(condition[0].strip())
                                            #print("4-This is a relevant method because " + val + " and " + fac + " match" )
                                        else:
                                            #print("5-This is not a relevant method because " + val + " and " + fac + " dont match" )
                                            relevant = False
                                            break
                            
                        else:
                            #print("Still Looking for: " , condition[0].strip())
                            relevant = False
                            
                if(not relevant):
                    break
            
            if(relevant):
                relevant_methods.append(method)   

        return relevant_methods
