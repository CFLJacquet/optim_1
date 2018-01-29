from constraint_programming import constraint_programming
from pprint import pprint

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class crossword_solveur:

    def __init__(self, grid_file, dico):
        self.dico = self.init_words(dico)
        self.cell = self.init_grid(grid_file)[0]
        self.H_segment = self.init_grid(grid_file)[1]
        self.V_segment = self.init_grid(grid_file)[2]
        self.var = self.init_domain()
        self.solver = constraint_programming(self.var)
        self.intersection(self.H_segment, self.V_segment, self.var)


    def init_grid(self, grid_file):
        
        grid = {}
        row = open(grid_file, 'r').readlines()
        n = len(row)
        m = len(row[0])
        
        H_segment = {}
        V_segment = {}

        for i, line in enumerate(row): 
            buff = []
            for j, elt in enumerate(line):
                if elt == ".":
                    grid[(i,j)] = ALPHABET
                    buff.append((i,j))
                else:
                    if buff and len(buff) > 1:
                        H_segment["H"+str(len(H_segment)+1)] = buff
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
                        V_segment["V"+str(len(V_segment)+1)] = buff
                        buff = []
                    else: 
                        buff = []

        return grid, H_segment, V_segment

    def init_domain(self):
        var = {}
        for key, value in self.H_segment.items():
            var[key] = set(self.dico[len(value)])
        
        for key, value in self.V_segment.items():
            var[key] = set(self.dico[len(value)])

        return var
            # parser dico de mots
            # lire ligne 1 pour connaitre largeur
            # lire nb total ligne pour connaitre la hauteur
            # pour chaque case qui est un point, retenir les coordonnées 
            # leur donner a chacune un alphabet de possibilité
            # créer pgrm contrainte qui dit que toutes les cases en hauteur et en longueur doivent faire partie du dico de mots

            # autre idée: trier par longueur de mots / segment

    def init_words(self, dico):
        liste_mots = open(dico, 'r').read().lower().split("\n")
        dico = {}
        for mot in liste_mots:
            n = len(mot)
            if n > 1:
            # les mots de longueur inférieure à 1 ne sont pas valables dans les mots-croissés.
                try:
                    dico[n].append(mot)
                except :
                    dico[n] = [mot]
        return dico

    def relation(self, i, j, liste_mot_h, liste_mot_v):
        rel = []
        for mot_h in liste_mot_h:
            for mot_v in liste_mot_v:
                if mot_h[i] == mot_v[j]:
                    rel.append((mot_h, mot_v))
        return set(rel)

    def intersection(self, horizontal, vertical, var):
        for h_key, h_positions in horizontal.items():
            # pour chaque section horizontale ....
            for v_key, v_positions in vertical.items():
                # ... on regarde si une section verticale l'intersecte
                for i in range(len(h_positions)):
                    for j in range(len(v_positions)):
                        # peut être amélioré
                        if h_positions[i] == v_positions[j]:
                            rel = self.relation(i, j, var[h_key], var[v_key])
                            self.solver.addConstraint(h_key, v_key, rel)

    def solve(self):
        return self.solver.solve()


    def __repr__(self):
        return "Mot-croisé avec {} mots à trouver.".format(len(self.var))



if __name__ == "__main__":
    c = crossword_solveur("crossword2.txt", "words2.txt")
    print(c.var)

