from random import randint
import time
from party import Party
from world import World

class Controller():
    """Controller Class"""

    def __init__(self,size:int):
        """# Controller Class
            Handles the game, being able to manage the world and performing the main game loop on its own.
            ## Parameters
            size:int - Takes in size of the world and generates a world of that size.
            world:World - Holds the world object.
            parties:List[Party] - Holds all the parties on the map, used to update them and interact w them.

            ## Methods
            generateWorld(timepassed) - Generates all the content on the world. 
            printWorld() - Returns the a string of the world to print.
            advanceWorldTime() - Moves the world time forward by 1 tick.
        """
        self.size = size
        self.world = World(size)
        self.parties:list[Party] = [] # List containing all parties in the world.

    def generateWorld(self,timeincrements:int=0):
        """ Generates the world through several steps, iteratively, going through the history of the world one time increment at a time and outputs a log."""
        txtlog = ""
        # TODO Generate terrain 
        txtlog+="|Terrain Gen|\n"
        txtlog+="|Terrain Gen Complete|\n"
        # TODO Generate factions - Each faction starts as one settlement, which grows each time increment and may expand with another settlement.
        txtlog+="|Faction Gen|\n"
        txtlog+="|Faction Gen Complete|\n"        
        # TODO Generate History - Go through time to complete faction gen
        txtlog+="|Year 0|\n"
        txtlog+="|History Generated|\n"
        # Generate parties - At the end, generate neutral parties and set them loose to interact with the world. 
        txtlog+="|Party Gen|\n"

        # Generates up to 5 parties by choosing random location and checking if anything is there in the world.
        for _ in range(5):
            x = randint(0,self.size-1)
            y = randint(0,self.size-1)
            txtlog+=f"Attempting to place new party at ({x},{y})"
            objects = self.world.getObjects(x,y)
            # If the chosen coordinate has anything, placing the party fails, otherwise place party and add to parties list
            if len(objects) != 0:
                txtlog+="- Failed, object already there\n"
            else:
                newparty = Party()
                newparty.updateCoordinates(x,y)
                self.world.addObject(newparty,x,y)
                self.parties.append(newparty)
                txtlog+="- Succeeded\n"

        txtlog+="|Party Gen Complete|\n"

        date = time.time()
        with open(f"creationlogs\log{date}.txt","w") as logfile:
            logfile.write(txtlog)
            
    def advanceWorldTime(self):
        """Goes through each faction and party and allows for them to act. 
        TODO Currently moves party on its own, but in future should give the party pathfinding ability.
        """
        for party in self.parties:
            # Randomly pick a direction and move party there. 
            dcoords = [0,0]
            direction = randint(0,3)
            if direction == 0:
                dcoords = [1,0]
            elif direction == 1:
                dcoords = [0,1]
            elif direction == 2:
                dcoords = [-1,0]
            elif direction == 3:
                dcoords = [0,-1]
            pcoords = party.getCoordinates()
            targetcoords = [pcoords[0]+dcoords[0],pcoords[1]+dcoords[1]]
            if targetcoords[0] >= self.size or targetcoords[0] < 0 or targetcoords[1] >= self.size or targetcoords[1] < 0:
                continue # Skips movement as failed to move in that direction, edge of world
            else:
                self.world.addObject(party,targetcoords[0],targetcoords[1])
                self.world.removeObject(party,pcoords[0],pcoords[1])
                party.updateCoordinates(targetcoords[0],targetcoords[1])

            

    def printWorld(self):
        """Prints the world"""
        print(self.world.printWorld())


if __name__ == "__main__":
    c = Controller(30)
    c.generateWorld()
    c.printWorld()
    time.sleep(1)
    c.advanceWorldTime()
    c.printWorld()
    time.sleep(1)
    c.advanceWorldTime()
    c.printWorld()