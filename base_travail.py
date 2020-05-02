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
        self.last_position = start

    # Définit la position de l'axe choisit et vérifie si l'on passe ou non un mur.
    def SetPosition (self, axis, move) :
        if self.position[axis] == 0 and move[axis] == -1:
            pos = 9
        elif self.position[axis] == 9 and move[axis] == 1:
            pos = 0
        else :
            pos = self.position[axis] + move[axis]

        return pos
    
    def move (self) :
        
        key = input("Mouvement (z,q,s,d) : ")
        while key not in Player.keyboard_key.keys() :
            key = input("Mouvement (z,q,s,d) : ")
        
        move = Player.keyboard_key[key]

        # Le passage du mur ne se fait que si l'on devrait passer à une valeur -1 ou 10
        # qui ne sont pas comprises dans le tableau de 10x10 car un axe >=0 et <=9.
        new_position = ( self.SetPosition(0, move), self.SetPosition(1, move) )

        # On empêche le joueur de retourner en arrière.
        # La variable last_position permet de sauvegarder l'ancienne position avant son changement.
        if self.last_position != new_position:
            self.last_position = self.position
            self.position = new_position       
    
class Game :

    #Dictionnaire des type de bonbons et leur valeur en point.
    candies = {'Bonbon': 1,
                'Super bonbon': 5,
                'Mega bonbon': 10,
                'Faux bonbon': -2}
    
    def __init__(self, player, size=10):
        self.player = player
        self.board_size = size
        self.candies_position = []
        self.candies_type = []
        self.candies_ate = []
        
    # Dessine le plateau
    def draw(self):
        for line in range(self.board_size):
            for col in range(self.board_size):
                if (line,col) in self.candies_position :
                    
                    # On affiche les bonbons sous une autre forme en fonction de leur type.
                    candy_index = self.candies_position.index((line,col))
                    if self.candies_type[candy_index] == 'Bonbon':
                        print("©",end=" ")
                    elif self.candies_type[candy_index] == 'Super bonbon' :
                        print("£",end=" ")
                    elif self.candies_type[candy_index] == 'Mega bonbon' :
                        print("¶",end=" ")
                    elif self.candies_type[candy_index] == 'Faux bonbon':
                        print("X",end=" ")
            
                elif (line,col) == self.player.position :
                    print("0",end=" ")
                else : 
                    print(".",end=" ")
            print()
        print()
            
    # Fait apparaitre un bonbon
    def pop_candy(self):
        new_candy = (random.choice(range(self.board_size)),random.choice(range(self.board_size)))

        #Désormais, il est possible d'avoir différent type de bonbon générés que l'on récupère dans le dictionnaire
        candy_type = random.choice(list(Game.candies))
        if new_candy not in self.candies_position :
            # On ajoute à 2 lists : La position et le type de bonbons généré.
            self.candies_position.append(new_candy)
            self.candies_type.append(candy_type)
            
    # Regarde s'il y a un bonbon à prendre (et le prend)
    def check_candy(self):
        if self.player.position in self.candies_position:
            # Pour utiliser le même index que celui de la position.
            candy_index = self.candies_position.index(self.player.position)
            candy_type = self.candies_type[candy_index]
            # On incrémente les points avec la valeur du bonbon mangé, qui est enregistrée dans le dictionnaire
            self.player.points += Game.candies.get(candy_type)

            # On enregistre le bonbon mangé dans un liste pour le tableau des scores.
            self.candies_ate.append(candy_type)
            
            # On retire des 2 listes la position et le type de bonbon.
            self.candies_position.remove(self.player.position)
            self.candies_type.pop(candy_index)

    # Affiche le tableau de score de fin de partie.
    def score_board(self):
        print("----- Terminé -----")
        print()
        print("Nombre de bonbons mangés :")
        # Chaque type de bonbon mangés sont affichés, avec leur nombre mangés durant la partie, les points qu'ils octroient, le total.
        # Puis le score final est affiché.
        for candy, points in Game.candies.items():
            total = self.candies_ate.count(candy)*points
            print (candy, ': ', self.candies_ate.count(candy),'*', points, '=', total,' points')
        print()        
        print(self.player.name + ", vous avez fait un score de", self.player.points, "points !" )
        
    # Joue une partie complète
    def play(self):
        print()
        print("--- Début de la partie ---")
        print()
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
        
        # Partie finie, on affiche le score final.
        self.score_board()
        # Puis on enregistre dans le fichier des meilleurs score.
        
        # Demande si l'on souhaite faire une nouvelle partie, en cas de refus, on ferme le jeu.
        print()
        key = input("Nouvelle partie ? O/n : ")
        while key.upper() not in ('O','N') :
            key = input("Nouvelle partie ? O/n : ")

        if key.upper() == 'O':
            new_game()
        else :
            exit()

    @staticmethod
    # retourne le moment où le jeu est censé être fini
    def end_time(delta_minute, delta_second):
        delta = datetime.timedelta(minutes=delta_minute, seconds=delta_second)
        end = datetime.datetime.today() + delta
        return end

# Pour lancer une partie de jeu, utile pour pouvoir relancer une partie.
def new_game():
    player_name = input("Veuillez entrer votre nom de joueur : ")
    p = Player(player_name)
    g = Game(p)
    g.play()


if __name__ == "__main__" :
    new_game()

    
    
    
