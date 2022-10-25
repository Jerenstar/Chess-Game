from echiquier import *
from tkinter import *
from PIL import ImageTk,Image 

class Piece:
	
	def __init__(self,i,j,couleur,echiquier):
		self.pos = [i,j]
		self.couleur = ""
		self.echiquier = echiquier
		self.image_base = Image.open("piece.png").convert("RGBA")
		self.image_base = self.image_base.resize((600,200))
		self.w_im_base,self.h_im_base  = self.image_base.size
		self.img_w = self.w_im_base//6
		self.img_h = self.h_im_base//2
		self.id = 0

	def bouger(self,dl,dc,bouge = True ):
		
		"""
		Prend en entrée les coordonnées ou l'on veut bouger une pièce qui est bougeable
		change la piece de cooordonées si elle est bougeable à la place souhaitée
		l'option bouge a False permet de juste visualiser la faisabilité d'un mvt (vérification d'échec)
		Sinon renvoie False

		"""
		pass
	
	def bougeable(self,echiquier):
		
		"""
		Renvoie True si une pièce peut bouger et False sinon
		(cas d'une piece entourée de pièce de la mme couleur ou autres)
		"""
		pass

	def verif_colonne(self,i_cible):
		
		"""
		Fonction vérifiant la vacuité d'une colonne entre deux points
		pour un mvt de type colonne 

		"""


		if i_cible > self.pos[0]:
			for i in range(int(i_cible-self.pos[0])-1):
				i += 1
				case_verif = self.echiquier.coord_num([self.pos[0] + i , self.pos[1]])
				if self.echiquier.cases[case_verif].piece != None:
					return False
		if i_cible < self.pos[0]:
			for i in range(int(self.pos[0]-i_cible)-1):
				i += 1
				case_verif = self.echiquier.coord_num([self.pos[0] - i , self.pos[1]])
				if self.echiquier.cases[case_verif].piece != None:
					return False
		return True

	def verif_ligne(self,j_cible):
		
		"""
		Fonction vérifiant la vacuité d'une ligne entre deux points
		pour un mvt de type ligne
		"""
		if j_cible > self.pos[1]:
			for i in range(int(j_cible-self.pos[1])-1):
				i += 1
				case_verif = self.echiquier.coord_num([self.pos[0],self.pos[1] + i])
				if self.echiquier.cases[case_verif].piece != None:
					return False
		
		if j_cible < self.pos[1]:
			for i in range(int(self.pos[1]-j_cible)-1):
				i += 1
				case_verif = self.echiquier.coord_num([self.pos[0],self.pos[1] - i])
				if self.echiquier.cases[case_verif].piece != None:
					return False
		return True

	def verif_case_vide(self,i,j):
		
		"""
		Fonction servant à vérifier la vacuité d'une case
		pour le mvt des pions
		renvoie True si vide False sinon 
		
		"""
		
		return not (self.echiquier.cases[self.echiquier.coord_num([i,j])].piece)

	def verif_case_occupe_couleur_op(self,i,j):
		
		"""
		Vérifie qu'une case donnée est bien occupée par une pièce de couleur opposée
		pour valider un mvt
		"""
		return self.echiquier.cases[self.echiquier.coord_num([i,j])].piece and  self.echiquier.cases[self.echiquier.coord_num([i,j])].piece.couleur != self.couleur

	def verif_case_occupe_couleur_meme(self,i,j):
		
		"""
		Vérifie qu'une case donnée est pas occupée par une piece de la mme couleur

		"""
		if  i<=0 or i>8 or j<=0 or j>8:
			return True
			
		else:
			return self.echiquier.cases[self.echiquier.coord_num([i,j])].piece and  self.echiquier.cases[self.echiquier.coord_num([i,j])].piece.couleur == self.couleur

	def verif_diag(self,i_cible,j_cible):
		
		"""
		Fonction qui renvoie true si une diagonale entre la position initiale
		et la position cible est vide
		"""
		i = self.pos[0]
		j = self.pos[1]

		if i_cible > i and j_cible > j:
			for k in range(i_cible -i -1):
				k += 1
				case_verif = self.echiquier.coord_num([self.pos[0] + k,self.pos[1] + k])
				if self.echiquier.cases[case_verif].piece != None:
					return False

		if i_cible > i and j_cible < j:
			for k in range(i_cible -i -1):
				k += 1
				case_verif = self.echiquier.coord_num([self.pos[0] + k,self.pos[1] - k])
				if self.echiquier.cases[case_verif].piece != None:
					return False

		if i_cible < i and j_cible > j:
			for k in range(i - i_cible -1):
				k += 1
				case_verif = self.echiquier.coord_num([self.pos[0] - k,self.pos[1] + k])
				if self.echiquier.cases[case_verif].piece != None:
					return False

		if i_cible < i and j_cible < j:
			for k in range(i - i_cible -1):
				k += 1
				case_verif = self.echiquier.coord_num([self.pos[0] - k,self.pos[1] - k])
				if self.echiquier.cases[case_verif].piece != None:
					return False
		return True			






