from random import randint

class Character():
    """Character Class"""

    def __init__(self):
        """# Character Class
            Holds data on character including 
            """
        
        self.x:int = 0
        self.y:int = 0
        self.name:str = "Character"
        self.hp:int = 10
        self.resistance:int = 1
        self.strength = 5
        self.dexterity = 5
        self.weapons:list = []
        self.displaychar:str = "C"
        
    def getCoords(self)->list[int]:
        return [self.x,self.y]

    def setCoords(self,x:int,y:int):
        self.x = x
        self.y = y
        
    def meleeAttack(self)->int:
        """Returns a number to hit in melee"""
        tohit = randint(1,6) + self.dexterity
        return tohit

    def rangedAttack(self,distance:int)->int:
        """Returns a number to hit in ranged"""
        tohit = randint(1,6) + self.dexterity - distance//3
        return tohit

    def calculateDamage(self)->int:
        """Returns a damage calculated from attack"""
        damage = self.strength
        return damage

    def printSelf(self)->str:
        """Returns a string to display the character representation for a battle"""
        return self.displaychar