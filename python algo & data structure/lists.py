#the file is to show how to work on lists

#creating a list 

class List:
    def __init__(self):
        self.names = []

    def addToList(self):
        #the lst will take inputs from user 
        userInPut = [input("enter your inputs: ").split()]
        self.names.append(userInPut)
        print("The new list is: \n {}".format(self.names))
    
    def removeFromList(self):
        removeWithIndex = int(input("enter the position you want removed: "))
        removeWithItemName = input("enter the name of the item you wish removed: ")