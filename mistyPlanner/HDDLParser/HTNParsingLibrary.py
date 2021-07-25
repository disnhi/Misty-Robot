'''
Creater: @Saad Mahboob
Date: 03/27/2021
'''

from HDDLParser import HTNParsingLibrary
from HDDLParser import HTNMethod
from HDDLParser import HTNParameter
from HDDLParser import HTNOperator


#this library hold the markers to identify the start of specifc methods, operators, tasks,and parameters used in parsing
METHOD_START = "(:method"
PARAMETERS_START = ":parameters"
TASK_START = ":task"
PRECONDITIONS_START = ":precondition"
SUBTASKS_START = ":ordered-subtasks"
OPERATORS_START = ":action"
OPERATORS_EFFECT_START = ":effect"

OPENING_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"

PARAMETER_VALUE_START = '?'
PARAMETER_VALUE_END = '-'
PARAMETER_TYPE_START = '-'
PARAMETER_TYPE_END1 = '?'
PARAMETER_TYPE_END2 = ')'