"""
PyShop is an adaptation of Pyhop 1.2.2.  The intent of PyShop is to
return to using declarative representations of domains.
@see https://bitbucket.org/dananau/pyhop
"""

from __future__ import print_function
import copy,sys,pprint
from HDDLParser import HTNParser, HTNParsingLibrary, HTNMethod, HTNOperator, HTNBinder


class State():
    """A state is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name
        self.bindings = None
        self.facts = []
        self.bindings = HTNBinder.HTNBinder()
    
    #set preconditions
    def setPrecondition(self, precondition):
        pre = precondition.split()
        self.bindings.update_bindings(pre[0],pre[1])
    
    """ 
    function ask (create the bindings out of the facts dictionary)
    ask: (tAt ?l)
        -> [?l / loc1]
    ask: (road loc1 ?l2) 
        -> [[?l2 / loc 2], [?l2 / loc3]]
    """
    def ask(self, precondition):
        binding = self.bindings.get_bindings()
        if(precondition in binding.keys()):
            return binding[precondition]        
        else:
            return False
    
    def add(self, mAssert):
        if mAssert not in self.facts:
            self.facts.append(mAssert)  
    
    def remove(self, mRetract):
        if mRetract in self.facts:
            self.facts.remove(mRetract)
    
    
    #three methods
    #   dictionary of facts (key = predicate(first item in list e.g tAt),
    #   value = list of lists, inner list -> actual values (l1)) 
    #   example dictionary {tAt: [[loc1]], pAt:[[loc2]], road:[[loc1, loc2], [loc1, loc3], [loc2, loc3]]}
    #   1) ask (create the bindings out of the facts dictionary)
    # Ask: (tAt ?l)
    # [?l / loc1]
    # return the first one u find 
    # #Binding object, dictionary, name of variable mapped to the value (never returns False)
    # ask: (road loc1 ?l2) -> [[?l2 / loc 2], [?l2 / loc3]]
    #   2)add (assert) 
    #   3)remove (retract)

class Goal():
    def __init__(self,name):
        self.__name__ = name

### print_state and print_goal are identical except for the name
def print_state(state,indent=4):
    if state != False:
        for (name,val) in vars(state).items():
            if name != '__name__':
                for _ in range(indent): 
                    sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else: 
        print('False')

def print_goal(goal,indent=4):
    if goal != False:
        for (name,val) in vars(goal).items():
            if name != '__name__':
                for _ in range(indent): 
                    sys.stdout.write(' ')
                sys.stdout.write(goal.__name__ + '.' + name)
                print(' =', val)
    else: 
        print('False')

class PyShop(object):

    def __init__(self,name):
        self.__name__ = name
        self.operators = {}
        self.methods = {}
        
    #each method has key as name of task and the value is the list of methods attached to that task
    #check to see if already has method so add that method into the list
    def declare_methods(self, filePath):
        methods = HTNParser.HTNParser(filePath).get_methods()
        for method in methods:
            method_list = []
            task = method.get_task_without_perameters()
            method_list.append(method)
            if task in self.methods:
                old_list = self.methods[task]
                old_list.extend(method_list)
                method_list = old_list
                
            self.methods[task] = method_list

    #each operator has a key as name of the operator and value is the operator object
    def declare_operators(self, filePath):
        parser = HTNParser.HTNParser(filePath)
        operators = parser.get_operators()
        for operator in operators:
            name = operator.get_name()
            self.operators[name] = operator

    def print_operators(self):
        print('OPERATORS:', ', '.join(self.operators))

    def print_methods(self):
        print('{:<20}{}'.format('TASK:','METHODS:'))
        for task in self.methods:
            print('{:<20}'.format(task) + ', '.join([f.get_name() for f in self.methods[task]]))


    def pyshop(self,state,tasks,verbose=0,maxdepth=100):
        result = self.seek_plan(state,tasks,[],[],verbose)
        return result

    def seek_plan(self,state,tasks,plan,depth,verbose=0,maxdepth=100):
        
        if verbose>1: 
            print('depth {} tasks {}'.format(len(depth),tasks))
        if len(depth) > maxdepth:
            print('WARNING: Depth limit reached, returning no plan')
            return None
        if tasks == []:
            if verbose>2: print('depth {} returns plan {}'.format(len(depth),plan))
            return plan
        
        # v = input("Enter something: ")
        # if(v == "n"):
        #     sys.exit(0)
                
        firstTask = tasks[0]
        taskName = firstTask[0]

        #DEBUG
        #print("TASK: ", tasks)
        #print("\nTASKNAME: ",taskName)
        #print("METHOD_KEYS: ", self.methods.keys(),"\n")

        count = 0

        if taskName in self.methods.keys():

            if verbose>2:
                print('depth {} method instance {}'.format(len(depth),firstTask))       
            relevant_methods = HTNParser.HTNParser.get_relevant_methods(self,taskName,self.methods, state, firstTask[1:])

            for method in relevant_methods:
                subtasks = method.get_subtasks(firstTask[1:])
                #DEBUG
                #print("Subtask inside for loop: ", subtasks)

                if verbose>2:
                    print('depth {} new tasks: {}'.format(len(depth),subtasks))
                if subtasks != False:
                    methodTrace = [method.get_name()] 
                    
                    for value in firstTask[1:]:
                        methodTrace.append(value)
                
                    solution = self.seek_plan(state,subtasks+tasks[1:],plan,[methodTrace,list(firstTask)]+depth,verbose)
                    count = 1
                                        
                    if solution != False:
                        return solution
        
        if taskName in self.operators:          
            if verbose>2: 
                print('depth {} action {}'.format(len(depth),firstTask))
            
            operator = self.operators[taskName]
            newstate = copy.deepcopy(state)
            newstate = operator.execute(newstate, firstTask[1:])
            
            if verbose>2:
                print('depth {} new state:'.format(len(depth)))
            if newstate:
                solution = self.seek_plan(newstate,tasks[1:],plan+[(firstTask,depth)],depth,verbose)
                if solution != False:
                    return solution

        if count == 1:
            return solution
        else:
            print("Sorry! No solution.")
            return

        if verbose>2:
            print('depth {} returns failure'.format(len(depth)))
        return False
