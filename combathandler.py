import party
import character
class CombatHandler():
    """CombatHandler Class"""

    def __init__(self,*parties:party.Party):
        """# CombatHandler class
            One combathandler is created for each fight, and takes parties.
            Creates a 2d grid and deploys both sides' soldiers on either side, then they can fight it out.
        """

        # Create grid
        self.combat_grid:list[list[list[character.Character]]] = []
        for _ in range(20):
            self.combat_grid.append([])
            for __ in range(10):
                self.combat_grid[_].append([])
        

        # For party, deploy them on one side of the battlefield, currently allows side 1 on the left and side 2 on the right
        side = 0 
        for party in parties:
            characters = party.getPartyMembers()
            increment = 0 
            for _character in characters:
                if side == 0:
                    _character.setCoords(increment//9,increment%9)
                    self.combat_grid[increment//9][increment%9].append(_character)
                elif side == 1:
                    _character.setCoords(19-increment//9,increment%9)
                    self.combat_grid[19-increment//9][increment%9].append(_character)
                increment+=1
            side+=1

    def printSelf(self)->str:
        txt = ""
        for j in range(10):
            for i in range(20):
                if len(self.combat_grid[i][j]) == 0:
                    txt+="."
                elif len(self.combat_grid[i][j]) == 1:
                    txt+=self.combat_grid[i][j][0].printSelf()
                else: # If more than 1 character:
                    txt+="+"
            txt+="\n"
        return txt
    

if __name__ == "__main__":
    p1 = party.Party()
    p1.addPartymember(character.Character())
    p1.addPartymember(character.Character())
    p1.addPartymember(character.Character())
    p2 = party.Party()
    p2.addPartymember(character.Character())
    p2.addPartymember(character.Character())
    p2.addPartymember(character.Character())

    ch = CombatHandler(p1,p2)
    print(ch.printSelf())