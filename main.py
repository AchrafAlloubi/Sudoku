import copy


class main:

    def __init__(self, taille):
        # taille 3 => une grille de 9*9
        self.taille = taille

        #Modelisation du CSP avec def de VDC
        # Les variables => la liste de toutes les cases de la grille
        # Domaine => la liste des valeurs possibles pour une case
        # Contraintes => si deux cases sont sur meme ligne ou colonne ou sur le meme bloc
                       # elles possedents des contraintes binaires
        self.variables = [[[0] for i in range(taille*taille)] for j in range(taille*taille)]
        self.domaines = []
        for t in range(1, taille*taille + 1):
            self.domaine.append(t)
        self.contraintes = {}
        # liste de toutes les cases, chaque case est definie de :
        # valeur de la case, nbre de valeur dispo pour la case, la liste des valeurs dispo pour la case
        self.gride = [[[0, 0, []] for i in range(taille * taille)] for j in range(taille * taille)]


    def creer_contrainte(self):

        for x in range(0, self.taille * self.taille):
            for y in range(0, self.taille * self.taille):
                liste_contraintes = []

                for a in range(0, len(self.variables[0])):
                    if x != a:
                        liste_contraintes.append([a, y])
                    if y != a:
                        liste_contraintes.append([x, a])
                dx = int(x / self.taille)
                dy = int(y / self.taille)
                for i in range(0, self.taille):
                    for j in range(0, self.taille):
                        liste_contraintes.append([dx * self.taille + i, dy * self.taille + j])

                liste_contraintes.enlever_valeur([x, y])
                nouvelle_liste = []

                for l in liste_contraintes:
                    if l not in nouvelle_liste:
                        nouvelle_liste.append(l)
                self.contraintes["[" + str(x) + "," + str(y) + "]"] = nouvelle_liste

    # todo affichage de la grille 9*9
    def afficher_grille(self):
        pass


    # MRV => on va parcourir l'ensemble des cases declarées dans la var self.gride et on recupere la case
    #dont le domaine est le plus petit
    #degree heuristic => doit retourner la case possedant le plus grand nombre de contraintes binaires


    #Pseudo code dans le cours
    def backtracking_search(self):
        return self.recursive_backtracking()

    def recursive_backtracking(self):

        if self.verifier_completude():
            return self.gride
        x, y = self.Select_Unasigned_Variable()

        # Boucle de la technique least constraining value
        if self.technique == "least constraining value":
            valeurs_possibles = self.leastConstrainingValue(x, y)
            for valeur,_ in valeurs_possibles:
                if self.consistant(x, y, valeur):
                    self.ajouter_valeur(x,y,valeur)
                    result = self.recursive_backtracking()
                    if result != False:
                        return result
                    self.enlever_valeur(x,y,valeur)

        #Boucle du MRV + degree-heuristic
        else:
            for valeur in self.gride[x][y][2]:
                if self.consistant(x, y, valeur):
                    self.ajouter_valeur(x,y,valeur)
                    resultat = self.recursive_backtracking()

                    if resultat != False:
                        return resultat
                    self.enlever_valeur(x,y,valeur)
        return False


    # Check si la grille est full, le 0 signifie que le case est vide
    def verifier_completude(self):
        full = True
        for ligne in self.gride:
            for case in ligne:
                if case[0] == 0:
                    full = False
                    break
        return full


    # retourne les coordonnées de la case à laquelle on va assigner une valeur
    # cela depend de la technique utilisée
    def Select_Unasigned_Variable(self):

        if self.technique == "ac3" or self.technique == "least constraining value":
            caseSelectionnee = [[0, 0], self.taille * self.taille + 1]
            for x in range(0, self.taille * self.taille):
                for y in range(0, self.taille * self.taille):
                    if self.gride[x][y][0] == 0:
                        caseSelectionnee = [[x, y], self.gride[x][y][1]]
                        return caseSelectionnee[0][0], caseSelectionnee[0][1]


        elif self.technique == "mrv":
            caseSelectionnee = [[0,0], self.taille*self.taille + 1]
            for x in range(0,self.taille*self.taille):
                for y in range(0,self.taille*self.taille):

                    if self.gride[x][y][0] == 0:
                        if self.gride[x][y][1] < caseSelectionnee[1]:
                            caseSelectionnee = [[x,y], self.gride[x][y][1]]


        elif self.technique == "degree heuristic":

            caseSelectionnee = [[self.taille * self.taille + 1, self.taille * self.taille + 1], 0]
            for x in range(0, self.taille * self.taille):
                for y in range(0, self.taille * self.taille):
                    if self.gride[x][y][0] == 0:
                        key = "[" + str(x) + "," + str(y) + "]"
                        if len(self.contraintes[key]) > caseSelectionnee[1]:
                            caseSelectionnee = [[x, y], self.gride[x][y][1]]


        return caseSelectionnee[0][0], caseSelectionnee[0][1]



    #verifier si la valeur donnée en param existe dans le domaine de valeurs possibles pour la case
    def consistant(self, x, y, valeur):

        if (x == self.taille * self.taille + 1 and y == self.taille * self.taille + 1):
            return False

        key = "[" + str(x) + "," + str(y) + "]"
        liste_contrainte = self.contrainte[key]

        if valeur in self.gride[x][y][2]:
            return True

        return False


    # add value dans gride + modification du domaine des valeurs possibles possedant contraintes binaires avec la case en question
    def ajouter_valeur(self, x, y, valeur):
        self.gride[x][y][0] = valeur
        self.gride[x][y][1] = 1
        self.gride[x][y][2] = [valeur]
        key = "[" + str(x) + "," + str(y) + "]"
        liste_contraintes = self.contraintes[key]

        for element in liste_contraintes:
            if valeur in self.gride[element[0]][element[1]][2]:
                self.gride[element[0]][element[1]][2].enlever_valeur(valeur)
                self.gride[element[0]][element[1]][1] -= 1


    def enlever_valeur(self, x, y, valeur):
        self.gride[x][y][0] = 0
        key = "[" + str(x) + "," + str(y) + "]"
        liste_contraintes = self.contraintes[key]
        domainesLocaux = copy.copy(self.domaines)

        for element in liste_contraintes:
            if self.gride[element[0]][element[1]][0] != 0 and self.gride[element[0]][element[1]][
                0] in domainesLocaux:
                domainesLocaux.enlever_valeur(self.gride[element[0]][element[1]][0])

        self.gride[x][y][2] = domainesLocaux
        self.gride[x][y][1] = len(domainesLocaux)

        for element in liste_contraintes:
            if self.gride[element[0]][element[1]][0] == 0:
                if valeur not in self.gride[element[0]][element[1]][2]:
                    second_key = "[" + str(element[0]) + "," + str(element[1]) + "]"
                    second_liste_contraintes = self.contraintes[second_key]
                    add_valeur = True
                    for second_element in second_liste_contraintes:
                        if valeur == self.gride[second_element[0]][second_element[1]][0]:
                            add_valeur = False
                    if add_valeur:
                        self.gride[element[0]][element[1]][2].append(valeur)
                        self.gride[element[0]][element[1]][1] += 1


    def leastConstrainingValue(self, x, y):
        valeurs = []
        for v in self.domaines:
            valeurs.append([v, 0])
        contraintes = self.contraintes["[" + str(x) + "," + str(y) + "]"]

        for v in valeurs:
            i = 0
            for c in contraintes:
                if self.gride[c[0]][c[1]][0] == 0 and v[0] in self.gride[c[0]][c[1]][2]:
                    i = i + 1
            v[1] = i

        valeurs.sort(key=lambda x: x[1])
        return valeurs


    # algo permet de créer liste of all arcs de la grille
    def list_arc_making(self):
        var=self.contraintes.copy()
        liste_arc=[]
        for i in self.domaines:
            for j in self.domaines:
                key=[i-1,j-1]
                arc=var.pop('['+str(key[0])+','+str(key[1])+']')
                for k in arc:
                    liste_arc+=[(key,k)]
        return liste_arc

    def test_inconsistance(self, x, Wj):

        for y in self.gride[Wj[0]][Wj[1]][2]:
            if x != y:
                return False
        return True

        # enlever les x des domaines de Wi si x n'est pas consistant
        # True ==> at least une valeur est retiree
        # False ==> Sinon

    def enlever_valeurs_inconsistantes(self, Wi, Wj):

        done = False
        for x in self.gride[Wi[0]][Wi[1]][2]:
            if self.test_inconsistance(x, Wj):
                self.gride[Wi[0]][Wi[1]][2].remove(x)
                self.gride[Wi[0]][Wi[1]][1] -= 1
                done = True
        return done

    def Arc_Consistency3(self):
        tail = self.list_arc_making()

        while (len(tail) > 0):
            Wi, Wj = tail.pop(0)
            if self.remove_inconsistent_values(Wi, Wj):
                for Wk in self.contraintes.get('[' + str(Wi[0]) + ',' + str(Wi[1]) + ']'):
                    tail = tail + [(Wk, Wi)]