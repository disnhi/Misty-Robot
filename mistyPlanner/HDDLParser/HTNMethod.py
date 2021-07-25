"""
Creater: @Saad Mahboob
"""
"""
    HTNMethod class contains the following fields:
    1) name
    2) parameters -> arguments that have been passed into the method 
    3) method_code -> lines of codes containing the whole method
    4) task -> for which the method has been assigned
    5) preconditions -> these are probably strings(for now) which need to be true for the method to work
    6) subtasks -> these are the sequence of actions suggested by the method 
                -> (can contain more operator objects) (store in list)
"""

import re, sys
from HDDLParser import HTNParsingLibrary, HTNMethod, HTNParameter, HTNOperator, HTNBinder

class HTNMethod:

    def __init__(self, idx, lines):
        self.lines = lines
        self.index = idx
        self.method_name = lines[self.index][8:].strip()  #get the method name from the first line of code passed in
        self.task = None 
        self.fullTask = None

        self.parameters = [] 
        self.method_code = [] 
        self.parenthesis = [] 
        self.preconditions = [] 
        self.subtasks = [[]] 
        self.bindings = None

        #self.get_method_name()
        self.extract_code()
        self.extract_task() 
        self.extract_parameters()
        self.extract_preconditions()
        self.extract_subtasks() #this might be the one to edit for parsing string

    def get_name(self):
        return self.method_name
    
    def get_task_without_perameters(self):
        return self.task
    
    def get_task_with_perameters(self):
        #print("FULL TASK? ", self.fullTask)
        return self.fullTask
    
    def get_method_parameters(self):
        return self.parameters

    def extract_code(self):
        self.parenthesis.append(HTNParsingLibrary.OPENING_PARENTHESIS)
        #we have already extracted name from 1st line, so now shift to next before looping
        self.index = self.index + 1 
        while(self.index < len(self.lines) and len(self.parenthesis) != 0):
            cur_line = self.lines[self.index]
            self.method_code.append(cur_line)
            self.index += 1

            #this keeps track of opening and closing parenthesis to extract the method code
            for char in cur_line:
                if HTNParsingLibrary.OPENING_PARENTHESIS in char:
                    self.parenthesis.append(HTNParsingLibrary.OPENING_PARENTHESIS)
                if HTNParsingLibrary.CLOSING_PARENTHESIS in char:
                    self.parenthesis.pop()
                    
        #print(self.method_code)
    
    def extract_task(self): #where the bug possible is
        for line in self.method_code:
            if HTNParsingLibrary.TASK_START in line:
                idx_start = line.find(HTNParsingLibrary.OPENING_PARENTHESIS)+1
                idx_end = line.find(HTNParsingLibrary.CLOSING_PARENTHESIS)
                line = line[idx_start:idx_end]

                self.fullTask = line

                #print("\nFULLTASK? : ", self.fullTask)

                 #my code
                #if '?' in line:
                #    print("\n\nIS THIS WORKINGGGGGGGGGGGGGGGGGG???\n\n")
                #    temp = line.find('?')
                #    line = line[0:temp]
                #    print("LINE: ",line)

                #my code

                #Ensures that the last index doesn't get cut off
                if line.find(HTNParsingLibrary.CLOSING_PARENTHESIS) >= 0:
                    if '?' in line: 
                        temp = line.find('?')
                    idx_q_start = line.find(HTNParsingLibrary.PARAMETER_VALUE_START)
                    self.task = line[:idx_q_start].strip()
                else:
                    #my code
                    if '?' in line: 
                        temp = line.find('?')
                        #self.task = line[0:temp]
                        #print("line issssssssssssssssssssssssssssssssssssssssssssssss: ", line)
                        #print("line 0:temp is ... ", line[0:temp])
                        temp = line[0:temp].strip()
                        self.task = temp
                        
                    #my code
                    else:
                     self.task = line.strip()

                break

        #don't think this code is doing the binding for the parameter.
        #try something like if there's a '?' then call do binding

        #print("The Task: ", self.task)
        #print("The full task: ",self.fullTask)
 
    def extract_parameters(self):
        for line in self.method_code:
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
                    par_type = parameter_line[type_start:type_end]

                    #this is to check if there are multiple parameter values of same type
                    multiple_par = value.count("?")
                    
                    #if there are multiple values of same type, we create multiple parameter objects
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
        
        #the following helps us get the starting line from the whole method, where preconditions start
        line = ""
        idx1  = 0
        for idx in range(len(self.method_code)):
            line = self.method_code[idx]
            if HTNParsingLibrary.PRECONDITIONS_START in line:
                line = self.method_code[idx+1]
                idx1 = idx+1
                break
        
        #this stack is to match parenthesis of the precondition code 
        stack = []
        #starating parenthesis of the precondition, we skipped the first line, so we add it here
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
                line = self.method_code[idx1]

        #this is to extract preconditions out of the lines and push them into final list of list
        for precondition in precondition_code:
            precondition = precondition.strip()
            
            
            #remove the parenthesis from the precondition
            condition = precondition.replace("(","").replace(")","")
            split_precondition = condition.split(" ")
                        
            list_condition = []
            
            #in this loop add all the values of a precondition which were split up before on basis of space into this list
            for i in range(0,len(split_precondition)):
                list_condition.append(split_precondition[i])
            self.preconditions.append(list_condition)

    def extract_subtasks(self):
        self.subtasks = [[]]
        #the following helps us get the starting line from the whole method, where subtasks start
        line = ""
        idx1  = 0

        #looping through method section and searching for subtask
        for idx in range(len(self.method_code)):
            line = self.method_code[idx]
            if HTNParsingLibrary.SUBTASKS_START in line:
                line = self.method_code[idx+1]
                idx1 = idx+1
                break
        
        stack = []
        #subtasks are the last one, so we have to add 2 parenthesis, one which was 
        #from method start and other one for subtask or effects start as we skip that line
        stack.append(HTNParsingLibrary.OPENING_PARENTHESIS)
        stack.append(HTNParsingLibrary.OPENING_PARENTHESIS)
        subtask_code = []

        #this here is to match parenthesis of each line in task and stop when the subtask section is over 
        #this helps extract subtask or effect code into the list of lines
        while(len(stack) != 0):
            for char in line:
                if HTNParsingLibrary.OPENING_PARENTHESIS in char:
                    stack.append(HTNParsingLibrary.OPENING_PARENTHESIS)
                elif HTNParsingLibrary.CLOSING_PARENTHESIS in char:
                    stack.pop()
            
            subtask_code.append(line)
            if(len(stack) != 0):
                idx1 += 1
                line = self.method_code[idx1]
    
        #this is to extract task or action out of brackets and push into subtask list

        for sub in subtask_code:
            temp_subtask = []
            sub = sub.strip()
            idx_start = sub.find(HTNParsingLibrary.OPENING_PARENTHESIS)+1
            idx_end = sub.find(HTNParsingLibrary.CLOSING_PARENTHESIS)
            temp_subtask = sub[idx_start:idx_end].split() #can't just do the .split since we're using a string. so adjust to account for string argumments 

            start_tracker = 0
            end_tracker = 0
            count = 0
            temp_string = []
            text_string = '"'
            temp_list = []
            final_string = ""
            temp_word = ""

            #checks to see if there's a string argument
            for item in temp_subtask:

                if text_string not in item:
                    if count == 0:
                        temp_list.append(item)
                    else:
                        temp_word = item + " "
                        final_string += temp_word
                else:
                    if count == 0:
                        temp_word = item + " "
                        final_string += temp_word
                        count += 1
                    else: 
                        temp_word = item + " " 
                        final_string += temp_word
                        count = 0
                        stripped_string = final_string.replace('"',"") #gets rid of the double quotation marks
                        temp_list.append(stripped_string)

            temp_subtask = temp_list

            self.subtasks.append(temp_subtask)

        if [] in self.subtasks:
            self.subtasks.remove([])


    def do_bindings(self, parameter_list):

        #create the binding object        
        bindings = HTNBinder.HTNBinder()

        
        #get the task and see what parameters are attached to it
        #those parameter values would passed in as argument here in parameter list
        task = self.get_task_with_perameters()
        idx_q_start = task.find(HTNParsingLibrary.PARAMETER_VALUE_START)
        pars = task[idx_q_start:].strip()
        pars = pars.split()
        
        
        #update the bindings based on the task prameters as key and their values from parameter_list
        for i in range(len(pars)):
            key = pars[i-1]
            if len(parameter_list) != 0:
                value = parameter_list[i-1] #what i did was change i to i-1
                bindings.update_bindings(key, value)
        
        
        #assign the binding object we created to this method
        self.bindings = bindings

        return self.bindings
    
    #when returning the subtaks list, update the parameters based on the bindings dictionary
    def get_subtasks(self, parameter_list):
        
        self.extract_subtasks()        
        bindings = self.bindings
        
        #loop through all the subtasks
        #if any parmeter from subtaks is in bindings, we update the value of that subtask's parameter
        for subtask in self.subtasks:
            for i in range(len(subtask)):
                  
                 #DEBUG
                 #print("Subtask of i: ", subtask[i])
                 #print("Bindings: ", bindings.get_bindings())

                 if subtask[i] in bindings.get_bindings(): 
                     subtask[i] = bindings.get_bindings()[subtask[i]]
        
        if [] in self.subtasks:
            self.subtasks.remove([])
        
        #if any value from the precondition, is not available in the bindings, we dont consider that method and return false
        return self.subtasks                     