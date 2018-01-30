from constraint_programming import constraint_programming
import time
from pprint import pprint

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class crossword_solveur:

    def __init__(self, grid_file, dico):
        self.dico = self.init_words(dico)
        grid = self.init_grid(grid_file)
        self.cell = grid[0]
        self.H_segment = grid[1]
        self.V_segment = grid[2]
        self.n = grid[3]
        self.m = grid[4]
        self.var = self.init_domain()
        self.solver = constraint_programming(self.var)
        #self.solver.maintain_arc_consistency()
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

        return grid, H_segment, V_segment, n, m

    def init_domain(self):
        var = {}
        for key, value in self.H_segment.items():
            var[key] = set(self.dico[len(value)])
        
        for key, value in self.V_segment.items():
            var[key] = set(self.dico[len(value)])

        return var

    def init_words(self, dico):
        """
        Cette fonction prend un fichier contenant l'ensemble des mots qui peuvent être utilisés pour compléter
        le mot croissé. Cet ensemble en mis dans un dictionnaire ayant pour clés les tailles possibles de mots et
        comme valeurs associées la liste des mots de cette taille. Ce dictionnaire permet de definir le
        domaine de chaque variable.
        :param dico: fichier de mots
        :return: dictionnaire par taille
        """
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
        """
        A partir des points d'intersection de deux variables et de leur domaine, on détermne l'ensemble des couples
        possibles de mots pour ces deux variables. Cette relation sera ajoutée aux contraintes pour le solveur.
        :param i: point d'intersection dans le mot horizontal
        :param j: point d'intersection dans le mot vertical
        :param liste_mot_h: liste des mots possibles pour la variable horizontale
        :param liste_mot_v: liste des mots possibles pour la variable verticale
        :return: set des couples possibles de mots
        """
        t1 = time.time()
        rel = []
        dic_h = {}
        for mot_h in liste_mot_h:
            lettreh = mot_h[i]
            try :
                dic_h[lettreh].append(mot_h)
            except:
                dic_h[lettreh] = [mot_h]
        for mot_v in liste_mot_v:
            lettrev = mot_v[j]
            try:
                for m in dic_h[lettrev]:
                    rel.append((m, mot_v))
            except:
                pass
        t2 = time.time()
        print(t2-t1)
        return set(rel)

    def intersection(self, horizontal, vertical, var):
        """
        calcule tous les intersections entre les variables et fait appel à la fonction relation pour construire
        les relations. Elles sont ajoutée aux contraintes du solveur.
        :param horizontal: dictionnaire des varibles horizontales avec leur position
        :param vertical: dictionnaire des varibles horizontales avec leur position
        :param var: dictionnaire des varibles avec leur domaine
        :return:
        """
        for h_key, h_positions in horizontal.items():
            print(h_key)
            # pour chaque section horizontale ....
            for v_key, v_positions in vertical.items():
                # ... on regarde si une section verticale l'intersecte
                for i in range(len(h_positions)):
                    for j in range(len(v_positions)):
                        if h_positions[i] == v_positions[j]:
                            rel = self.relation(i, j, var[h_key], var[v_key])
                            self.solver.addConstraint(h_key, v_key, rel)
                            j = len(v_positions)-1
                            i = len(h_positions)-1

                        
    def solve(self):
        """
        appel de la fonction solve du solveur pour avoir une solution possible du mot croisé
        :return: une solution possible sous form de dictionnaire avec comme valeur un mot pour chaque variable
        """
        return self.solver.solve()

    def display_solution(self):
        """
        fait appel à la fonction solve du solveur. A partir de la solution trouvée, recoustruit le grille pour
        avoir la solution visuellement.
        :return:
        """
        solution = self.solve()
        sol = []
        for k in range(self.n):
            sol.append(['#']*self.m)
        for sequence in solution:
            if sequence[0] == 'H':
                positions = self.H_segment[sequence]
            else:
                positions = self.V_segment[sequence]
            for i in range(len(positions)):
                sol[positions[i][0]][positions[i][1]] = solution[sequence][i]
        for ligne in sol:
            content = ""
            for col in ligne:
                content += col
            print(content)


    def __repr__(self):
        return "Mot-croisé avec {} mots à trouver.".format(len(self.var))



if __name__ == "__main__":
    t1 = time.time()
    c = crossword_solveur("crossword1.txt", "words1.txt")
    c.display_solution()
    t2 = time.time()
    print(t2-t1)

