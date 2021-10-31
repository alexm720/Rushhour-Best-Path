

import copy
import math

############## Dictionary Creation ############

# This functions main purpose is to take in a string that contains
# the starting State and creates a dictionary which contains the car
# name as a key and either H or V as a value which indicates if the car
# is placed vertically or horizonatally.
def AutoCount(StateSpace):
    CarDict = {} 
    for line in range(0,len(StateSpace)): # For loop goes through each list inside the main list
        for char in StateSpace[line]:     # and goes character by character.
            if(char == '-'):              # If the character is empty, nothing happens
                continue
            else:                         # If the character is not empty check if the character is already in
                temp = char               # the dictionary
                if temp not in CarDict:
                    if StateSpace[line].count(temp) >= 2:    # If the character is not in the dictionary, check if the length of that characters occurance
                        CarDict[temp] = "H"                  # is greater than or equal to two, this would indicate the car is horizontal if true
                    elif StateSpace[line].count(temp) == 1:  # If the character occurance length is one, then this indcates that the car is vertical
                        CarDict[temp] = "V"
    return CarDict
                                   



############ PUZZLE LOGIC #####################

# This functions main purpose is to preform the logic of the puzzle. Through
# difference sorts of manipulation we are able to perform each set of moves through
# the use of this single function. In simple terms, this function shifts a given car
# to the right once. This function takes the statespace that needs to shift right and the car type.
# The fucntion retures the shiftted list of strings. 
def RightHorizontalMove(StateSpace,car):
    RowLength = len(StateSpace[0])-1                # Get the index for the last character of the first string.  
    for line in range(0, len(StateSpace)):          # This for loop finds the index of the first occurance of the car
        if car in StateSpace[line]:         
            row = line
            col = StateSpace[line].index(car)
            break     
    if (StateSpace[row].count(car) == 2):                               #If the occurance length of the car is equal to two, then the car is a car and its is size two
        if (col+1 == RowLength or list(StateSpace[row])[col+2] != '-'):
            return[]
        else:                                                           # Here, given the index and row of the car, we can save that string to another variable
            oldState = StateSpace[row]                                 
            newState = list(StateSpace[row])
            newState[col] = '-'
            newState[col+2] = car
            newState = unlist(newState)     
            return GenterateNewStates(StateSpace,newState,row,col)      # We now call GenerateNewStates to perform the shift on the car. 
        
    elif (StateSpace[row].count(car) == 3):                             # If the occruacen length of the car is equal to two, then that car is actually a truckt and 
        if (col+2 == RowLength or list(StateSpace[row])[col+3] != '-'): # it is of size 3
            return[]
        else:                                                           # Perform same logic as before, but with Trucks.
            oldState = StateSpace[row]
            newState = list(StateSpace[row])
            newState[col] = '-'
            newState[col+3] = car
            newState = unlist(newState)
            return GenterateNewStates(StateSpace,newState,row,col)      # Call GenerateNewStates and perform the right shift on the trucxk

        

def LeftHorizontalMove(StateSpace,car):
    return reverseEach(RightHorizontalMove(reverseEach(StateSpace),car)) # A left move on any given car can be simulated by reversing the strings in out given statespace


def UpVerticalMove(StateSpace,car):
    return transpose(LeftHorizontalMove(transpose(StateSpace),car)) # An Up move on any given car can be simulated by transposing the strings in our given statespace and then
                                                                    # perform a left shift on a tranposed statespace
                                                                    
def DownVerticalMove(StateSpace,car):                               # A down move can be simulated by transpoing the strings and performing a Right shift on a transposed Statespace. 
    return transpose(RightHorizontalMove(transpose(StateSpace),car))


#################################################################

#################HELPER FUNCTIONS################################


def unlist(lst):                                     #Unlists a list
    string = ""
    for char in lst:
        string += char
    return string

def transpose(Matrix):                                  # Treats Statespace as a matrix, this function transposes that matrix
    result = [list(char) for char in zip(*Matrix)]
    for i in range(0,len(result)):
        result[i] = unlist(result[i])
    return result

