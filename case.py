from pieces import *
class Case:

	def __init__(self,i,j,piece = None):
		self.piece = piece
		self.index = [i,j]

	
	def __str__(self):
		if self.piece  == None:
			return "__"
		else:
			return str(self.piece)

if __name__ == "__main__":
	C= Case(1,1)
	p = Pion(1,1,"noir")
	print(C.occuped)
