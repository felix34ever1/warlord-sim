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
        self.colorpairID = 0

        # Get random name in character list
        with open("names.txt","r") as f:
            self.name = f.readlines(randint(1,1000))[-1]
            self.name = self.name.removesuffix("\n")
        
    def getName(self)->str:
        return self.name

    def getCoords(self)->list[int]:
        return [self.x,self.y]

    def setCoords(self,x:int,y:int):
        self.x = x
        self.y = y

    def getcolorpairID(self)->int:
        return self.colorpairID

    def setcolorpairID(self,newID:int):
        self.colorpairID = newID
        
    def meleeAttack(self)->int:
        """Returns a number to hit in melee"""
        tohit = randint(1,6) + self.dexterity
        return tohit

    def rangedAttack(self,distance:int)->int:
        """Returns a number to hit in ranged"""
        tohit = randint(1,6) + self.dexterity - distance//3
        return tohit
    
    def getEvasion(self)->int:
        """Returns evasion"""
        return self.dexterity+randint(1,6)

    def calculateDamage(self)->int:
        """Returns a damage calculated from attack"""
        damage = self.strength
        return damage
    
    def takeDamage(self,damage:int)->int:
        """Deals damage to the unit, returning resistance for logging reasons"""
        damage -= self.resistance
        if damage>0:
            self.hp -= damage

        return self.resistance

    def printSelf(self)->str:
        """Returns a string to display the character representation for a battle"""
        return self.displaychar
    
    def getHP(self)->int:
        """Returns the character HP, likely used to check if enemy has died"""
        return self.hp

if __name__ == "__main__":
    ch = Character()
    print(ch.getName())