class Pion(Piece):
	
	def __init__(self,i,j,couleur,echiquier):
		Piece.__init__(self,i,j,couleur,echiquier)
		self.couleur = couleur
		self.lettre = "P{}".format(self.couleur[0])
		if self.couleur == "blanc":
			self.img = self.image_base.crop([5*self.img_w,0*self.img_h,6*self.img_w,self.img_h])

		else:
			self.img = self.image_base.crop([5*self.img_w,1*self.img_h,6*self.img_w,2*self.img_h])
	
	def __str__(self):
		return self.lettre	

	def bougeable(self):
		"""
		bougeable si aucune piece devant ou une piece dans la diagonale
		"""
		if self.couleur =="noir":
			return self.verif_case_vide(self.pos[0] - 1,self.pos[1]) or self.verif_case_occupe_couleur_op(self.pos[0]-1,self.pos[1]+1) or  self.verif_case_occupe_couleur_op(self.pos[0]-1,self.pos[1]-1)
		else:
			return self.verif_case_vide(self.pos[0] + 1,self.pos[1]) or self.verif_case_occupe_couleur_op(self.pos[0]+1,self.pos[1]+1) or  self.verif_case_occupe_couleur_op(self.pos[0]+1,self.pos[1]-1)

	def bouger(self,i,j,bouge = True):

		"""
		Les pions bougent différemment s'ils sont blanc ou noir 
		
		TODO : ajouter la prise en passant  et la transformation si on atteint une extrémité

		"""
		
		num_cible = self.echiquier.coord_num([i,j])

		if self.couleur == "blanc":

			if self.pos[0] == 2:
				#un mvt en plu si sur leur première ligne 
				if i - self.pos[0] == 1  :
					#avance de 1 ligne
					if self.verif_case_vide(i,j) and j == self.pos[1]: 
						# et de 0 colone si la case de devant est vide
						if bouge:
							self.pos[0] = i
						return True

					elif (j == self.pos[1]+1 or j == self.pos[1]-1) and self.verif_case_occupe_couleur_op(i,j):
						if bouge:
							self.pos[0] = i
							self.pos[1] = j
						return True
						
				elif i - self.pos[0] == 2 and j == self.pos[1]:
					#possibilité d'avancer de deux puisque première ligne
					if self.verif_case_vide(i,j) and self.verif_colonne(i):
							if bouge:
								self.pos[0] = i 
							return True
				else : 
					return False
			else:
				#meme code que précedemment sans la possibilité d'avancer de deux cases
				if i - self.pos[0] == 1 :
					if j == self.pos[1] and self.verif_case_vide(i,j): 
						if bouge:
							self.pos[0] = i
						return True
					elif j == self.pos[1]+1 or j == self.pos[1]-1:
						if self.verif_case_occupe_couleur_op(i,j):
							if bouge:
								self.pos[0] = i
								self.pos[1] = j
							return True
				else : 
					return False


		elif self.couleur == "noir":
			#code des blancs adaptés au noirs
			if self.pos[0] == 7:
				if self.pos[0] - i == 1 :
					if j == self.pos[1] and self.verif_case_vide(i,j): 
						if bouge:
							self.pos[0] = i
						return True
					elif (j == self.pos[1]+1 or j == self.pos[1]-1) and self.verif_case_occupe_couleur_op(i,j):
						if bouge:
							self.pos[0] = i
							self.pos[1] = j
						return True
				elif self.pos[0] - i == 2 and j == self.pos[1]:
					if self.verif_case_vide(i,j) and self.verif_colonne(i):
						if bouge:
							self.pos[0] = i 
						return True
				else : 
					return False
			else:
				if self.pos[0] - i == 1 :

					if j == self.pos[1] and self.verif_case_vide(i,j): 
						if bouge:
							self.pos[0] = i
						return True
					elif (j == self.pos[1]+1 or j == self.pos[1]-1) and self.verif_case_occupe_couleur_op(i,j):
						if bouge:
							self.pos[0] = i
							self.pos[1] = j
						return True
				else : 
					return False

	
		return False
		
				

					





