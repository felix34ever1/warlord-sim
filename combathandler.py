import party
import character
import math
import time
from random import randint
class CombatHandler():
    """CombatHandler Class"""

    def __init__(self,*parties:party.Party):
        """# CombatHandler class
            One combathandler is created for each fight, and takes parties.
            Creates a 2d grid and deploys both sides' soldiers on either side, then they can fight it out.
        
        processTurn() - Let both sides fight, calculating initiative and then let each unit in order perform its turn.
        printSelf() - Return a string printing the current display of the battle.

        """

        self.parties = parties

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

    def processTurn(self):
        """Handles the turn of units, calculating initative, then letting units do their turn.
        """
        ## Initiative calculation
        # Get all units in a list
        all_units:list[character.Character] = []
        for _party in self.parties:
            units = _party.getPartyMembers()
            for unit in units:
                all_units.append(unit)
        
        # Get a new list which puts the units in a random order (NOTE current version of initiative, later will be a priority queue )
        ordered_units:list[character.Character] = []
        while len(all_units) != 0:
            ordered_units.append(all_units.pop(randint(0,len(all_units)-1)))

        # Go through units and let each unit do a turn.
        while len(ordered_units)!=0:
            cur_unit = ordered_units.pop(0)
            enemy_units:list[character.Character] = []
            # Figure out all enemy units by going through party and getting all hostile parties in one list
            for _party in self.parties:
                if cur_unit in _party.getPartyMembers():
                    pass
                else:
                    enemy_units.extend(_party.getPartyMembers())

            shortest_distance = 9999
            # Use manhattan distance heuristic to pick closest unit to path to.
            closest_enemy = None
            for enemy_unit in enemy_units:
                c_x,c_y = cur_unit.getCoords()
                e_x,e_y = enemy_unit.getCoords()
                m_distance = abs(e_x-c_x)+abs(e_y-c_y)
                if m_distance<shortest_distance:
                    shortest_distance = m_distance
                    closest_enemy = enemy_unit
            
            # If enemies left, move toward them by pathfinding or fight if next to eachother.
            if closest_enemy!= None:
                if shortest_distance == 1:
                    # Combat
                    pass
                else:
                    # Pathfind
                    pathfind_nodes = self.pathfind(c_x,c_y,e_x,e_y,list())
                    next_node = pathfind_nodes[0]
                    self.moveCharacterTo(cur_unit,next_node)

    def moveCharacterTo(self, char:character.Character, targetcoords:tuple[int]):
        """Attempts to move character to target coords, if they are already occupied, it will instead fail, leaving the character at their original position.

        Args:
            char (character.Character): Character attempting to move
            targetcoords (tuple[int]): coordinates the character is attempting to move to
        """

        if len(self.combat_grid[targetcoords[0]][targetcoords[1]]) == 0:
            # Move to new area
            chcoords = char.getCoords()
            self.combat_grid[chcoords[0]][chcoords[1]].clear()
            char.setCoords(targetcoords[0],targetcoords[1])
            self.combat_grid[targetcoords[0]][targetcoords[1]].append(char)
        else:
            # No movement
            pass

    def pathfind(self,start_x:int,start_y:int,end_x:int,end_y:int,visited_coords:list[tuple[int]] = list())->list[tuple[int]]:
        """Pathfinds from start position to end position recursively using euclidean distance heuristic, returning a completed path of points.

        Args:
            start_x (_type_): start x coord
            start_y (_type_): start y coord
            end_x (_type_): target x coord
            end_y (_type_): target y coord
            visited_coords: Set of points that have already been visited.

        Returns:
            list[tuple[int]]: Returns the path to be taken to get there.
        """
        # First add the start area as visited
        visited_coords.append((start_x,start_y))

        # Check if one of the moves would reach the target, in which case return as that's the target reached but the two characters cant stand atop eachother.
        # Check manhattan:
        if abs(start_x-end_x)+abs(start_y-end_y) == 1:
            return(list())


        # Get all possible movement tiles around the start position, adding them to a list, making sure they haven't already been visited.
        possible_moves = []
        if start_x>0:
            if len(self.combat_grid[start_x-1][start_y])==0 and not (start_x-1,start_y) in visited_coords:
                possible_moves.append((start_x-1,start_y))
        if start_x<len(self.combat_grid)-1:
            if len(self.combat_grid[start_x+1][start_y])==0 and not (start_x+1,start_y) in visited_coords:
                possible_moves.append((start_x+1,start_y))
        if start_y>0:
            if len(self.combat_grid[start_x][start_y-1])==0 and not (start_x,start_y-1) in visited_coords:
                possible_moves.append((start_x,start_y-1))
        if start_y<len(self.combat_grid[0])-1:
            if len(self.combat_grid[start_x][start_y+1])==0 and not (start_x,start_y+1) in visited_coords:
                possible_moves.append((start_x,start_y+1))
        
        # Calculate best of the moves by euclidean distance heuristic
        smallest_distance = 99999
        best_move = None
        for move in possible_moves:
            euc_distance = math.sqrt((move[0]-end_x)**2+(move[1]-end_y)**2)
            if euc_distance<smallest_distance:
                smallest_distance = euc_distance
                best_move = move

        # If no more path found to enemy, return nothing
        if best_move == None:
            return(list())
        # Otherwise, start a new list, append the best move, then extend with a recursive call to algo and return.
        else:
            nextpath = self.pathfind(best_move[0],best_move[1],end_x,end_y,visited_coords)
            if nextpath == None:
                return([best_move])
            elif len(nextpath) == 0:
                return([best_move])
            else:
                path = [best_move]
                while len(nextpath) != 0:
                    path.append(nextpath.pop(0))
                return path
    def printSelf(self)->str:
        """Returns the string displaying an image of the battlefield. 
        """
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
    p1coords = p1.getPartyMembers()[0].getCoords()
    p2coords = p2.getPartyMembers()[0].getCoords()

    for _ in range (10):
        print(ch.processTurn())
        print(ch.printSelf())
        time.sleep(0.5)