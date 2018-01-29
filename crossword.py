from constraint_programming import constraint_programming
from pprint import pprint

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class crossword_solveur:

    def __init__(self, grid_file, dico):
        self.cell = self.init_grid(grid_file)[0]
        self.segment = self.init_grid(grid_file)[1]
        self.dico = self.init_words(dico)

    def init_grid(self, grid_file):
        
        grid = {}
        row = open(grid_file, 'r').readlines()
        n = len(row)
        m = len(row[0])
        
        row_seg = []
        col_seg = []

        for i, line in enumerate(row): 
            buff = []
            for j, elt in enumerate(line):
                if elt == ".":
                    grid[(i,j)] = ALPHABET
                    buff.append((i,j))
                else:
                    if buff and len(buff) > 1:
                        row_seg.append(buff)
                        buff = []
                    else: 
                        buff = []
        
        for j in range(m):
            for i, line in enumerate(row):
                if line[j] == ".":
                    grid[(i,j)] = ALPHABET
                    buff.append((i,j))
                else:
                    if buff and len(buff) > 1:
                        col_seg.append(buff)
                        buff = []
                    else: 
                        buff = []
        
        

        return grid, row_seg + col_seg 
            # parser dico de mots
            # lire ligne 1 pour connaitre largeur
            # lire nb total ligne pour connaitre la hauteur
            # pour chaque case qui est un point, retenir les coordonnées 
            # leur donner a chacune un alphabet de possibilité
            # créer pgrm contrainte qui dit que toutes les cases en hauteur et en longueur doivent faire partie du dico de mots

            # autre idée: trier par longueur de mots / segment

    def init_words(self, dico):
        dico = open(dico, 'r').read().lower().split("\n")
        return dico

    # def solve(self):
    #     P = constraint_programming(self.grid)
    #     P.addConstraint(x)

    # def __repr__(self):
    #     return "{} \n\n {}".format(str(self.grid), len(self.dico))


if __name__ == "__main__":
    c = crossword_solveur("crossword2.txt", "words1.txt")
    pprint(c.segment)

