class Team():
    def __init__(self):
        self.team =[]

class Characters:
    def __init__(self,name,atk,deff,hp):
        self.name = name
        self.atk = atk
        self.deff = deff
        self.hp = hp
    

    def attaque(self, personnage):
        #calcul les degats
        degats = self.calcul_degats(personnage)
        #appliquer les degats
        personnage.appliquer_atk(degats)
    
    def calcul_degats(self, personnage):
        if self.atk - personnage.deff > 0:
            return self.atk - personnage.deff
        return 0
    
    def appliquer_atk(self, degats):
        if self.hp - degats > 0:
            self.hp -= degats
        else:
            self.hp = 0