def reverseEach(listOfLists):                           # Reverse each string in the list
    result = []
    for lst in listOfLists:
        result.append(reverse(lst))
    return result    

def reverse(st):                                        # Reverse a string
    return st[::-1]


def PrintPath(Start):                                   # Given a list of lists print out each item(list) if
    Start = Start[::-1]                                 # it is true that the item is a list, if not, skip that item.
    moves = 0                                           # This is done because a lot of items in the list could be
    for elem in Start:                                  #integers but we dont need those here
        if isinstance(elem,list):
            if not elem:
                pass
            else:
                for lst in elem:
                    print(lst)
                moves += 1
                print("**********")
    return moves

def findX(start):                                       # Finds X, and returns the column/row of where x is.
    for i in range(0, len(start)):
        if 'X' in start[i]:
            row = i
            col = start[i].index('X')
            break
    return row,col



#######################################################



############### HEURISTIC FUNCTIONS (h(n)) ##############

# This is the first of the two heuristic functions. This function's main purpose
# is to find the column and row of X, once found we check the row and count how
# many occurses of difference cars are blocking X in X's given row.

def blocking(start):
    row,col = findX(start)                              # Find the location of X                          
    unique = []
    blocking = 0
    xRow = list(start[row])
    i = 0
    for char in xRow:                                   # Use this for loop to count the number of cars
        if char == 'X' and i == 0:                    # in front of X that are unique and are not empty.
            i += 1                                  
        elif (char not in unique and char != 'X'
        and char != '-' and i != 0):
            unique.append(char)
            blocking += 1
    if not unique:                                      # If unique is empty that means there are not cars blocking
        return blocking                                 # and we may return 0
    else:
        blocking += 1                                   # Else add one to the final count, and return the number of cars blocking x + 1.
        return blocking

# This is the student-made heuristic, where instead of counting all the cars in front of x
# we rather count all the cars blocking x, then we count all the cars that are blocking those
# cars which are blocking X
def MultiBlocking(start,carDict):
    row,col = findX(start)
    unique = []
    blocking = 0
    xRow = list(start[row])
    i = 0
    for char in xRow:                           
        if char == 'X' and i == 0:
            i += 1
        elif (char not in unique and                # Logic follows the same as def blocking() for the first
        char != 'X' and char != '-' and i != 0):    # portion of this function
            unique.append(char)
            blocking += 1
    if not unique:
        return blocking
    else:                                           # Here we make use of our dictionarty containing all cars.
        for car in unique:                          # We check each of the cars according to whether they are horizontal
            if carDict[car] == 'V':                 # or vertial. If the car is horizontal we check if a right move is possible
                if not UpVerticalMove(start, car):  # or a left move. For each possible move we add one. This is because if a move is 
                    blocking += 1                   # is possibke, then there are no cars blocking that given car, in that direction
                else:
                    pass
                if not DownVerticalMove(start, car):
                    blocking += 1
                else:
                    pass
            if carDict[car] == 'H':                 # We follow the same logic, but now we do it for those cars that are Horizontal.
                if not LeftHorizontalMove(start, car):
                    blocking += 1
                else:
                    pass
                if not RightHorizontalMove(start, car):
                    blocking += 1
                else:
                    pass
        return blocking                             # Return our new heuristic value

####################################################



#################STATE GENERATION###################


# This function takes a current state, the row with the new state and the row/col of that
# string to be shifted. The current state is then replaced by the new state that was generated
# and we return our new shifted state as the result
def GenterateNewStates(CurrState,NewState,Row,Col):
    result = []
    for i in range(0, len(CurrState)):              
        if i == Row:
            result.append(NewState)
        else:
            result.append(CurrState[i])
    return result


