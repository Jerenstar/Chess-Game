import numpy as np 
from case import *
from pieces import *
from copy import *
import time as t
class Echiquier:
	def __init__(self):
		self.lignes = [8,7,6,5,4,3,2,1]
		self.colonnes = [1,2,3,4,5,6,7,8]
		self.cases = []
		self.piece_prises = {"blanc":[],"noir":[]}
		self.tour_couleur = "blanc"
		self.msg_blanc = "Blancs: \n"
		self.msg_noir = "Noirs: \n"

		for i in self.lignes:
			for j in self.colonnes:
				if i == 2:
					self.cases.append(Case(i,j,Pion(i,j,"blanc",self)))
				elif i == 7:
					self.cases.append(Case(i,j,Pion(i,j,"noir",self)))
				elif i == 8:
					if j == 1 or j == 8:
						self.cases.append(Case(i,j,Tour(i,j,"noir",self)))
					if j == 2 or j == 7:
						self.cases.append(Case(i,j,Cavalier(i,j,"noir",self)))
					if j == 3 or j == 6:
						self.cases.append(Case(i,j,Fou(i,j,"noir",self)))
					if j == 4:
						self.cases.append(Case(i,j,Reine(i,j,"noir",self)))
					if j == 5:
						self.cases.append(Case(i,j,Roi(i,j,"noir",self)))
				elif i == 1:
					if j == 1 or j == 8:
						self.cases.append(Case(i,j,Tour(i,j,"blanc",self)))
					if j == 2 or j == 7:
						self.cases.append(Case(i,j,Cavalier(i,j,"blanc",self)))
					if j == 3 or j == 6:
						self.cases.append(Case(i,j,Fou(i,j,"blanc",self)))
					if j == 4:
						self.cases.append(Case(i,j,Reine(i,j,"blanc",self)))
					if j == 5:
						self.cases.append(Case(i,j,Roi(i,j,"blanc",self)))

				else:
					self.cases.append(Case(i,j))

		self.cases_couvrables_blanche = self.cases_couvrables("blanc")
		self.cases_couvrables_noir = self.cases_couvrables("noir")
		self.coup_joues = []

	def ecrire_pts(self):
		"""
		Ecrit le nb de point qu'a chaque joueur en fct dun nb de piece qu'il a prit
		"""

		nb_pts = {"P":1,"T":5,"C":3,"F":3,"Q":9}
		cb = 0
		cn = 0
		self.msg_blanc ="Blancs: \n"
		self.msg_noir ="Noirs: \n"
		for i in self.piece_prises:
			if i == "blanc":
				for k in self.piece_prises[i]:
					cb += nb_pts[k[0]]
					self.msg_blanc = self.msg_blanc +k[0] + ","
			else:
				for k in self.piece_prises[i]:
					cn += nb_pts[k[0]]
					self.msg_noir = self.msg_noir + k[0] + ","
		
		if cb-cn > 0:

			self.msg_blanc = self.msg_blanc + "+" + "{}".format(cb-cn)
		elif cn-cb > 0:
			self.msg_noir = self.msg_noir + "+" + "{}".format(cn-cb)
			


	def __str__(self):
		tour_couleurs_accorde = {"noir":"noirs", "blanc":"blancs"}
		Ech = """
8	%s, %s, %s, %s, %s, %s, %s, %s

7	%s, %s, %s, %s, %s, %s, %s, %s 

6	%s, %s, %s, %s, %s, %s, %s, %s

5	%s, %s, %s, %s, %s, %s, %s, %s   
                                            Tour des {tour}
4	%s, %s, %s, %s, %s, %s, %s, %s      {Echec}

3	%s, %s, %s, %s, %s, %s, %s, %s

2	%s, %s, %s, %s, %s, %s, %s, %s

1	%s, %s, %s, %s, %s, %s, %s, %s
	 
	 
	 a   b   c   d   e   f   g   h		
	""".format(tour = tour_couleurs_accorde[self.tour_couleur],Echec = self.echec(self.tour_couleur)[1])%(str(self.cases[0]),str(self.cases[1]),str(self.cases[2]),str(self.cases[3]),str(self.cases[4]),str(self.cases[5]),str(self.cases[6]),str(self.cases[7]),
		str(self.cases[8]),str(self.cases[9]),str(self.cases[10]),str(self.cases[11]),str(self.cases[12]),str(self.cases[13]),str(self.cases[14]),str(self.cases[15]),
		str(self.cases[16]),str(self.cases[17]),str(self.cases[18]),str(self.cases[19]),str(self.cases[20]),str(self.cases[21]),str(self.cases[22]),str(self.cases[23]),
		str(self.cases[24]),str(self.cases[25]),str(self.cases[26]),str(self.cases[27]),str(self.cases[28]),str(self.cases[29]),str(self.cases[30]),str(self.cases[31]),
		str(self.cases[32]),str(self.cases[33]),str(self.cases[34]),str(self.cases[35]),str(self.cases[36]),str(self.cases[37]),str(self.cases[38]),str(self.cases[39]),
		str(self.cases[40]),str(self.cases[41]),str(self.cases[42]),str(self.cases[43]),str(self.cases[44]),str(self.cases[45]),str(self.cases[46]),str(self.cases[47]),
		str(self.cases[48]),str(self.cases[49]),str(self.cases[50]),str(self.cases[51]),str(self.cases[52]),str(self.cases[53]),str(self.cases[54]),str(self.cases[55]),
		str(self.cases[56]),str(self.cases[57]),str(self.cases[58]),str(self.cases[59]),str(self.cases[60]),str(self.cases[61]),str(self.cases[62]),str(self.cases[63]))
		return(Ech)

	def entrez_coord(self,message):
		"""
		Demande de taper une case avec un message et 
		check le fait que les coordonnées rentrées soient de la forme
		[lettrechiffre] = a1,b8,c4 etc...
		avec a<=lettre<=h et 1<=chiffre<=8
		sinon demande de re-rentrer la case
		"""

		coord = str(input(message))

		while not (len(coord) == 2 and coord[0] in ["a","b","c","d","e","f","g","h"] and int(coord[1]) in [1,2,3,4,5,6,7,8]):
			print("case non valide (ex de case valide : a7)")
			coord = str(input(message))
		return coord


	def num_case(self,case):
		colonnes_cor = {1:"a", 2:"b" , 3:"c" ,4:"d",5:"e",6:"f",7:"g",8:"h"}

		return '{}{}'.format(colonnes_cor[case%8+1],8-case//8)

	def case_num(self,case):
		"""
		convertit une coordonée de case de type f8, a2 etc... en son numéro dans la liste 
		des cases de l'échiquier numérotées de 0 à 63

		"""

		colonnes_cor = {"a":1 , "b":2 , "c":3 ,"d":4,"e":5,"f":6,"g":7,"h":8}
		ligne = int(case[1])
		col = int(colonnes_cor[case[0]])

		return col-1+ (8-int(ligne))*8
	
	def case_coord(self,case):

		"""
		convertit une coordonée de case de type a3, c4 etc... en un index ligne colonnes
		ex a3 = [3,1] / f4 = [4,6] etc...

		"""

		colonnes_cor = {"a":1 , "b":2 , "c":3 ,"d":4,"e":5,"f":6,"g":7,"h":8}
		ligne = int(case[1])
		col = int(colonnes_cor[case[0]])
		return [int(ligne),col]

	def coord_num(self,coord):
		"""
		convertit la coordonée d'une case de type [i,j]
		en son numéro dans la liste des cases de l'échiquier numérotées de 0 à 63

		"""

		i,j = coord[0:]
		return j - 1+ (8-i)*8

	def num_coord(self,num):
		"""
		transforme un numéro de case sur l'echiquier 64*1 en une cooordonée 

		La case 0 (haut gauche) --> [1,8]
		la case 63 (bas droite) --> [8,1]
		
		origine du système de coordonées en bas à droite [colonne,ligne]
		"""
		return [num%8+1,8-(num//8)]

	def echec(self,couleur):
		
		"""
		Renvoie True si la couleur séléctionée subie un échec 
		
		"""
		rois = {"blanc" : "Kb" , "noir" : "Kn"}
		ind_case_roi_coul =[] #position du roi dont on désire savoir s'il est en echec

		for i in self.cases:
			if i.piece:
				if str(i.piece) == rois[couleur]:
					ind_case_roi_coul = i.index
		for k in self.cases:
			if k.piece:
				if k.piece.couleur != couleur:
					if k.piece.bouger(ind_case_roi_coul[0],ind_case_roi_coul[1],bouge = False):
						return [True,"Attention, echec au roi {}".format(couleur)]
		return [False,""]


	def cases_couvrables(self,couleur):
		"""
		Donne la liste des cases que peut atteindre un joueur d'une couleur 
		(liste des coups possibles)
		"""


		cases_couvertes = {}
		for i in range(1,9):
			for j in range(1,9):
				for p in self.cases:
					if p.piece != None:
						if p.piece.couleur == couleur:
							if p.piece.bouger(i,j,bouge = False):
								num = self.coord_num([i,j])
								if num in cases_couvertes:
									cases_couvertes[num].append(p.piece.pos)
								else:
									cases_couvertes[num] = [p.piece.pos]
				
		return cases_couvertes


	def echec_mat2(self,couleur):
		"""
		renvoie True s'il ya echec et mat et false sinon
		"""

		if self.echec(couleur)[0]:
			t1 = t.time()
			if couleur == "blanc":
				for i in self.cases_couvrables_blanche:
					for j in cases_couvrables_blanche[i]:
						ech_temp_mat = deepcopy(self)
						ech_temp_mat.cases[self.coord_num(j)].piece.bouger(self.num_coord(i)[1],self.num_coord(i)[0])
						case = self.coord_num(j) 
						case_cible = [self.num_coord(i)[1],self.num_coord(i)[0]]
						case_cible = ech_temp_mat.coord_num(case_cible)
						ech_temp_mat.cases[case_cible].piece = ech_temp_mat.cases[case].piece
						ech_temp_mat.cases[case].piece = None			
						
						if not ech_temp_mat.echec("blanc")[0]:
							return False
						else:
							ech_temp_mat = deepcopy(self)
				print(t.time()-t1)
				
				return True
			
			elif couleur == "noir":
				for i in self.cases_couvrables_noir:
					for j in self.cases_couvrables_noir[i]:						
						ech_temp_mat = deepcopy(self)
						ech_temp_mat.cases[self.coord_num(j)].piece.bouger(self.num_coord(i)[1],self.num_coord(i)[0])
						case = self.coord_num(j) 
						case_cible = [self.num_coord(i)[1],self.num_coord(i)[0]]
						case_cible = ech_temp_mat.coord_num(case_cible)
						ech_temp_mat.cases[case_cible].piece = ech_temp_mat.cases[case].piece
						ech_temp_mat.cases[case].piece = None						
						if not ech_temp_mat.echec("noir")[0]:
							return False
						else:
							ech_temp_mat = deepcopy(self)
				print(t.time()-t1)
				
				return True


	def un_tour(self,couleur,x1,y1,x2,y2):
		
		"""
		Fonction gérant un tour de jeu
		Demande quelle pièce on veut bouger vérifie que l'on a bien choisi une piece et pas une case vide
		puis que la pièce est de la bonne couleur puis enfin si la piece est bougeable ou non, 
		si ttes ces coditions sont remplies, ont demandes à l'utilisateur de renseigner la case ou il désire
		bouger la pièce

		"""

		couleur_piece = {"blanc":"blanche","noir":"noire"}
		couleur_opposee = {"blanc":"noir","noir":"blanc"}

		ech_temp = deepcopy(self)
		# verif_mvtposs = False #Vérifie que la piece choisie peut bouger commme indiqué
		# verif_echec = False #Vérifie que le mvt ne va pas nous mettre en échec
		# verif_piece_coul = False #Vérifie que la pièce choisie est de la couleur du joueur
		# verif_piece = False #Vérifie que la pièce choisie est bien une pièce
		# verif_piece_peut =False #Vérifie que la pièce peut bouger
		
		
		#on vérifie que le mvt rentré est valide
		# case = self.entrez_coord("choisissez une pièce : ")
		# case = self.case_num(case)
		case = self.coord_num([x1,y1])
		# erreur = False
		if self.cases[case].piece == None:
			# print("Vous avez choisi une case vide, choisissez une pièce")
			return False


		if not self.cases[case].piece.couleur == couleur:
			# print("Vous avez choisi une pièce de la mauvaise couleur, choisissez une pièce {}".format(couleur_piece[couleur]))
			return False
	

		if not self.cases[case].piece.bougeable():
			# print("Vous avez choisi une pièce qui ne peut pas bouger, choisissez une autre pièce")
			return False

	
		case_cible = [x2,y2]

		if not ech_temp.cases[case].piece.bouger(case_cible[0],case_cible[1]) :
			# print("mvt non valide")
			return False

		else:
			ech_temp.cases[case].piece.bouger(case_cible[0],case_cible[1])
			case_cible_copy = case_cible
			case_cible = ech_temp.coord_num(case_cible)
			ech_temp.cases[case_cible].piece = ech_temp.cases[case].piece
			ech_temp.cases[case].piece = None
			verif_mvtposs = True

	
		if ech_temp.echec(couleur)[0] :
			# print("mvt non valide, il vous laisse en echec")
			verif_mvtposs = False
			ech_temp = deepcopy(self)
			return False


		


		roque = self.cases[case].piece.bouger(case_cible_copy[0],case_cible_copy[1])
		
		case_cible_copy = self.coord_num(case_cible_copy)
		if roque == "Grand roque":
			self.cases[case_cible_copy].piece = self.cases[case].piece
			self.cases[case].piece = None
			self.cases[case_cible_copy-2].piece.pos = [self.num_coord(case_cible_copy)[1],self.num_coord(case_cible_copy)[0]+1]
			self.cases[case_cible_copy+1].piece = self.cases[case_cible_copy-2].piece
			self.cases[case_cible_copy-2].piece = None
			self.ecrire_pts()
			self.cases_couvrables_blanche = self.cases_couvrables("blanc")
			self.cases_couvrables_noir = self.cases_couvrables("noir")
			# print("{}{}".format(self.num_case(case),self.num_case(case_cible_copy)))
			self.coup_joues.append("{}{}".format(self.num_case(case),self.num_case(case)))
			return "Grand roque"
		
		elif roque == "Petit roque":
			self.cases[case_cible_copy].piece = self.cases[case].piece
			self.cases[case].piece = None
			self.cases[case_cible_copy+1].piece.pos = [self.num_coord(case_cible_copy)[1],self.num_coord(case_cible_copy)[0]-1]
			self.cases[case_cible_copy-1].piece = self.cases[case_cible_copy+1].piece
			self.cases[case_cible_copy+1].piece = None
			self.ecrire_pts()
			self.cases_couvrables_blanche = self.cases_couvrables("blanc")
			self.cases_couvrables_noir = self.cases_couvrables("noir")
			# print("{}{}".format(self.num_case(case),self.num_case(case_cible_copy)))
			self.coup_joues.append("{}{}".format(self.num_case(case),self.num_case(case)))
			return "Petit roque"

		if self.cases[case_cible_copy].piece != None:
			self.piece_prises[couleur].append(str(self.cases[case_cible_copy].piece))
		self.cases[case_cible_copy].piece = self.cases[case].piece
		self.cases[case].piece = None
		# print("{}{}".format(self.num_case(case),self.num_case(case_cible_copy)))
		self.coup_joues.append("{}{}".format(self.num_case(case),self.num_case(case_cible)))
		self.ecrire_pts()
		self.cases_couvrables_blanche = self.cases_couvrables("blanc")
		self.cases_couvrables_noir = self.cases_couvrables("noir")
		return True
		
			
		
	def test_valide(self,x_piece,y_piece,couleur,x_arrive,y_arrive):
		pass

	def le_jeu(self):
		ca_joue = True
		i = 0
		while ca_joue:
			if i%2 == 0:
				self.tour_couleur = "blanc"
				ca_joue = self.un_tour("blanc")
			else:
				self.tour_couleur = "noir"
				ca_joue = self.un_tour("noir")
			i += 1
	

if __name__ == "__main__":
	A = Echiquier()
	A.le_jeu()

