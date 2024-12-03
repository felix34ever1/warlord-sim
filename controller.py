from random import randint
import time
from party import Party
from character import Character
from world import World
from combathandler import CombatHandler
import curses
from curses import wrapper

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
        self.nextID = 1

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
                newparty.getcolorpairID()
                self.world.addObject(newparty,x,y)
                self.parties.append(newparty)
                # init colour pairing
                curses.init_pair(self.nextID,newparty.getColourPair()[0],newparty.getColourPair()[1])
                newparty.setcolorpairID(self.nextID)
                self.nextID+=1
                # Add soldiers to party
                num_units = randint(3,20)
                txtlog+=f", {num_units} soldiers."
                for soldiers in range(num_units):
                    newsoldier = Character()
                    newsoldier.setcolorpairID(newparty.getcolorpairID())
                    newparty.addPartymember(newsoldier)
                    

                txtlog+="- Succeeded\n"

        txtlog+="|Party Gen Complete|\n"

        date = time.time()
        with open(f"creationlogs\log{date}.txt","w") as logfile:
            logfile.write(txtlog)
            
    def advanceWorldTime(self,stdscr:curses.window):
        """Goes through each faction and party and allows for them to act. 
        TODO Currently moves party on its own, but in future should give the party pathfinding ability.
        """
        for party in self.parties:
            # Randomly pick a direction and move party there. 
#            dcoords = [0,0]
#            direction = randint(0,3)
#            if direction == 0:
#                dcoords = [1,0]
#            elif direction == 1:
#                dcoords = [0,1]
#            elif direction == 2:
#                dcoords = [-1,0]
#            elif direction == 3:
#                dcoords = [0,-1]
            
            # Check if party has path, if not generate one.
            pcoords = party.getCoordinates()
            if len(party.getPath()) == 0:
                # Pick a target 
                for _opp_party in self.parties:
                    if _opp_party != party:
                        break
                _opp_coords = _opp_party.getCoordinates()
                new_path = self.world.pathfindOnce(pcoords[0],pcoords[1],_opp_coords[0],_opp_coords[1],list())
                party.setPath(new_path)

            if len(party.getPath()) != 0:
                # Pathfind towards enemy
                targetcoords = party.getPath().pop(0)
                if targetcoords[0] >= self.size or targetcoords[0] < 0 or targetcoords[1] >= self.size or targetcoords[1] < 0:
                    continue # Skips movement as failed to move in that direction, edge of world
                else:
                    self.world.addObject(party,targetcoords[0],targetcoords[1])
                    self.world.removeObject(party,pcoords[0],pcoords[1])
                    party.updateCoordinates(targetcoords[0],targetcoords[1])
            else:
                # Shares a space with target faction, attack!
                if len(self.world.getObjects(pcoords[0],pcoords[1]))>1:
                    parties = self.world.getObjects(pcoords[0],pcoords[1])
                    combat = CombatHandler(parties[0],parties[1])
                    combat.doCombat()
                else:
                    # Only ONE party left
                    break

            if len(self.world.getObjects(party.getCoordinates()[0],party.getCoordinates()[1]))>1:
                # If shares a space with another party, HAVE A FIGHT!
                parties:list[Party] = self.world.getObjects(party.getCoordinates()[0],party.getCoordinates()[1])
                combat = CombatHandler(parties[0],parties[1])
                combat.doCombat(stdscr)
                for _party in parties:
                    if len(_party.getPartyMembers()) == 0:
                        self.parties.remove(_party)
                        self.world.removeObject(_party,_party.getCoordinates()[0],_party.getCoordinates()[1])


    def printWorld(self):
        """prints the world"""
        print(self.world.printWorld())

    def printWorld(self,stdscr:curses.window):
        """Passes stdscr to the world and lets it draw to the cmd"""
        self.world.printWorld(stdscr)


def main(stdscr:curses.window):
    curses.cbreak(True)
    c = Controller(10)
    c.generateWorld()
    stdscr.clear()
    c.printWorld(stdscr)
    stdscr.refresh()
    stdscr.getch()
    for i in range(12):
        stdscr.clear()
        c.advanceWorldTime(stdscr)
        c.printWorld(stdscr)
        time.sleep(0.5) 
        stdscr.refresh()
        if len(c.parties) == 0:
            break


    stdscr.clear()
    stdscr.addstr("SIMULATION OVER! X to quit")
    stdscr.refresh()
    char:str = str(stdscr.getch())
    curses.endwin()

    
if __name__ == "__main__":
    wrapper(main)