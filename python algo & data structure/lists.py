#the file is to show how to work on lists

#creating a list 

class MyList:
    def __init__(self):
        self.names = []

    def addToList(self):
        #the lst will take inputs from user 
        userInPut = input("enter your inputs: ").split()
        self.names.append(userInPut)
        print("The new list is: \n {}".format(self.names))
    
    def removeFromList(self):
        removeWithIndex = int(input("Enter the position you want removed: "))
        removeWithItemName = input("Enter the name of the item you wish removed: ")

        self.names.pop(removeWithIndex)
        self.names.remove(removeWithItemName)

if __name__ == "__main__":
    myList = MyList()
    myList.addToList()
    myList.removeFromList()