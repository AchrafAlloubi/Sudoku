from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QLineEdit, QVBoxLayout, QWidget, QPushButton, QLabel, QToolBar, QStatusBar, QWidgetItem, QColorDialog, QSpinBox
from PySide6.QtGui import QPalette, QColor, QScreen, QGuiApplication, QFont, QAction
import sys
import PySide6
import copy


technique_utilisee = "least constraining value"
#technique_utilisee = "mrv"
#technique_utilisee = "degree heuristic"
#technique_utilisee = "ac3"

class main:

    def __init__(self, taille):
        # taille 3 => une grille de 9*9
        self.taille = taille

        #Modelisation du CSP avec def de VDC
        # Les variables => la liste de toutes les cases de la grille
        # domaines => la liste des valeurs possibles pour une case
        # Contraintes => si deux cases sont sur meme ligne ou colonne ou sur le meme bloc
                       # elles possedents des contraintes binaires
        self.variables = [[[0] for i in range(taille*taille)] for j in range(taille*taille)]
        self.domaines = []
        for t in range(1, taille*taille + 1):
            self.domaines.append(t)
        self.contraintes = {}
        # liste de toutes les cases, chaque case est definie de :
        # valeur de la case, nbre de valeur dispo pour la case, la liste des valeurs dispo pour la case
        self.gride = [[[0, 0, []] for i in range(taille * taille)] for j in range(taille * taille)]
        self.technique = technique_utilisee
        print("> Technique utilisée : ",self.technique)

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

                liste_contraintes.remove([x, y])
                nouvelle_liste = []

                for l in liste_contraintes:
                    if l not in nouvelle_liste:
                        nouvelle_liste.append(l)
                self.contraintes["[" + str(x) + "," + str(y) + "]"] = nouvelle_liste

    # todo affichage de la grille 9*9
    def afficher_grille(self):
        c = 0
        t = self.taille

        for liste in self.gride:
            if (t == self.taille):
                print("  ", end="")
                for i in range(0, 13):
                    print(" - ", end='')
                print("")
                t = 0
            t = t + 1
            print(" || ", end='')
            for element in liste:
                c = c + 1
                if (element[0] == 0):
                    print(" ", end='')
                else:
                    print(element[0], end='')
                if (c == self.taille):
                    print(" || ", end='')
                    c = 0
                else:
                    print(" | ", end='')
            print("")

        print("  ", end="")
        for i in range(0, self.taille * self.taille + 4):
            print(" - ", end='')
        print("")


    def check_conditions(self):
        for x in range(0, self.taille * self.taille):
            for y in range(0, self.taille * self.taille):
                key = "[" + str(x) + "," + str(y) + "]"
                liste_contraintes = self.contraintes[key]
                for element in liste_contraintes:
                    if self.gride[element[0]][element[1]][0] == self.gride[x][y][0]:
                        return False

        return True

    # MRV => on va parcourir l'ensemble des cases declarées dans la var self.gride et on recupere la case
    #dont le domaines est le plus petit
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
                    self.add(x,y,valeur)
                    resultat = self.recursive_backtracking()
                    if resultat != False:
                        return resultat
                    self.remove(x,y,valeur)

        elif self.technique == "ac3":
            for valeur in self.gride[x][y][2]:

                # Ajouter valeur
                val = self.gride[x][y][2]
                self.gride[x][y][2] = [valeur]
                self.gride[x][y][0] = valeur
                nb = self.gride[x][y][1]
                self.gride[x][y][1] = 1

                self.Arc_Consistency3()

                resultat = self.recursive_backtracking()
                if resultat != False:

                    return resultat

                # Enlever valeur
                self.gride[x][y][0] = 0
                self.gride[x][y][1] = nb
                self.gride[x][y][2] = val
                self.initialiser_gride()


        #Boucle du MRV + degree-heuristic
        else:
            for valeur in self.gride[x][y][2]:
                if self.consistant(x, y, valeur):
                    self.add(x,y,valeur)
                    resultat = self.recursive_backtracking()

                    if resultat != False:
                        return resultat
                    self.remove(x,y,valeur)
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
        if self.technique == "mrv":
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

        elif self.technique == "least constraining value" or self.technique == "ac3":
            caseSelectionnee = [[0, 0], self.taille * self.taille + 1]
            for x in range(0, self.taille * self.taille):
                for y in range(0, self.taille * self.taille):
                    if self.gride[x][y][0] == 0:
                        caseSelectionnee = [[x, y], self.gride[x][y][1]]
                        return caseSelectionnee[0][0], caseSelectionnee[0][1]


        return caseSelectionnee[0][0], caseSelectionnee[0][1]



    #verifier si la valeur donnée en param existe dans le domaines de valeurs possibles pour la case
    def consistant(self, x, y, valeur):

        if (x == self.taille * self.taille + 1 and y == self.taille * self.taille + 1):
            return False

        key = "[" + str(x) + "," + str(y) + "]"
        liste_contraintes = self.contraintes[key]

        if valeur in self.gride[x][y][2]:
            return True

        return False

    def initialiser_gride(self):

        for x in range(0, self.taille * self.taille):
            for y in range(0, self.taille * self.taille):
                valeurs = copy.copy(self.domaines)

                if self.gride[x][y][0] != 0:
                    self.gride[x][y][1] = 1
                    self.gride[x][y][2] = [self.gride[x][y][0]]
                else:
                    key = "[" + str(x) + "," + str(y) + "]"
                    liste_contraintes = self.contraintes[key]
                    for element in liste_contraintes:
                        if self.gride[element[0]][element[1]][0] in valeurs:
                            valeurs.remove(self.gride[element[0]][element[1]][0])

                    self.gride[x][y][1] = len(valeurs)
                    self.gride[x][y][2] = valeurs



    # add value dans gride + modification du domaines des valeurs possibles possedant contraintes binaires avec la case en question
    def add(self, x, y, valeur):
        self.gride[x][y][0] = valeur
        self.gride[x][y][1] = 1
        self.gride[x][y][2] = [valeur]
        key = "[" + str(x) + "," + str(y) + "]"
        liste_contraintes = self.contraintes[key]

        for element in liste_contraintes:
            if valeur in self.gride[element[0]][element[1]][2]:
                self.gride[element[0]][element[1]][2].remove(valeur)
                self.gride[element[0]][element[1]][1] -= 1


    def remove(self, x, y, valeur):

        self.gride[x][y][0] = 0
        key = "[" + str(x) + "," + str(y) + "]"
        liste_contraintes = self.contraintes[key]
        domainesLocaux = copy.copy(self.domaines)


        for element in liste_contraintes:
            if self.gride[element[0]][element[1]][0] != 0 and self.gride[element[0]][element[1]][0] in domainesLocaux:
                domainesLocaux.remove(self.gride[element[0]][element[1]][0])

        self.gride[x][y][2] = domainesLocaux
        self.gride[x][y][1] = len(domainesLocaux)

        for element in liste_contraintes:
            if self.gride[element[0]][element[1]][0] == 0:
                if valeur not in self.gride[element[0]][element[1]][2]:
                    second_key = "[" + str(element[0]) + "," + str(element[1]) + "]"
                    second_liste_contraintes = self.contraintes[second_key]
                    ajouter_valeur = True
                    for second_element in second_liste_contraintes:
                        if valeur == self.gride[second_element[0]][second_element[1]][0]:
                            ajouter_valeur = False
                    if ajouter_valeur:
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
            if self.enlever_valeurs_inconsistantes(Wi, Wj):
                for Wk in self.contraintes.get('[' + str(Wi[0]) + ',' + str(Wi[1]) + ']'):
                    tail = tail + [(Wk, Wi)]


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.choiceBar()
        self.taille = 3
        self.init_screen()
        self.setStyleSheet("background-color: moccasin;")


    def init_screen(self):

        self.setWindowTitle("Grille Sudoku")
        max_taille = len(str(self.taille * self.taille))
        verticalLayout = QVBoxLayout()
        verticalLayout.setAlignment(PySide6.QtCore.Qt.AlignVCenter)
        self.text = QLabel()
        self.text.setText("Enter values and press \"Lancer\"")
        font = self.text.font()
        font.setPointSize(20)
        self.text.setFont(font)
        self.text.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
        verticalLayout.addWidget(self.text)

        self.layout = QGridLayout()
        for x in range(0, self.taille * self.taille):
            for y in range(0, self.taille * self.taille):
                box = QLineEdit()
                box.setMaxLength(max_taille)
                font = box.font()
                font.setPointSize(100 / self.taille)
                box.setFont(font)
                box.setMaximumSize(150 / self.taille, 150 / self.taille)
                box.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
                self.layout.addWidget(box, x, y)

        self.layout.setAlignment(PySide6.QtCore.Qt.AlignHCenter)
        verticalLayout.addLayout(self.layout)
        # Bouton lancer

        launch_button = QPushButton("Lancer")
        launch_button.setStyleSheet('QPushButton {background-color: #A3C1DA}')
        launch_button.clicked.connect(self.bouton_lancer)
        font = launch_button.font()
        font.setPointSize(15)
        launch_button.setFont(font)
        verticalLayout.addWidget(launch_button)

        # Bouton effacer
        erase_button = QPushButton("Effacer")
        erase_button.setStyleSheet('QPushButton {background-color: #A3C1DA}')
        erase_button.clicked.connect(self.bouton_effacer)
        font = erase_button.font()
        font.setPointSize(15)
        erase_button.setFont(font)

        verticalLayout.addWidget(erase_button)


        widget = QWidget()
        widget.setLayout(verticalLayout)
        self.setCentralWidget(widget)

    # Récupère input of user et affiche la grille par l'algo backtracking search
    def bouton_lancer(self):
        layout = self.layout
        m = main(self.taille)

        m.afficher_grille()

        for x in range(0, self.taille * self.taille):
            for y in range(0, self.taille * self.taille):
                box = layout.itemAtPosition(x, y).widget()
                if box.text() == "":
                    m.gride[x][y][0] = 0
                else:
                    box.setStyleSheet("color: coral;")
                    m.gride[x][y][0] = int(box.text())

        m.afficher_grille()
        m.creer_contrainte()
        m.initialiser_gride()
        m.grid = m.gride

        if (m.backtracking_search() != False):
            for x in range(0, self.taille * self.taille):
                for y in range(0, self.taille * self.taille):
                    box = layout.itemAtPosition(x, y).widget()
                    box.setText(str(m.gride[x][y][0]))
            self.text.setText("Problem solved")
        else:
            self.text.setText("There is no solution !!")

        m.afficher_grille()

    # Retire toutes les valeurs du sudoku afin que l'utilisateur puisse rentrer un nouveau sudoku à résoudre
    def bouton_effacer(self):
        layout = self.layout
        self.text.setText("Enter values and press \"Lancer\"")
        for x in range(0, self.taille * self.taille):
            for y in range(0, self.taille * self.taille):
                box = layout.itemAtPosition(x, y).widget()
                box.setText("")
                box.setStyleSheet("color: black;")


    def choiceBar(self):
        menuBar = self.menuBar()
        self.techniqueMenu = menuBar.addMenu("&Technique utilisée")

        ac3_action = QAction("AC 3", self)
        ac3_action.setStatusTip("Technique AC3")
        #connecter bouton à la methode
        ac3_action.triggered.connect(self.Arc_Consistency3_clicked)

        mrv_action = QAction("MRV", self)
        mrv_action.setStatusTip("Technique MRV")
        #connecter bouton à la methode
        mrv_action.triggered.connect(self.MRV_clicked)

        degree_action = QAction("degree_heuristic", self)
        degree_action.setStatusTip("Technique degree heuristic")
        #connecter bouton à la methode
        degree_action.triggered.connect(self.DegreeHeuristic_clicked)

        lcv_action = QAction("least_constraining_value", self)
        lcv_action.setStatusTip("Technique least constraining value")
        #connecter bouton à la methode
        lcv_action.triggered.connect(self.LeastConstrainingValue_clicked)

        self.techniqueMenu.addAction(ac3_action)
        self.techniqueMenu.addAction(mrv_action)
        self.techniqueMenu.addAction(degree_action)
        self.techniqueMenu.addAction(lcv_action)


    def Arc_Consistency3_clicked(self, s):

        global technique_utilisee
        technique_utilisee = "ac3"
        print(technique_utilisee)
        self.techniqueMenu.setTitle("&Arc Consistency3")

    def MRV_clicked(self, s):
        global technique_utilisee
        technique_utilisee = "mrv"
        print(technique_utilisee)
        self.techniqueMenu.setTitle("&Minimum Remaining Values")

    def DegreeHeuristic_clicked(self, s):
        global technique_utilisee
        technique_utilisee = "degree heuristic"
        print(technique_utilisee)
        self.techniqueMenu.setTitle("&degree heuristic")

    def LeastConstrainingValue_clicked(self, s):
        global technique_utilisee
        technique_utilisee = "least constraining value"
        print(technique_utilisee)
        self.techniqueMenu.setTitle("&Least Constraining Value")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.showMaximized()
    app.exec()