# This function's main duty is to generate all possible
# states, given a current state)
def AllPossibleStates(autoDict,lst,checklist,heuristic):
    i = 0
    newlist = []
    for car in autoDict:
        if 'H' in autoDict[car]:                                    # This for loop goes through each car in the dictionary and checks
            if (not LeftHorizontalMove(lst[1],car) or               # if that car is horizontal or vertival. Then the approriate shifts
                LeftHorizontalMove(lst[1],car) in checklist):       # are generated. If the shift is not possible or its already 
                pass                                                # been seen then no new shift is made.
            else:
                checklist.append(LeftHorizontalMove(lst[1],car))
                newlist.append([LeftHorizontalMove(lst[1],car)]+lst)
                newlist[i].insert(0,1+lst[0])                    
                if heuristic == 0 :                                                         # Here we check which heuristic is chosen, based on that the 
                    newlist[i].insert(0,(blocking(newlist[i][1])+newlist[i][0]))            # fn will vary.
                    i += 1
                elif heuristic == 1:
                    newlist[i].insert(0,(MultiBlocking(newlist[i][1],autoDict)+newlist[i][0]))
                    i += 1             
            if (not RightHorizontalMove(lst[1],car) or
                    RightHorizontalMove(lst[1],car) in checklist):
                pass
            else:
                checklist.append(RightHorizontalMove(lst[1],car))                           # We append the move into a checklist which contains moves already made
                newlist.append([RightHorizontalMove(lst[1],car)]+lst)                       # Here we append the now generated list along its path
                newlist[i].insert(0,1+lst[0])                                               # Here we have the height which is the actual cost of getting to this node
                if heuristic == 0 :
                    newlist[i].insert(0,(blocking(newlist[i][1])+newlist[i][0]))
                    i += 1
                elif heuristic == 1:
                    newlist[i].insert(0,(MultiBlocking(newlist[i][1],autoDict)+newlist[i][0]))
                    i += 1    
        elif 'V' in autoDict[car]:                                                       # All of the same logic performed here is the same as above but for vertical  
            if (not UpVerticalMove(lst[1],car) or                                        # cars
                UpVerticalMove(lst[1],car) in checklist):
                pass
            else:
                checklist.append(UpVerticalMove(lst[1],car))
                newlist.append([UpVerticalMove(lst[1],car)]+lst)
                newlist[i].insert(0,1+lst[0])
                if heuristic == 0 :
                    newlist[i].insert(0,(blocking(newlist[i][1])+newlist[i][0]))
                    i += 1
                elif heuristic == 1:
                    newlist[i].insert(0,(MultiBlocking(newlist[i][1],autoDict)+newlist[i][0]))
                    i += 1                  
            if (not DownVerticalMove(lst[1],car) or
                DownVerticalMove(lst[1],car) in checklist):
                    pass
            else:
                checklist.append(DownVerticalMove(lst[1],car))
                newlist.append([DownVerticalMove(lst[1],car)]+lst)
                newlist[i].insert(0,1+lst[0])
                if heuristic == 0 :
                    newlist[i].insert(0,(blocking(newlist[i][1])+newlist[i][0]))
                    i += 1
                elif heuristic == 1:
                    newlist[i].insert(0,(MultiBlocking(newlist[i][1],autoDict)+newlist[i][0]))
                    i += 1    
    
    return newlist

# Once a solution has been found, this function shift
# X to its approriate spot and the states are printed.
def MoveX(lst):                                                         
    size = len(lst[2][0])- 1
    row, col = findX(lst[2])
    path = []
    if col+1 != size:
        temp = RightHorizontalMove(lst[2],'X')
        path.insert(0,temp)
        col += 1
        while col != size:
            temp = RightHorizontalMove(path[0],'X')
            path.insert(0,temp)
            col += 1
    moves = PrintPath(path)
    return moves




############# A* Algorithm ##############################


