from tkinter import *
from tkinter import messagebox
from principalFrame import *
from dbManager import *

#CUADRO DE LOGIN
class LoginFrame(Frame):

	def __init__(self,window,xframe,yframe):
		
		#CARACTERÍSITCAS DE VENTANA
		self.window=window
		self.xframe=xframe
		self.yframe=yframe
		super().__init__(self.window,bg="#%02x%02x%02x" % (107,111,228),width=400,height=200,relief="groove",highlightthickness=2,highlightbackground="black")

		#CUADRO DE TEXTO PARA USUARIO
		Label(self,fg="black",text="Usuario:",font=("Verdana",15),bg="#%02x%02x%02x" % (107,111,228),width=10,anchor="e").place(x=30,y=40)
		self.user=StringVar()
		userBox=Entry(self,textvariable=self.user,fg="black",justify="center",font=("Verdana",15),bg="#%02x%02x%02x" % (200,191,231),width=12)
		userBox.place(x=185,y=40)
		userBox.bind('<Return>',lambda x:self.login())

		#CUADRO DE TEXTO PARA CONTRASEÑA
		Label(self,text="Contraseña:",font=("Verdana",15),bg="#%02x%02x%02x" % (107,111,228),width=10,anchor="e").place(x=30,y=100)
		self.password=StringVar()
		passwordBox=Entry(self,textvariable=self.password,justify="center",font=("Verdana",15),bg="#%02x%02x%02x" % (200,191,231),width=12,show="*")
		passwordBox.place(x=185,y=100)
		passwordBox.bind('<Return>',lambda x:self.login())

		#BOTÓN DE INICIO DE SESIÓN
		Button(self,text="Entrar",font=("Verdana",12),bg="white",width=15,command=self.login).place(x=120,y=150)

	#INICIAR SESIÓN
	def login(self):
		#CONSULTA USUARIO Y CONTRASEÑA EN LA BASE DE DATOS
		row=DBManager().login(self.user.get())
		if row!=None and row[0]==self.user.get() and row[1]==self.password.get() :
			#SI ES CORRECTO, ABRE LA VENTANA PRINCIPAL
			PrincipalFrame(self.window,self.xframe,self.yframe,row[0],self).pack()
			self.place_forget()
			self.user.set("")
			self.password.set("")
		else:
			#SI NO, MUESTRA UN MENSAJE DE ERROR
			messagebox.showwarning("Error","El usuario no existe o bien la contraseña introducida no es válida")