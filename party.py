import character

class WorldObject():
    """WorldObject Class"""

    def __init__(self):
        """#WorldObject
        Defines any object that is going to exist in the overworld, including parties, places and other stuff.

        Returns:
            _type_: _description_
        """
        self.character:str[1] = 'O'
        self.x:int = 0
        self.y:int = 0
        
    def printSelf(self):
        return self.character

    def getCoordinates(self)->list[int]:
        return (self.x,self.y)

    def updateCoordinates(self,x:int,y:int):
        self.x = x
        self.y = y

class Party(WorldObject):
    """Party Class"""

    def __init__(self):
        """#Party class
        contains details on the party, including its creatures, and its AI decision making.
        
        printSelf() - Returns an ascii character to represent the party

        
        """

        self.character:str[1] = 'P'
        self.members:list[character.Character] = []
        
    def getPartyMembers(self)->list[character.Character]:
        """Gets list of party members"""
        return self.members
    
    def addPartymember(self,newmember:character.Character):
        """Add a new character to party"""
        self.members.append(newmember)

if __name__ == "__main__":

    p = Party()
    print(p.printSelf())