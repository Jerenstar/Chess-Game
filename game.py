	
from echiquier import *
from PIL import ImageTk,Image



class Menu:
	def __init__(self):
		self.win = Tk()
		self.win.geometry("200x150+650+300")
		self.buton_start = Button(self.win, text = "lancer la partie",command = self.lancer_game,width = 20,height = 2)
		self.buton_start.pack(pady = 10)
		self.buton_quitter = Button(self.win, text = "Quitter",command = self.win.destroy,width = 20,height = 2)
		self.buton_quitter.pack(pady = 10)
		self.win.mainloop()
	
	def lancer_game(self):
		echiquier = Echiquier()
		game = Game(echiquier,self.win)
		self.win.withdraw()

class Game:

	def __init__(self,echiquier,wind):
		self.root = wind	
		self.master = Toplevel(wind) #Fenetre principale
		self.master.protocol("WM_DELETE_WINDOW",wind.destroy)
		self.master.configure(bg ="white")
		self.master.title("Le super jeu d'échecs !")
		self.master.resizable() #Non redimensionable
		self.master.geometry("1400x900+350+100")

		self.largeur_cnv = 800
		self.cnv = Canvas(self.master,width =self.largeur_cnv, height = self.largeur_cnv,highlightthickness=3, highlightbackground="black", relief='solid') # Widget Canvas (zone graphique)
		self.cnv.grid(row = 0,column=1,rowspan=8,columnspan=8,padx= 0) # On charge le Canvas dans la fenetre

		self.partie_finie = False

		self.echiquier = echiquier
		

		self.dessiner_grille(self.cnv)
		
		self.dic_piece = {}
		self.dessiner_pieces(self.cnv)
		
		
		self.selected = None

		self.i = -1
		self.tour = {-1:"blanc",1:"noir"}
		self.text_tour = StringVar()
		self.text_tour.set('Tour des {}s'.format(self.tour[self.i]))
		self.text_blanc = StringVar()
		self.text_noir = StringVar()
		self.text_blanc.set(self.echiquier.msg_blanc)
		self.text_noir.set(self.echiquier.msg_noir)

		self.afficher_text_blanc = Label(master=self.master,textvariable=self.text_blanc,font = (("Arial"),20),bg = "white")
		self.afficher_text_blanc.grid(column=9,row = 5,rowspan = 2,sticky = "w",padx = 40)
		self.afficher_text_noir = Label(master=self.master,textvariable=self.text_noir,font = (("Arial"),20),bg = "white")
		self.afficher_text_noir.grid(column=9,row = 1,rowspan = 2,sticky = "w",padx = 40)
		self.afficher_tour = Label(master=self.master,textvariable=self.text_tour,font = (("Arial"),30),bg ="white")
		self.afficher_tour.grid(column=9,row = 3,rowspan =  2 ,sticky = "w",padx = 40)

		self.un =  Label(master=self.master,text="1",font = (("Arial"),20),bg = "white")
		self.un.grid(column=0,row =7,padx = 5 , sticky = "e")
		
		self.deux =  Label(master=self.master,text="2",font = (("Arial"),20),bg = "white")
		self.deux.grid(column=0,row =6,padx = 5 , sticky = "e")
		
		self.trois =  Label(master=self.master,text="3",font = (("Arial"),20),bg = "white")
		self.trois.grid(column=0,row =5,padx = 5 , sticky = "e")
		
		self.quatre =  Label(master=self.master,text="4",font = (("Arial"),20),bg = "white")
		self.quatre.grid(column=0,row =4,padx = 5 , sticky = "e")
		
		self.cinq =  Label(master=self.master,text="5",font = (("Arial"),20),bg = "white")
		self.cinq.grid(column=0,row =3,padx = 5 , sticky = "e")
		
		self.six =  Label(master=self.master,text="6",font = (("Arial"),20),bg = "white")
		self.six.grid(column=0,row =2,padx = 5 , sticky = "e")
		
		self.sept =  Label(master=self.master,text="7",font = (("Arial"),20),bg = "white")
		self.sept.grid(column=0,row =1,padx = 5 , sticky = "e")
		
		self.huit =  Label(master=self.master,text="8",font = (("Arial"),20),bg = "white")
		self.huit.grid(column=0,row =0,padx = 5 , sticky = "e")

		self.a =  Label(master=self.master,text="a",font = (("Arial"),20),bg = "white")
		self.a.grid(column=1,row =8)
		
		self.b =  Label(master=self.master,text="b",font = (("Arial"),20),bg = "white")
		self.b.grid(column=2,row =8)
		
		self.c =  Label(master=self.master,text="c",font = (("Arial"),20),bg = "white")
		self.c.grid(column=3,row =8)
		
		self.d =  Label(master=self.master,text="d",font = (("Arial"),20),bg = "white")
		self.d.grid(column=4,row =8)
		
		self.e =  Label(master=self.master,text="e",font = (("Arial"),20),bg = "white")
		self.e.grid(column=5,row =8)
		
		self.f =  Label(master=self.master,text="f",font = (("Arial"),20),bg = "white")
		self.f.grid(column=6,row =8)
		
		self.g =  Label(master=self.master,text="g",font = (("Arial"),20),bg = "white")
		self.g.grid(column=7,row =8)
		
		self.h =  Label(master=self.master,text="h",font = (("Arial"),20),bg = "white")
		self.h.grid(column=8,row =8)
		
		


	def dessiner_grille(self,canvas):
		for i in range(8):
			for j in range(8):
				taille_case = self.largeur_cnv//8
				sommet_1 = ((i*taille_case,j*taille_case)) 
				sommet_2 = (i*taille_case+taille_case,j*taille_case+taille_case)
				
				if (i+j)%2 == 0:
					canvas.create_rectangle(sommet_1,sommet_2,fill = "#EBFFFE")
				else:
					canvas.create_rectangle(sommet_1,sommet_2,fill = "#488B90")
		
	def dessiner_pieces(self,canvas,id_ = -1 ):
		if id_ <0:
			for i in self.echiquier.cases:
				if i.piece :
					
					index_piece = i.piece.pos
					longueur_case = self.largeur_cnv//8
					x_piece = (index_piece[1]-1)*longueur_case + longueur_case//2
					y_piece = (8 - index_piece[0])*longueur_case  + longueur_case//2
					coord = (x_piece,y_piece)
					
					image = ImageTk.PhotoImage(i.piece.img,master = self.master)
					
					id_image = canvas.create_image(coord,image=image)
					i.piece.id = id_image
					self.dic_piece[id_image] = [i.piece,image]
					self.cnv.tag_bind(id_image, '<ButtonPress-1>', self.start_move) 
					self.cnv.tag_bind(id_image, '<B1-Motion>', self.move)
					self.cnv.tag_bind(id_image, '<ButtonRelease-1>', self.stop_move)
		else:

			piece = self.dic_piece[id_][0]
			index_piece = piece.pos
			for k in self.dic_piece:
				if self.dic_piece[k][0].pos == index_piece:
					self.cnv.delete(k)
			longueur_case = self.largeur_cnv//8
			x_piece = (index_piece[1]-1)*longueur_case + longueur_case//2
			y_piece = (8 - index_piece[0])*longueur_case  + longueur_case//2
			coord = (x_piece,y_piece)
			image = ImageTk.PhotoImage(piece.img,master = self.master)
			id_image = canvas.create_image(coord,image=image)
			piece.id = id_image
			self.dic_piece[id_image] = [piece,image]
			self.cnv.delete(id_)
			self.cnv.tag_bind(id_image, '<ButtonPress-1>', self.start_move) 
			self.cnv.tag_bind(id_image, '<B1-Motion>', self.move)
			self.cnv.tag_bind(id_image, '<ButtonRelease-1>', self.stop_move)
			
	def start_move(self, event):
		# find all clicked items
		self.selected = self.cnv.find_closest(event.x,event.y)# get first selected item
		self.coord_base_selec = ((event.x//100)*100+50,(event.y//100)*100+50)
		self.selected = self.selected[0]


	def move(self, event):
		# move selected item

		self.cnv.coords(self.selected,event.x,event.y)

	def stop_move(self, event):
		# delete or release selected item
		try:
			x1,y1 = self.dic_piece[self.selected][0].pos
			x,y = self.cnv.coords(self.selected)
			x2 = int(8-y//100)
			y2 = int(x//100+1)
			coul = self.tour[self.i]
			mvt_possible = self.echiquier.un_tour(coul,x1,y1,x2,y2)
			
			if mvt_possible:
				if mvt_possible == "Grand roque":
					
					self.dessiner_pieces(self.cnv,id_ = self.selected)
					self.dessiner_pieces(self.cnv,id_ = self.selected-4)
				
				elif mvt_possible == "Petit roque":
					self.dessiner_pieces(self.cnv,id_ = self.selected)
					self.dessiner_pieces(self.cnv,id_ = self.selected+3)

				else:
					self.dessiner_pieces(self.cnv,id_ = self.selected)

				
				
				self.dic_piece[self.selected][0].pos = [x2,y2]
				self.i = -self.i
				
				self.text_tour.set('Tour des {}s'.format(self.tour[self.i]))
				self.text_blanc.set(self.echiquier.msg_blanc)
				self.text_noir.set(self.echiquier.msg_noir)



				if self.echiquier.echec_mat2(self.tour[self.i]):
					self.partie_finie = True
					self.text_tour.set('Victoire des {}s'.format(self.tour[-self.i]))
					self.fin_de_partie()
			else:
				self.cnv.coords(self.selected,self.coord_base_selec)
			
			self.selected = None
			
		except :
			pass
	
	
	def fin_de_partie(self):
		self.m_fin = Menu_fin(self.root,self.master)

	def IA_PLAY(self):
		if self.i == 1:
			self.dessiner_pieces(self.cnv,id_ = self.IA.jouer_le_premier_coup())
			self.i = -self.i	
			self.text_tour.set('Tour des {}s'.format(self.tour[self.i]))
			self.text_blanc.set(self.echiquier.msg_blanc)
			self.text_noir.set(self.echiquier.msg_noir)
			self.echiquier.cases_couvrables_noir = self.echiquier.cases_couvrables("noir")
		self.master.after(1000,self.IA_PLAY)


	def update_couv(self):
		self.echiquier.cases_couvrables_blanche = self.echiquier.cases_couvrables("blanc")
		self.echiquier.cases_couvrables_noir = self.echiquier.cases_couvrables("noir")
		self.master.after(3000,self.update_couv)

class Menu_fin:
	def __init__(self,root,wingame):
		self.wingame = wingame
		self.root = root
		self.win_end = Toplevel(self.root)
		self.win_end.geometry("200x150+650+300")
		self.win_end.grab_set()
		self.win_end.focus_set()
		self.buton_start = Button(self.win_end, text = "rejouer",command = self.relancer,width = 20,height = 2)
		self.buton_start.pack(pady = 10)
		self.win_end.protocol("WM_DELETE_WINDOW",self.root.destroy)

	def relancer(self):
		self.wingame.withdraw()
		echiquier = Echiquier()
		game = Game(echiquier,self.root)
		self.win_end.destroy()
if __name__ == "__main__":
	Menu()