from tkinter import *
from resultSearchFrame import *
import datetime
from threading import Timer
from loginFrame import *

#PANEL PRINCIPAL DE LA APLICACIÓN
class PrincipalFrame(Frame):

	def __init__(self,window,xframe,yframe,user,loginFrame):

		#CARACTERÍSTICAS DEL PANEL
		self.loginFrame=loginFrame
		self.window=window
		self.xframe=xframe
		self.yframe=yframe
		self.months = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
		self.weekday = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
		self.searched_domain=""

		#COLOR DE FONDO
		bgcolor1="#%02x%02x%02x" % (102,119,238)
		bgcolor2="#%02x%02x%02x" % (81,100,236)

		super().__init__(window,bg=bgcolor1,width=xframe,height=yframe)

		#CUADRO DE TÍTULO
		forTitle=Frame(self,bg=bgcolor2,height=80,width=xframe-305)
		Label(forTitle,bg=bgcolor2,width=65,text="SISTEMA MUNICIPAL DE GESTIÓN DE INFRACCIONES",
			font=("Verdana",20,"italic")).place(x=0,y=20)
		forTitle.place(x=0,y=0)

		#CUADRO DE RELOJ
		self.clockLabel=Label(self,bg=bgcolor2,text=self.dateandtime("clock"),font=("Times",14,"italic"),width=30,height=4,highlightthickness=1,highlightbackground="black")
		self.clockLabel.place(x=xframe-305,y=0) 

		Label(self,bg=bgcolor1,text="Ingrese DOMINIO:",font=("Verdana",12)).place(relx=0.02,rely=0.15)

		#VARIABLE PARA EL DOMINIO INGRESADO
		self.sv=StringVar()
		self.searchBox=Entry(self,textvariable=self.sv,font=("Verdana",20),justify="center",width=18)
		self.searchBox.place(relx=0.02,rely=0.2)
		self.searchBox.bind('<Return>',lambda x:self.search())

		self.sv.trace("w",lambda x,y,z:self.sv.set(self.sv.get().upper()))
		Timer(1,lambda:self.clock()).start()

		#INSTANCIA EL PANEL DE PESTAÑAS
		self.tabsFrame=TabsFrame(self)
		self.tabsFrame.place(x=xframe*1/4,y=80)
		
		activebuttoncolor="#%02x%02x%02x" % (131,145,241)

		#BOTÓN DE CREACIÓN DE INFRACCIÓN
		self.addInfractionButton=HoverButton(self,text="AÑADIR INFRACCIÓN",font=("Verdana",16),width=20,
			activebackground=activebuttoncolor,state="disabled",
			command=lambda:self.tabsFrame.createNewInfractionTab(self.searched_domain))
		self.addInfractionButton.place(relx=0.03, rely=0.35)

		#BOTÓN DE ELIMINACIÓN DE INFRACCIÓN
		self.deleteInfractionButton=HoverButton(self,text="QUITAR INFRACCIÓN",font=("Verdana",16),width=20,
			activebackground=activebuttoncolor,state="disabled",
			command=lambda:self.tabsFrame.createDeleteInfractionTab(self.searched_domain,self.tabsFrame.resultSearchTab.getSelectedRow()))
		self.deleteInfractionButton.place(relx=0.03, rely=0.45)

		#BOTÓN DE PAGO DE INFRACCIÓN
		self.paidInfractionButton=HoverButton(self,text="REGISTRAR PAGO",font=("Verdana",16),width=20,
			activebackground=activebuttoncolor,state="disabled",
			command=lambda:self.tabsFrame.createPayInfractionTab(self.searched_domain,self.tabsFrame.resultSearchTab.getSelectedRow()))
		self.paidInfractionButton.place(relx=0.03, rely=0.55)

		#VER LISTA DE VEHÍCULOS
		HoverButton(self,text="VER VEHÍCULOS",font=("Verdana",16),width=20,
			activebackground=activebuttoncolor,
			command=lambda:self.tabsFrame.createVehiclesTab()).place(
			relx=0.03, rely=0.65)

		#VER LISTA DE PERSONAS
		HoverButton(self,text="VER PERSONAS",font=("Verdana",16),width=20,
			activebackground=activebuttoncolor,
			command=lambda:self.tabsFrame.createPersonsTab()).place(
			relx=0.03, rely=0.75)

		#MUESTRA DATOS DE LA SESIÓN INICIADA
		dataUser=Frame(self,bg="#%02x%02x%02x" % (128,238,235),height=27,width=xframe,highlightthickness=1,highlightbackground="black")
		Label(dataUser,bg="#%02x%02x%02x" % (128,238,235),text="Sesión iniciada por el usuario '" + user +"' el " + self.dateandtime("login_time"),
			font=("Arial",8,"bold")).place(x=0,y=3)
		Button(dataUser,text="Cerrar Sesión",font=("Arial",8,"bold"),height=1,
			command=self.logout).place(relx=0.93,y=0)
		dataUser.place(relx=0,y=yframe-27)

	#FUNCIÓN DE BÚSQUEDA DEL DOMINIO INGRESADO
	def search(self):
		self.searched_domain=self.sv.get()
		row=DBManager().getVehicle(self.searched_domain)

		#SI EXISTE, ACTIVA LOS BOTONES DE INFRACCIÓN
		if row!=None:
			self.addInfractionButton["state"]="active"
			self.deleteInfractionButton["state"]="active"
			self.paidInfractionButton["state"]="active"
		#SI NO, LOS DESACTIVA
		else:
			self.addInfractionButton["state"]="disabled"
			self.deleteInfractionButton["state"]="disabled"
			self.paidInfractionButton["state"]="disabled"
		#ENVÍA LOS DATOS PARA MOSTRARLOS EN PANTALLA
		self.tabsFrame.resultSearchTab.showData(row)	

	#FUNCIÓN QUE OBTIENE LOS DATOS DEL RELOJ Y DE INICIO DE SESIÓN
	def dateandtime(self,reason):
		date=datetime.datetime.now()
		if reason=="clock":
			return self.weekday[date.weekday()] + ", " + str(date.day) + " de " + self.months[date.month-1] + " de " + str(date.year) + "\n" + str(date.hour).zfill(2) + " : " + str(date.minute).zfill(2) + " : " + str(date.second).zfill(2)
		elif reason=="login_time":
			return "%02d-%02d-%4d"%(date.day,date.month,date.year)  + " a las " + "%02d:%02d"%(date.hour,date.minute) + " hs."

	#FUNCIÓN QUE CONTROLA EL MOVIMIENTO DEL RELOJ
	def clock(self):
		self.clockLabel.configure(text=self.dateandtime("clock"))
		Timer(1,lambda:self.clock()).start()

	#FUNCIÓN DE CIERRE DE SESIÓN
	def logout(self):
		if(messagebox.askokcancel("Mensaje de confirmación","¿Cerrar Sesión?")):
			self.loginFrame.place(x=self.xframe/2-200,y=self.yframe/2-100)
			self.loginFrame.focus_force()
			self.tabsFrame.destroy()
			self.destroy()
			

#CLASE ESPECIAL PARA OTORGAR COMPORTAMIENTO ESPECIAL A LOS BOTONES
class HoverButton(Button):
	def __init__(self, master, **kw):
		Button.__init__(self,master=master,**kw)
		self.defaultBackground = self["background"]
		self.bind("<Enter>", self.on_enter)
		self.bind("<Leave>", self.on_leave)

	def on_enter(self, e):
		self["background"] = self["activebackground"]

	def on_leave(self, e):
		self["background"] = self.defaultBackground
