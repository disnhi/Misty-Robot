from HDDLParser import HTNParsingLibrary
from HDDLParser import HTNMethod
from HDDLParser import HTNParameter
from HDDLParser import HTNOperator

class HTNParameter:

    def __init__(self, parType, parValue):
        self.parType = parType
        self.parValue = parValue

    def getValue(self):
        return self.parValue
    
    def getType(self):
        return self.parType
    
    def toString(self):
        return self.parType + " " + self.parValue