
from HDDLParser import HTNParsingLibrary,HTNMethod,HTNParameter,HTNOperator
# from HDDLParser import HTNMethod
# from HDDLParser import HTNParameter
# from HDDLParser import HTNOperator

class HTNBinder():
    
    def __init__(self):
        self.bindings = {}
        
    def update_bindings(self, key, value):
        self.bindings[key] = value
        return True
    
    def get_bindings(self):
        return self.bindings
    
    def addAnotherBinding(self,newBindings):
        for key in newBindings:
            self.update_bindings(key,newBindings[key])