class Tour(Piece):
	def __init__(self,i,j,couleur,echiquier):
		Piece.__init__(self,i,j,couleur,echiquier)
		self.couleur = couleur
		self.lettre = "T{}".format(self.couleur[0])
		if self.couleur == "blanc":
			self.img = self.image_base.crop([4*self.img_w,0*self.img_h,5*self.img_w,self.img_h])
		else:
			self.img = self.image_base.crop([4*self.img_w,1*self.img_h,5*self.img_w,2*self.img_h])
		self.has_moved = False
	def __str__(self):
		return self.lettre

	def bougeable(self):
		return not (self.verif_case_occupe_couleur_meme(self.pos[0]+1,self.pos[1]) and self.verif_case_occupe_couleur_meme(self.pos[0]-1,self.pos[1]) and
			self.verif_case_occupe_couleur_meme(self.pos[0],self.pos[1]+1) and self.verif_case_occupe_couleur_meme(self.pos[0],self.pos[1]-1))

	def bouger(self,i,j,bouge = True):
		
		if i != self.pos[0] and j != self.pos[1]:
			# vérifie que l'on change seulement de ligne ou seulement de colonne 
			return False
		
		elif i != self.pos[0] and self.verif_colonne(i) and not self.verif_case_occupe_couleur_meme(i,j):
			# changementt de ligne 
			if bouge:
				self.pos[0] = i
				self.has_moved = True
			return True

		elif j != self.pos[1] and self.verif_ligne(j) and not self.verif_case_occupe_couleur_meme(i,j):
			#changement de colonne
			if bouge:
				self.pos[1] = j
				self.has_moved = True
			return True

		return False





class Cavalier(Piece):
	
	def __init__(self,i,j,couleur,echiquier):
		Piece.__init__(self,i,j,couleur,echiquier)
		self.couleur = couleur
		self.lettre = "C{}".format(self.couleur[0])
		if self.couleur == "blanc":
			self.img = self.image_base.crop([3*self.img_w,0*self.img_h,4*self.img_w,self.img_h])
		else:
			self.img = self.image_base.crop([3*self.img_w,1*self.img_h,4*self.img_w,2*self.img_h])
	
	def __str__(self):
		return self.lettre

	def bougeable(self):
		i = self.pos[0]
		j = self.pos[1] 
		return not (self.verif_case_occupe_couleur_meme(i+2,j+1)
			and self.verif_case_occupe_couleur_meme(i+2,j-1)
			and self.verif_case_occupe_couleur_meme(i-2,j+1)
			and self.verif_case_occupe_couleur_meme(i-2,j-1)
			and self.verif_case_occupe_couleur_meme(i+1,j+2)
			and self.verif_case_occupe_couleur_meme(i-1,j+2)
			and self.verif_case_occupe_couleur_meme(i+1,j-2)
			and self.verif_case_occupe_couleur_meme(i-1,j-2))

	def bouger(self,i,j,bouge = True):
		x = self.pos[0]
		y = self.pos[1]
		if i == x + 2 and j == y + 1 and not self.verif_case_occupe_couleur_meme(x+2,y+1):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x + 2 and j == y - 1 and not self.verif_case_occupe_couleur_meme(x+2,y-1):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x - 2 and j == y + 1 and not self.verif_case_occupe_couleur_meme(x-2,y+1):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x - 2 and j == y - 1 and not self.verif_case_occupe_couleur_meme(x-2,y-1):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x + 1 and j == y + 2 and not self.verif_case_occupe_couleur_meme(x+1,y+2):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x - 1 and j == y + 2 and not self.verif_case_occupe_couleur_meme(x-1,y+2):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x + 1 and j == y - 2 and not self.verif_case_occupe_couleur_meme(x+1,y-2):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		elif i == x - 1 and j == y - 2 and not self.verif_case_occupe_couleur_meme(x-1,y-2):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		else:
			return False

class Fou(Piece):
	def __init__(self,i,j,couleur,echiquier):
		Piece.__init__(self,i,j,couleur,echiquier)
		self.couleur = couleur
		self.lettre = "F{}".format(self.couleur[0])
		if self.couleur == "blanc":
			self.img = self.image_base.crop([2*self.img_w,0*self.img_h,3*self.img_w,self.img_h])
		else:
			self.img = self.image_base.crop([2*self.img_w,1*self.img_h,3*self.img_w,2*self.img_h])
	
	def __str__(self):
		return self.lettre

	def bougeable(self):
		i = self.pos[0]
		j = self.pos[1] 
		return not (self.verif_case_occupe_couleur_meme(i+1,j+1)
			and self.verif_case_occupe_couleur_meme(i+1,j-1)
			and self.verif_case_occupe_couleur_meme(i-1,j+1)
			and self.verif_case_occupe_couleur_meme(i-1,j-1))

	def bouger (self,i,j,bouge = True):
		x = self.pos[0]
		y = self.pos[1] 	
		if abs(x-i) == abs(y-j) and self.verif_diag(i,j) and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
			return True
		return False


