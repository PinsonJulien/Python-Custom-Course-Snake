# -*- coding: utf-8 -*-

import random
import datetime

class Player :
    
    keyboard_key = {'z':(-1,0),
                    'q':(0,-1),
                    's':(1,0),
                    'd':(0,1)}
    
    def __init__(self, name, points = 0, start = (0,0)):
        self.name = name
        self.points = points
        self.position = start
    
    def move (self) :
        
        key = input("Mouvement (z,q,s,d) : ")
        while key not in Player.keyboard_key.keys() :
            key = input("Mouvement (z,q,s,d) : ")
        
        move = Player.keyboard_key[key]
        self.position = (self.position[0] + move[0], self.position[1] + move[1])
        
    

class Game :
    
    def __init__(self, player, size=10):
        self.player = player
        self.board_size = size
        self.candies = []
        
    # Dessine le plateau
    def draw(self):
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies :
                    print("*",end=" ")
                elif (line,col) == self.player.position :
                    print("O",end=" ")
                else : 
                    print(".",end=" ")
            print()
            
    # Fait apparaitre un bonbon
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))
        if new_candy not in self.candies :
            self.candies.append(new_candy)
            
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies:
            self.player.points += 1
            self.candies.remove(self.player.position)
    
        
        
    # Joue une partie complète
    def play(self):
        print("--- Début de la partie ---")
        self.draw()
        
        end = Game.end_time(1,0)
        now = datetime.datetime.today()
        
        while now < end :
            self.player.move()
            self.check_candy()
            
            if random.randint(1,3) == 1 :
                self.pop_candy()
                
            self.draw()
            
            now = datetime.datetime.today()
        
        
        print("----- Terminé -----")
        print("Vous avez", self.player.points, "points" )


    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end
        



if __name__ == "__main__" :
     
    p = Player("Moi")
    g = Game(p)
    g.play()

    
    
    