# This function serves are the search function that makes use of the A*
# Algorithm. If the heuristic is 0, then def blockig is use
# otherwise, def MultiBlocking is used
def StateSearchA(unsearched,path,autoDict,heuristic):
    unsearched[0].insert(0,0)                               #insert the height of tree            
    unsearched[0].insert(0,(blocking(unsearched[0][1])))    # insert the amount of cars blocking x 
    for lst in unsearched:                                  # This portion checks to see of the given state
        if lst[0] == lst[1]:                                # is already a winning move, if it is then complete function.
                moves = PrintPath(lst)+MoveX(lst) - 1
                print("Total Moves: ", moves)
                print("Total States Explored: ", 1)
                return        
    checklist = []
    buff = True
    explore = 0
    if heuristic == 0:                                      # If heuristic is 0, this part of the function runs
        while buff:       
            ind = 0
            i = 0
            SmallFn = unsearched[0][0]
            for lst in unsearched:                          # This for loop serves as finding the index of the smallest f(n)
                if lst[0] < SmallFn:                        # in our tree, if it is not found, then the most far left node is used
                    SmallFn = lst[0]
                    i = ind
                ind += 1
            unsearched[i].pop(0)                            # Remove the f(n) value
            TempList =  [elem[:] for elem in unsearched]    # create a copy of the chosen statespace to expand.
            unsearched.remove(unsearched[i])                # Remove the list which is about to get expanded
            unsearched = unsearched + AllPossibleStates(autoDict,TempList[i],checklist,0)  # append all new possible states with value chosen to the rest of the node
            explore += 1                                                                   # that were unexplored
            for lst in unsearched:                          # Checks each list to check if the entire path to the end goal is clear
                if lst[0] == lst[1]:                        # If it is clear, print path and print out the moves/exploration costs.
                    moves = PrintPath(lst)+MoveX(lst) - 1
                    print("Total Moves: ", moves)
                    print("Total States Explored: ",explore)
                    buff = False
                    break
                
    elif heuristic == 1:                                    # Follows same logic as before only a few minor changes due to different heuristic
        while buff:       
            ind = 0
            i = 0
            SmallFn = unsearched[0][0]
            for lst in unsearched:
                if lst[0] < SmallFn:                        # Pick the smallest fn
                    SmallFn = lst[0]
                    i = ind
                ind += 1
            unsearched[i].pop(0)
            TempList =  [elem[:] for elem in unsearched]
            unsearched.remove(unsearched[i])
            unsearched = unsearched + AllPossibleStates(autoDict,TempList[i],checklist,1)
            explore += 1
            for lst in unsearched:
                if blocking(lst[2]) == 0:                   # Since our heuristic is different we take advantag of the blocking function to see
                    moves = PrintPath(lst)+MoveX(lst) - 1   # if our goal state has been found, if it has print necessary information.
                    print("Total Moves: ", moves)
                    print("Total States Explored: ",explore)
                    buff = False
                    break

  

# Function to be called, takes starting point and 0 for blocking function, or 1 for the multiblocking function
def rushhour(h,start):                                      
    row,col = findX(start)
    autoDict = AutoCount(start)
    StateSearchA([[start]],[],autoDict,h)




    

### -------This is for testing purposes only -------

# HOW TO RUN:
# - rushhour(STARTING STATE, HEURISTIC)
#     ~ STARTING STATE: a list of strings
#     ~ HEURISTIC: 1 for student-made, 0 for blocking heurstic
    
def main():
    State = ["--AABB","--CDEF","XXCDEF","--GGHH","------","------"]
    State1 = ["--B---","--B---","XXB---","---AA-","------","------"]
    State2 = ["-ABBO-","-ACDO-","XXCDO-","PJFGG-","PJFH--","PIIH--"]
    State3 = ["---B--","---B--","-XXB--","---AA-","------","------"]
    state4 = ["------","--BC--","XXBC--","---C--","------","------"]
    state5 = ["--B-C-","--B-C-","XXB-C-","--AA--","DD----","EE----"]
    
    rushhour(1,State)
    rushhour(0,State)

    rushhour(1,State1)
    rushhour(0,State1)

    rushhour(1,State2)
    rushhour(0,State2)

    
    rushhour(1,State3)
    rushhour(0,State3)

    
    rushhour(1,state4)
    rushhour(0,state4)

    rushhour(1,state5)
    rushhour(0,state5)

if __name__ == '__main__': main()




