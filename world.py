import party
import math
import curses

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

            pathfind() - Finds a path between two areas.

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

    def printWorld(self,stdscr:curses.window):
        """Places a string on the curses window"""
        #string:str = ""
        for j in range(len(self.world_grid[0])):
            for i in range(len(self.world_grid)):
                areasize = len(self.world_grid[i][j])
                if areasize == 0:
                    stdscr.addch(".")
                elif areasize == 1:
                    stdscr.addch(self.world_grid[i][j][0].printSelf(),curses.color_pair(self.world_grid[i][j][0].colorpairID))
                else:
                    stdscr.addch("+")
            stdscr.move(j,0)

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

        # Check if has reached the target, in which case return as that's the target reached, this should get the party ontop of the other party.
        # Check manhattan:
        if abs(start_x-end_x)+abs(start_y-end_y) == 0:
            return(list())


        # Get all possible movement tiles around the start position, adding them to a list, making sure they haven't already been visited.
        possible_moves = []
        if start_x>0:
            if not (start_x-1,start_y) in visited_coords:
                possible_moves.append((start_x-1,start_y))
        if start_x<len(self.world_grid)-1:
            if not (start_x+1,start_y) in visited_coords:
                possible_moves.append((start_x+1,start_y))
        if start_y>0:
            if not (start_x,start_y-1) in visited_coords:
                possible_moves.append((start_x,start_y-1))
        if start_y<len(self.world_grid[0])-1:
            if not (start_x,start_y+1) in visited_coords:
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

    def pathfindOnce(self,start_x:int,start_y:int,end_x:int,end_y:int,visited_coords:list[tuple[int]] = list())->list[tuple[int]]:
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

        # Check if has reached the target, in which case return as that's the target reached, this should get the party ontop of the other party.
        # Check manhattan:
        if abs(start_x-end_x)+abs(start_y-end_y) == 0:
            return(list())


        # Get all possible movement tiles around the start position, adding them to a list, making sure they haven't already been visited.
        possible_moves = []
        if start_x>0:
            if not (start_x-1,start_y) in visited_coords:
                possible_moves.append((start_x-1,start_y))
        if start_x<len(self.world_grid)-1:
            if not (start_x+1,start_y) in visited_coords:
                possible_moves.append((start_x+1,start_y))
        if start_y>0:
            if not (start_x,start_y-1) in visited_coords:
                possible_moves.append((start_x,start_y-1))
        if start_y<len(self.world_grid[0])-1:
            if not (start_x,start_y+1) in visited_coords:
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
            return([best_move])

if __name__ == "__main__":
    w = World(4)
    w.addObject(party.Party(),0,1)
    w.addObject(party.WorldObject(),2,2)
    w.addObject(party.Party(),3,1)
    w.addObject(party.Party(),3,1)
    print(w.printWorld())