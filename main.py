class main:

    def __init__(self, taille):
        # taille 3 => une grille de 9*9
        self.taille = taille

        #Modelisation du CSP avec def de VDC
        self.variables = [[[0] for i in range(taille*taille)] for j in range(taille*taille)]
        self.domaines = []
        for t in range(1, taille*taille + 1):
            self.domaine.append(t)
        self.contraintes = {}


    #Pseudo code dans le cours
    def backtracking_search(self):
        return self.recursive_backtracking()

    def recursive_backtracking(self):
        #print(self.assignment)

        # todo Verfier_completude()
        if self.verifier_completude():
            return self.assignment
        x, y = self.Select_Unasigned_Variable()

        # Boucle de la technique least constraining value
        if self.technique == "least constraining value":
            valeurs_possibles = self.leastConstrainingValue(x, y)
            for valeur,_ in valeurs_possibles:
                if self.consistant(x, y, valeur):
                    self.add(x,y,valeur)
                    result = self.recursive_backtracking()
                    if result != False:
                        return result
                    self.remove(x,y,valeur)



    def leastConstrainingValue(self, x, y):
        valeurs = []
        for v in self.domaines:
            valeurs.append([v, 0])
        contraintes = self.contraintes["[" + str(x) + "," + str(y) + "]"]

        for v in valeurs:
            i = 0
            for c in contraintes:
                if self.assignment[c[0]][c[1]][0] == 0 and v[0] in self.assignment[c[0]][c[1]][2]:
                    i = i + 1
            v[1] = i

        valeurs.sort(key=lambda x: x[1])
        return valeurs

    def Select_Unasigned_Variable(self):

        if self.technique == "least constraining value" :
            caseSelectionnee = [[0, 0], self.taille * self.taille + 1]
            for x in range(0, self.taille * self.taille):
                for y in range(0, self.taille * self.taille):
                    if self.assignment[x][y][0] == 0:
                        caseSelectionnee = [[x, y], self.assignment[x][y][1]]
                        return caseSelectionnee[0][0], caseSelectionnee[0][1]


        return caseSelectionnee[0][0], caseSelectionnee[0][1]


    def consistant(self, x, y, valeur):

        if (x == self.taille * self.taille + 1 and y == self.taille * self.taille + 1):
            return False

        key = "[" + str(x) + "," + str(y) + "]"
        liste_contrainte = self.contrainte[key]

        if valeur in self.assignment[x][y][2]:
            return True

        return False
