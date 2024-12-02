import party

class World():
    """ World Class"""

    def __init__(self,size:int):
        """# World Class
            Holds a grid that stores entities in the world. It does not manage any of the entities, it only holds their location.
            
            world_grid - Holds party.WorldObjects, 2d list of defined size.

            addObject() - Adds a party.WorldObject to a list in world_grid.

            removeObject() - Removes a party.WorldObject from a list in world_grid.

            getObjects() - returns all party.WorldObjects in a given coordinate of world_grid.

            printWorld() - returns a string displaying the world.

        """

        self.world_grid:list[list[list[party.WorldObject]]] = []
        for x in range(size):
            self.world_grid.append([])
            for y in range(size):
                self.world_grid[x].append([])

        
    def addObject(self,object:party.WorldObject,x:int,y:int):
        """Adds a party.WorldObject to a list in world_grid at location x,y"""
        self.world_grid[x][y].append(object)
    
    def removeObject(self,object:party.WorldObject,x:int,y:int)->bool:
        """Removes a WorldObject in a list in world_grid at location x,y, returns True/False if succeeded or object already not there"""
        try:
            self.world_grid[x][y].remove(object)
            return True
        except ValueError:
            return False
    
    def getObjects(self,x:int,y:int)->list[party.WorldObject]:
        """Returns a list with WorldObjects at coordinates x, y"""
        return self.world_grid[x][y]
    
    def printWorld(self)->str:
        """Returns a string representing the world"""
        string:str = ""
        for i in range(len(self.world_grid)):
            for j in range(len(self.world_grid[0])):
                areasize = len(self.world_grid[i][j])
                if areasize == 0:
                    string+="."
                elif areasize == 1:
                    string+=self.world_grid[i][j][0].printSelf()
                else:
                    string+="+"
            string+="\n"
        return string


if __name__ == "__main__":
    w = World(4)
    w.addObject(party.Party(),0,1)
    w.addObject(party.WorldObject(),2,2)
    w.addObject(party.Party(),3,1)
    w.addObject(party.Party(),3,1)
    print(w.printWorld())