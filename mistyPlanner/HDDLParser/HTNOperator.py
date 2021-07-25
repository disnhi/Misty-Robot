"""
Creater: @Saad Mahboob
"""
"""
    HTNOperator class contains the following fields:
    1) name
    2) parameters -> arguments that have been passed into the operator 
    3) operator_code -> lines of codes containing the whwhole operator
    4) preconditions -> these are probably strings(for now) which need to be true for the operator to work
    6) effects -> these are the positive and negative impacts
"""

import re, sys
from HDDLParser import HTNParsingLibrary, HTNMethod, HTNParameter, HTNOperator, HTNBinder

class HTNOperator:

    def __init__(self, idx, lines):
        
        self.lines = lines #these are the total lines of code passed into
        self.index = idx   #this is the start index that we need to look at, will become end index
        self.operator_code = []  #this contains the list of lines of the specific section of code
        self.operator_name = lines[self.index][8:].strip()
        
        self.parameters = []
        self.operator_code = []
        self.parenthesis = []
        self.preconditions = []
        self.positiveEffects = []
        self.negativeEffects = []
        self.bindings = {}

        self.extract_code()
        self.extract_parameters()
        self.extract_preconditions()
        self.extract_effects()
        

    def get_name(self):
        return self.operator_name
    
    def extract_code(self):
        self.parenthesis.append(HTNParsingLibrary.OPENING_PARENTHESIS)
        #we have already extracted name from 1st line, so now shift to next before looping
        self.index = self.index + 1 
        while(self.index < len(self.lines) and len(self.parenthesis) != 0):
            cur_line = self.lines[self.index]
            self.operator_code.append(cur_line)
            self.index += 1

            #this keeps track of opening and closing parenthesis to extract the operator code
            for char in cur_line:
                if HTNParsingLibrary.OPENING_PARENTHESIS in char:
                    self.parenthesis.append(HTNParsingLibrary.OPENING_PARENTHESIS)
                if HTNParsingLibrary.CLOSING_PARENTHESIS in char:
                    self.parenthesis.pop()

    def extract_parameters(self):
        for line in self.operator_code:
            if HTNParsingLibrary.PARAMETERS_START in line:
                #this extracts out the parameter line from the code by checking start and end of closing parenthesis
                #we replace all the spaces to strip the line
                idx_start = line.find(HTNParsingLibrary.OPENING_PARENTHESIS)+1
                idx_end = line.find(HTNParsingLibrary.CLOSING_PARENTHESIS)-1
                parameter_line = line[idx_start:idx_end+1].replace(" ", "") + " "
                
                while(len(parameter_line) > 1):
                    #values start at '?' and end at '-' this can somtimes hold multiple values of same type
                    value_start = parameter_line.find(HTNParsingLibrary.PARAMETER_VALUE_START)
                    value_end = parameter_line.find(HTNParsingLibrary.PARAMETER_VALUE_END)
                    value = parameter_line[value_start:value_end]
                    value =  value.replace(" ", "")
                    
                    #type starts at '-' always and can end with either '?' or ')' check for ')' if '?' not found
                    type_start = parameter_line.find(HTNParsingLibrary.PARAMETER_TYPE_START)+1
                    type_end = parameter_line.find(HTNParsingLibrary.PARAMETER_TYPE_END1, value_end)
                    if(type_end == -1):
                        type_end = parameter_line.find(HTNParsingLibrary.PARAMETER_TYPE_END2)

                    #this stores the type of parameter that is extracted, for example location
                    par_type = parameter_line[type_start:type_end].strip()
                    multiple_par = value.count("?")

                    for _ in range(multiple_par-1):
                        find_first_qMark = value.find("?")
                        find_second_qMark = value.find("?",find_first_qMark+1)
                        val = value[find_first_qMark:find_second_qMark]
                        #call parameter object and store the values and types and add to parameter list
                        parameter1 = HTNParameter.HTNParameter(par_type, val)
                        self.parameters.append(parameter1)
                        value = value[find_second_qMark:]

                    #the last one left behind, either went into loop or not would be added into list here
                    parameter = HTNParameter.HTNParameter(par_type, value)
                    self.parameters.append(parameter)
                    
                    #keep shortening the parameter line and loop until there is just one or less element left
                    parameter_line = parameter_line[type_end:]                
                break

    def extract_preconditions(self):
        #the following helps us get the starting line from the whole operator, where preconditions start
        line = ""
        idx1  = 0
        for idx in range(len(self.operator_code)):
            line = self.operator_code[idx]
            if HTNParsingLibrary.PRECONDITIONS_START in line:
                line = self.operator_code[idx+1]
                idx1 = idx+1
                break
            
        #this stack is to match parenthesis of the precondition code 
        stack = []
        #starting parenthesis of the precondition, we skipped the first line, so we add it here
        stack.append(HTNParsingLibrary.OPENING_PARENTHESIS) 
        precondition_code = []

        #this here is to match parenthesis of each line in task and stop when the precondition section is over
        #this whole loop extracts the code of precondition into the preconditon code list
        while(len(stack) != 0):
            for char in line:
                if HTNParsingLibrary.OPENING_PARENTHESIS in char:
                    stack.append(HTNParsingLibrary.OPENING_PARENTHESIS)
                elif HTNParsingLibrary.CLOSING_PARENTHESIS in char:
                    stack.pop()
            
            precondition_code.append(line)

            if(len(stack) != 0):
                idx1 += 1
                line = self.operator_code[idx1]

        #this is to extract preconditions out of the lines and push them into final list of list
        for precondition in precondition_code:
            precondition = precondition.strip()
            #remove the parenthesis from the precondition
            condition = precondition.replace("(","").replace(")","")
            findQ = condition.split("?")
            
            #first element of this is always not a value so add that without a '?'
            list_condition = []
            list_condition.append(findQ[0])
            
            #in this loop add all the values of a precondition, added a ? before to show its a value
            for i in range(1,len(findQ)):
                list_condition.append("?"+findQ[i])
            self.preconditions.append(list_condition)

    def extract_effects(self):
        line = ""
        idx1  = 0
        for idx in range(len(self.operator_code)):
            line = self.operator_code[idx]
            if HTNParsingLibrary.OPERATORS_EFFECT_START in line:
                line = self.operator_code[idx+1]
                idx1 = idx+1
                break

        stack = []
        
        #effects are the last one, so we have to add 2 parenthesis to create balance while matching
        stack.append(HTNParsingLibrary.OPENING_PARENTHESIS) #starating parenthesis of the precondition
        stack.append(HTNParsingLibrary.OPENING_PARENTHESIS) #starating parenthesis of the operator code
        effectsCode = []

        #this here is to match parenthesis of each line in task and stop when the precondition section is over
        while(len(stack) != 0):
            for char in line:
                if HTNParsingLibrary.OPENING_PARENTHESIS in char:
                    stack.append(HTNParsingLibrary.OPENING_PARENTHESIS)
                elif HTNParsingLibrary.CLOSING_PARENTHESIS in char:
                    stack.pop()
            
            effectsCode.append(line)

            if(len(stack) != 0):
                idx1 += 1
                line = self.operator_code[idx1]
        
        #now extract the positive and negative effects
        for effect in effectsCode:
            findNot = effect.find("not")
            if findNot != -1:
                effects = effect.split("(not")
                
                for each in effects:
                    each = each.strip()
                    if each != "":
                        idx_start = each.find(HTNParsingLibrary.OPENING_PARENTHESIS)+1
                        idx_end = each.find(HTNParsingLibrary.CLOSING_PARENTHESIS)
                        foundEffect = each[idx_start:idx_end]
                        
                        self.negativeEffects.append(foundEffect.split())
            else:
                effect = effect.strip()
                idx_start = effect.find(HTNParsingLibrary.OPENING_PARENTHESIS)+1
                idx_end = effect.find(HTNParsingLibrary.CLOSING_PARENTHESIS)
                foundEffect = effect[idx_start:idx_end]
                self.positiveEffects.append(foundEffect.split())
        
    def execute(self,state,parameter_list): 
        #create a binding objecet, and loop through all parameters 
        #and the parameter list that is passed into it and update the bindings accordingly
        bindings = HTNBinder.HTNBinder()
                
        for i in range(len(parameter_list)):
            parameter = self.parameters[i]
            key = parameter.getValue()
            value = parameter_list[i]
            bindings.update_bindings(key, value)
        
        self.bindings = bindings
        
        #print("\nparameter list passed: " , parameter_list) 
        #print("operator bindings: " , bindings.get_bindings())

        #go through the preconditions
        #replace the arguments that we already know about the preconditions
        #firstly we check in our bindings dictionary
        #then we call the state to check its bindings dictionary
        #if not in state, return false, if found in state, we then update our bindings and then update variables   
        
        for precondition in self.preconditions:  
            for i in range(len(precondition)):
                cur = precondition[i].strip()
                if(cur.find("?") != -1):
                    if(cur in self.bindings.get_bindings().keys()):
                        precondition[i] = self.bindings.get_bindings()[cur]
                    else:
                        bind = state.ask(cur)
                        if bind == False:
                            return False
                        else:
                            self.bindings.addAnotherBinding(bind)
                            precondition[i] = self.bindings.get_bindings()[cur]

                        
        #print("Preconditions: ", self.preconditions)
        #print("Positive Effects: ", self.positiveEffects)
        #print("Negative Effects: ", self.negativeEffects)     
        #sys.exit(0)
        
        # ask the state if state has seen this fact (preconditions)
            # if yes: 
            # return new bindings based on that ask
            # fill in the empty variables and add these returned bindings from state
            # into the self.bindings for the operator
            # if no:
                #returning false to the execute method (meaning pre condition not fulfilled)
        
        #loop through all positive effects, ground each positive effect ->
        #variables in effect, look values for variables in bindings and doprint 
        #replacemenet and add the effects to the state
        
        for effects in self.positiveEffects:
            for i in range(len(effects)):
                cur = effects[i].strip()
                if(cur.find("?") != -1):
                    if(cur in self.bindings.get_bindings().keys()):
                        effects[i] = self.bindings.get_bindings()[cur]
                    else:
                        return False
            state.add(effects)
            
        
        #same for negative as above
        #at the end remove rather than add the effects from the state
        #return the state 
        
        for effects in self.negativeEffects:
            for i in range(len(effects)):
                cur = effects[i].strip()
                if(cur.find("?") != -1):
                    if(cur in self.bindings.get_bindings().keys()):
                        effects[i] = self.bindings.get_bindings()[cur]
                    else:
                        return False
            state.remove(effects)
            
        return state
            
        #print("Preconditions: ", self.preconditions)
        #print("Positive Effects: ", self.positiveEffects)
        #print("Negative Effects: ", self.negativeEffects)     
        #sys.exit(0)