class Reine(Piece):
	def __init__(self,i,j,couleur,echiquier):
		Piece.__init__(self,i,j,couleur,echiquier)
		self.couleur = couleur
		self.lettre = "Q{}".format(self.couleur[0])
		if self.couleur == "blanc":
			self.img = self.image_base.crop([1*self.img_w,0*self.img_h,2*self.img_w,self.img_h])
		else:
			self.img = self.image_base.crop([1*self.img_w,1*self.img_h,2*self.img_w,2*self.img_h])
	def __str__(self):
		return self.lettre

	def bougeable(self):
		i = self.pos[0]
		j = self.pos[1] 
		return not (self.verif_case_occupe_couleur_meme(i+1,j+1)
			and self.verif_case_occupe_couleur_meme(i+1,j-1)
			and self.verif_case_occupe_couleur_meme(i-1,j+1)
			and self.verif_case_occupe_couleur_meme(i-1,j-1)
			and self.verif_case_occupe_couleur_meme(i,j-1)
			and self.verif_case_occupe_couleur_meme(i,j+1)
			and self.verif_case_occupe_couleur_meme(i-1,j)
			and self.verif_case_occupe_couleur_meme(i+1,j))

	def bouger(self,i,j,bouge = True):
		x = self.pos[0]
		y = self.pos[1] 	
		if abs(x-i) == abs(y-j) and self.verif_diag(i,j) and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j

			return True


		elif i != x and j == y and self.verif_colonne(i) and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
			# changementt de ligne 
				self.pos[0] = i
			return True

		elif j != y and i == x and self.verif_ligne(j) and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
			#changement de colonne
				self.pos[1] = j

			return True

		return False





class Roi(Piece):
	def __init__(self,i,j,couleur,echiquier):
		Piece.__init__(self,i,j,couleur,echiquier)
		self.couleur = couleur
		self.has_moved = False
		self.lettre = "K{}".format(self.couleur[0])
		if self.couleur == "blanc":
			self.img = self.image_base.crop([0,0,self.img_w,self.img_h])
		else:
			self.img = self.image_base.crop([0,self.img_h,self.img_w,2*self.img_h])
        
	
	def __str__(self):
		return self.lettre

	def bougeable(self):
		i = self.pos[0]
		j = self.pos[1] 
		return not (self.verif_case_occupe_couleur_meme(i+1,j+1)
			and self.verif_case_occupe_couleur_meme(i+1,j-1)
			and self.verif_case_occupe_couleur_meme(i-1,j+1)
			and self.verif_case_occupe_couleur_meme(i-1,j-1)
			and self.verif_case_occupe_couleur_meme(i,j-1)
			and self.verif_case_occupe_couleur_meme(i,j+1)
			and self.verif_case_occupe_couleur_meme(i-1,j)
			and self.verif_case_occupe_couleur_meme(i+1,j))

	def bouger(self,i,j,bouge = True):
		x = self.pos[0]
		y = self.pos[1] 	
		if abs(x-i) == abs(y-j) and abs(x-i) == 1 and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
				self.pos[0] = i
				self.pos[1] = j
				self.has_moved = True
			return True


		elif abs(x-i) == 1 and j == y and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
			# changementt de ligne 
				self.pos[0] = i
				self.has_moved = True
			return True

		elif abs(y-j) == 1 and i == x and not self.verif_case_occupe_couleur_meme(i,j):
			if bouge:
			#changement de colonne
				self.pos[1] = j
				self.has_moved = True
			return True
		
		elif y-j == 2 and self.has_moved == False and x == i and not self.echiquier.echec(self.couleur)[0]:
			if str(self.echiquier.cases[self.echiquier.coord_num([x,y-4])])[0] == "T":
				if not self.echiquier.cases[self.echiquier.coord_num([x,y-4])].piece.has_moved and self.verif_ligne(y-4):
					if bouge:
						self.pos[1] = j
						self.pos[0] = i
						return "Grand roque"
		elif j-y == 2 and self.has_moved == False and x == i and not self.echiquier.echec(self.couleur)[0]:
			if str(self.echiquier.cases[self.echiquier.coord_num([x,y+3])])[0] == "T":
				if not self.echiquier.cases[self.echiquier.coord_num([x,y+3])].piece.has_moved and self.verif_ligne(y+3):
					if bouge:
						self.pos[1] = j
						self.pos[0] = i
						return "Petit roque"


if __name__ == "__main__":
	P = Pion(1,1)
	print(P.pos)
