from tkinter import *
from tkinter import ttk
from dbManager import * 
from tkintertable import TableCanvas, TableModel
from persona import *
import os, sys

#PANEL DE PESTAÑAS PARA GESTIONAR EL REGISTRO DE PERSONAS
class PersonsNotebook(ttk.Notebook):

	def __init__(self,principalNotebook):

		#CARACTERÍSTICAS DEL PANEL
		width=principalNotebook.cget("width")*3/4
		height=principalNotebook.cget("height")
		super().__init__(principalNotebook,width=int(width),height=int(height)-105)
		self.container=principalNotebook

		#INSTANCIA EL PANEL QUE MUESTRA LA TABLA DE PERSONAS
		self.personsTab = PersonsTab(self)
		self.add(self.personsTab,text="Lista")

		#BANDERAS DE PESTAÑAS ABIERTAS
		self.addPersonFlag=0
		self.modifyPersonFlag=0
		self.deletePersonFlag=0
		
		#PESTAÑAS POSIBLES
		self.addPersonTab=None
		self.modifyPersonTab=None

	#CREAR PESTAÑA DE REGISTRO
	def createAddPersonTab(self):
		if(self.addPersonFlag==0):
			self.addPersonTab = AddPersonTab(self)
			self.add(self.addPersonTab,text="Añadir Persona")
			self.addPersonFlag=1
		self.select(self.addPersonTab)

	#CREAR PESTAÑA DE MODIFICACIÓN DE REGISTRO
	def createModifyPersonTab(self):
		if(self.modifyPersonFlag==0):
			self.modifyPersonTab = ModifyPersonTab(self,self.personsTab.getSelectedRow())
			self.add(self.modifyPersonTab,text="Modificar Persona")
			self.modifyPersonFlag=1
		self.select(self.modifyPersonTab)

	#CREAR VENTANA DE ELIMINACIÓN DE REGISTRO
	def createDeletePersonToplevel(self):
		if(self.deletePersonFlag==0):
			DeletePersonToplevel(self,self.personsTab.getSelectedRow()).mainloop()
			self.deletePersonFlag=1

#PESTAÑA QUE MUESTRA LA TABLA DE PERSONAS REGISTRADAS
class PersonsTab(Frame):

	def __init__(self,notebook):

		#CARACTERÍSTICAS DE LA PESTAÑA
		super().__init__(notebook,bg="#%02x%02x%02x" % (166,185,180),highlightthickness=1,highlightbackground="black")
		width=notebook.cget("width")*3/5
		height=notebook.cget("height")

		#TÍTULO DEL PANEL
		Label(self,text="LISTA DE PERSONAS REGISTRADAS",font=("Verdana",16,"bold"),bg="#%02x%02x%02x" % (166,185,180)).place(relx="0.05",rely="0.05")

		#BOTÓN PARA CERRAR EL PANEL DE PESTAÑAS
		Button(self,text="Cerrar Menú",font=("Verdana",12),
			command=lambda:self.close(notebook)).place(relx="0.85",rely="0.05")

		#CREA LA TABLA DE PERSONAS
		self.tableFrame = Frame(self)
		self.model=TableModel()
		self.model.addColumn(colname="DNI")
		self.model.columnwidths["DNI"]=90
		self.model.addColumn(colname="APELLIDO")
		self.model.columnwidths["APELLIDO"]=90
		self.model.addColumn(colname="NOMBRES")
		self.model.addColumn(colname="FECHA DE NAC.")
		self.model.columnwidths["FECHA DE NAC."]=130
		self.model.addColumn(colname="DOMICILIO")
		self.model.columnwidths["DOMICILIO"]=147
		self.model.addColumn(colname="NACIONALIDAD")
		self.model.columnwidths["NACIONALIDAD"]=120
		self.model.addColumn(colname="CATEGORÍA")
		self.model.columnwidths["CATEGORÍA"]=90
		self.model.addColumn(colname="TIPO SANGRE")
		self.model.columnwidths["TIPO SANGRE"]=110
		self.personsTable = TableCanvas(self.tableFrame,model=self.model,width=900,thefont=("Arial",10),read_only=True)
		self.personsTable.show()
		self.tableFrame.place(relx="0.05",rely="0.15")

		self.showPersons()

		#BOTÓN PARA AÑADIR REGISTRO
		Button(self,text='AÑADIR REGISTRO',width=20,font=("Verdana",14),
			command=lambda:notebook.createAddPersonTab()).place(relx=0.1,rely=0.7)

		#BOTÓN PARA MODIFICAR REGISTRO
		Button(self,text='MODIFICAR REGISTRO',width=20,font=("Verdana",14),
			command=lambda:notebook.createModifyPersonTab()).place(relx=0.4,rely=0.7)

		#BOTÓN PARA ELIMINAR REGISTRO
		Button(self,text='ELIMINAR REGISTRO',width=20,font=("Verdana",14),
			command=lambda:notebook.createDeletePersonToplevel()).place(relx=0.7,rely=0.7)

	#FUNCIÓN PARA OBTENER Y CARGAR LAS PERSONAS REGISTRADAS
	def showPersons(self):
		persons=DBManager().getAllPersons()
		self.model.deleteRows()
		dataModel={}
		for person in persons:
			birthdate="%02d-%02d-%4d"%(person[3].day,person[3].month,person[3].year)
			dataModel[person[0]]={'DNI':person[0],
				'APELLIDO':person[1],
				'NOMBRES':person[2],
				'FECHA DE NAC.':birthdate,
				'DOMICILIO':person[4],
				'NACIONALIDAD':person[5],
				'CATEGORÍA':person[6],
				'TIPO SANGRE':person[7]}
		self.model.importDict(dataModel)
		self.personsTable.redraw()

	#OBTIENE LA FILA SELECCIONADA
	def getSelectedRow(self):
		return(self.personsTable.get_currentRecord())

	#CERRAR LA PESTAÑA Y ACCIONES COMPLEMENTARIAS
	def close(self,notebook):
		if notebook.addPersonFlag==0 and notebook.modifyPersonFlag==0 and notebook.deletePersonFlag==0:
			notebook.container.personsFlag=0
			notebook.container.principalFrame.searchBox["state"]="normal"
			notebook.container.principalFrame.search()
			notebook.destroy()
		else:
			#PARA PODER CERRAR EL PANEL, LAS PESTAÑAS DEBEN ESTAR CERRADAS
			messagebox.showwarning("Advertencia","Para poder cerrar el menú no debe haber ninguna pestaña abierta")

#PESTAÑA DE CREACIÓN DE REGISTRO
class AddPersonTab(Frame):
	def __init__(self,frame):
		
		super().__init__(frame,bg="#%02x%02x%02x" % (146,146,248),highlightthickness=1,highlightbackground="black")
		width=frame.cget("width")
		height=frame.cget("height")
		self.container=frame
		self.frame=frame
		font=("Verdana",12)

		#CREA LAS VARIABLES NECESARIAS
		self.dni=StringVar()
		self.surname=StringVar()
		self.surname.trace("w",lambda x,y,z:self.surname.set(self.surname.get().capitalize()))
		self.name=StringVar()
		self.name.trace("w",lambda x,y,z:self.name.set(self.name.get().title()))
		self.day=IntVar()
		self.month=StringVar()
		self.year=IntVar()
		self.residence=StringVar()
		self.nationality=StringVar()
		self.category=StringVar()
		self.bloodtype=StringVar()	
		
		#MENSAJE INFORMATIVO
		Label(self,bg="#%02x%02x%02x" % (146,146,248),text="Ingrese datos de la persona:",font=("Arial",18,"italic")).place(
			relx=0.10,rely=0.08)

		#PANEL PARA INGRESAR LOS DATOS DE LA PERSONA		
		dataPerson=Frame(self,bg="#%02x%02x%02x" % (146,146,248))
		dataPerson.place(relx=0.05,rely=0.25)

		Label(dataPerson,text="DNI N°",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=1,column=1,pady=15)
		Label(dataPerson,text="Apellido",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=2,column=1,pady=15)
		Label(dataPerson,text="Nombre",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=3,column=1,pady=15)
		Label(dataPerson,text="Fecha de nac.",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=4,column=1,pady=15)
		Label(dataPerson,text="Domicilio",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=1,column=3,pady=15)
		Label(dataPerson,text="Nacionalidad",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=2,column=3,pady=15)
		Label(dataPerson,text="Categoría",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=3,column=3,pady=15)
		Label(dataPerson,text="Tipo de Sangre",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=4,column=3,pady=15)

		#CUADRO DE TEXTO PARA EL DNI
		self.dniBox=Entry(dataPerson,textvariable=self.dni,font=font,highlightbackground="red",justify="center",width=18)
		self.dniBox.grid(row=1,column=2,padx=20)
		self.errorDniLabel=Label(dataPerson,text="DNI inválido",fg="red")

		#CUADRO DE TEXTO DEL APELLIDO
		self.surnameBox=Entry(dataPerson,textvariable=self.surname,font=font,highlightbackground="red",justify="center",width=18)
		self.surnameBox.grid(row=2,column=2,padx=20)

		#CUADRO DE TEXTO DEL NOMBRE
		self.nameBox=Entry(dataPerson,textvariable=self.name,font=font,highlightbackground="red",justify="center",width=18)
		self.nameBox.grid(row=3,column=2,padx=20)

		#PANEL PARA SELECCIONAR FECHA DE NACIMIENTO
		dateGrid=Frame(dataPerson,bg="#%02x%02x%02x" % (146,146,248))
		
		#OBTIENE FECHA ACTUAL
		self.actual_date=datetime.datetime.now()

		#SELECCIÓN DE DÍA
		Label(dateGrid,bg="#%02x%02x%02x" % (146,146,248),text="día",font=("Arial",8)).place(x=20,y=9)
		self.dayBox=ttk.Combobox(dateGrid,textvariable=self.day,state="readonly",font=font,width=3)
		self.dayBox.set(self.actual_date.day)
		self.dayBox.grid(row=1,column=1,columnspan=2,padx=5,pady=25)

		#SELECCIÓN DE MES
		self.meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio",
			"Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
		Label(dateGrid,bg="#%02x%02x%02x" % (146,146,248),text="mes",font=("Arial",8)).place(x=120,y=9)
		monthBox=ttk.Combobox(dateGrid,textvariable=self.month,state="readonly",font=font,width=12)
		monthBox["values"]=self.meses
		monthBox.bind("<<ComboboxSelected>>", lambda x:self.setdays())
		monthBox.current(self.actual_date.month-1)
		monthBox.grid(row=1,column=3,columnspan=2,padx=5,pady=25)
		
		#SELECCIÓN DE AÑO
		Label(dateGrid,bg="#%02x%02x%02x" % (146,146,248),text="año",font=("Arial",8)).place(x=255,y=9)
		yearBox=ttk.Combobox(dateGrid,textvariable=self.year,state="readonly",font=font,width=7)
		initial_year=self.actual_date.year
		for i in range(110):
			yearBox["values"]=list(yearBox["values"])+[str(initial_year - i)]
		yearBox.bind("<<ComboboxSelected>>", lambda x:self.setdays())
		yearBox.set(self.actual_date.year)
		yearBox.grid(row=1,column=5,columnspan=2,padx=5,pady=25)

		dateGrid.grid(row=4,column=2,padx=20)

		self.setdays()

		#CUADRO DE TEXTO DE DOMICILIO
		residenceBox=Entry(dataPerson,textvariable=self.residence,font=font,highlightbackground="red",justify="center",width=18)
		residenceBox.grid(row=1,column=4,padx=20)

		#SELECCIÓN DE NACIONALIDAD
		nationalityBox=ttk.Combobox(dataPerson,textvariable=self.nationality,font=font,state="readonly",justify="center",width=16)
		nationalityBox["values"]=["Argentino","Brasilero","Boliviano","Chileno","Paraguayo","Peruano","Uruguayo"]
		nationalityBox.grid(row=2,column=4,padx=20)

		#SELECCIÓN DE CATEGORÍA
		categoryBox=ttk.Combobox(dataPerson,textvariable=self.category,state="readonly",font=font,justify="center",width=16)
		categoryBox["values"]=["A.1.1","A.1.2","A.1.3","A.1.4","A.2.1","A.2.2","A.3","B.1","B.2","C.1","C.2","C.3","D.1","D.2","D.3","D.4",
		"E.1","E.2","F","G.1","G.2","G.3"]
		categoryBox.grid(row=3,column=4,padx=20)

		#SELECCIÓN DE TIPO DE SANGRE
		bloodtypeBox=ttk.Combobox(dataPerson,textvariable=self.bloodtype,state="readonly",font=font,justify="center",width=16)
		bloodtypeBox["values"]=["A+","B+","0+","AB+","A-","B-","0-","AB-"]
		bloodtypeBox.grid(row=4,column=4,padx=20)

		#MENSAJE DE ERROR SI FALTAN COMPLETAR CAMPOS
		self.evaluateLabel=Label(self,text="*Falta completar uno o más campos",bg="#%02x%02x%02x" % (146,146,248),width=30,fg="red",font=("Verdana",10))

		#BOTÓN PARA REALIZAR EL REGISTRO
		self.saveButton=Button(self,text="GUARDAR DATOS",font=("Arial",14),command=lambda:self.save())
		self.saveButton.place(relx=0.30,rely=0.70)

		#BOTÓN PARA CANCELAR LA ACCIÓN
		Button(self,text="CANCELAR",font=("Arial",14),command=lambda:self.close()).place(relx=0.55,rely=0.70)

	#FUNCIÓN AUXILIAR PARA MODIFICAR DINÁMICAMENTE EL CONTENIDO DE LOS SELECTORES DE FECHA
	def setdays(self):
		month=self.month.get()
		self.dayBox["values"]=[]
		if(month == "Abril" or month == "Junio" or month == "Septiembre" or month == "Noviembre"):
			self.dayBox["values"]=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
			if self.dayBox.get()=="31": 
				self.dayBox.set("30")
		elif(month == "Febrero"):
			if(int(self.year.get())%4==0):
				self.dayBox["values"]=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
				if self.dayBox.get()=="30" or self.day=="31":
					self.dayBox.set("29")
			else:
				self.dayBox["values"]=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
				if self.dayBox.get()=="29" or self.dayBox.get()=="30" or self.dayBox.get()=="31":
					self.dayBox.set("28")
		else:
			self.dayBox["values"]=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

	#EVALÚA QUE NO QUEDEN CAMPOS EN BLANCO
	def evaluateForm(self):
		if(self.dni.get()!="" and self.surname.get()!="" and self.name.get()!="" and self.residence.get()!="" and self.nationality.get()!="" and self.category.get()!="" and self.bloodtype.get()!=""):
			self.evaluateLabel.place_forget()
			return True
		else:
			self.evaluateLabel.place(relx=0.15,rely=0.81)
			return False

	#EVALÚA SI EL DNI TIENE EL FORMATO CORRECTO
	def evaluateDni(self):
		dni=self.dni.get()
		if dni.isdigit():
			self.errorDniLabel.place_forget()
			self.dniBox.configure(highlightthickness=0)
			return True
		else:
			self.errorDniLabel.place(x=300,y=45)
			self.dniBox.configure(highlightthickness=1)
			return False

	#EVALÚA LOS CAMPOS Y REALIZA EL REGISTRO EN LA BASE DE DATOS
	def save(self):
		okForm=self.evaluateForm()
		okDni=self.evaluateDni()
		if(okForm and okDni):
			if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la creación del registro?")):
				datetime_str=("%4d-%02d-%02d"%(self.year.get(),self.meses.index(self.month.get())+1,self.day.get()))
				datetime_obj=datetime.datetime.strptime(datetime_str,'%Y-%m-%d')
				DBManager().addPerson(Person(self.dni.get(),self.surname.get(),self.name.get(),
					datetime_obj,self.residence.get(),self.nationality.get(),self.category.get(),self.bloodtype.get()))
				self.container.personsTab.showPersons()
				self.close()
					
	#CIERRA LA PESTAÑA
	def close(self):
		self.container.addPersonFlag=0
		self.destroy()

#PESTAÑA DE MODIFICACIÓN DE REGISTRO
class ModifyPersonTab(AddPersonTab):
	def __init__(self,frame,dataPerson):
		
		super().__init__(frame)

		#BLOQUEA EL CUADRO DE TEXTO DE DNI
		self.dni.set(dataPerson["DNI"])
		self.dniBox["state"]="disabled"

		#CREA LAS VARIABLES CORRESPONDIENTES
		self.surname.set(dataPerson["APELLIDO"])
		self.name.set(dataPerson["NOMBRES"])

		dateandhour=datetime.datetime.strptime(dataPerson['FECHA DE NAC.'],'%d-%m-%Y')
		self.day.set(dateandhour.day)
		self.month.set(self.meses[dateandhour.month-1])
		self.year.set(dateandhour.year)

		self.residence.set(dataPerson["DOMICILIO"])
		self.nationality.set(dataPerson["NACIONALIDAD"])
		self.category.set(dataPerson["CATEGORÍA"])
		self.bloodtype.set(dataPerson["TIPO SANGRE"])

		#BOTÓN PARA CONFIRMAR LA MODIFICACIÓN
		self.saveButton["text"]="APLICAR CAMBIOS"

	#EVALÚA LOS CAMPOS Y REALIZA LA MODIFICACIÓN EN LA BASE DE DATOS
	def save(self):
		okForm=self.evaluateForm()
		if(okForm):
			if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la modificación del registro?")):
				datetime_str=("%02d-%02d-%4d"%(self.day.get(),self.meses.index(self.month.get())+1,self.year.get()))
				datetime_obj=datetime.datetime.strptime(datetime_str,'%d-%m-%Y')
				DBManager().modifyPerson(Person(self.dni.get(),self.surname.get(),self.name.get(),
					datetime_obj,self.residence.get(),self.nationality.get(),self.category.get(),self.bloodtype.get()))
				self.container.personsTab.showPersons()
				self.close()
					
	#CIERRA LA PESTAÑA
	def close(self):
		self.container.modifyPersonFlag=0
		self.destroy()

#VENTANA DE ELIMINACIÓN DE REGISTRO
class DeletePersonToplevel(Toplevel):
	def __init__(self,notebook,row):

		#CARACTERÍSTICAS DE VENTANA
		super().__init__(bg="#%02x%02x%02x" % (249,199,162))
		width = self.winfo_screenwidth() 
		height = self.winfo_screenheight() 
		size = (700,200)
		x = width/2 - size[0]/2 
		y = height/2 - size[1]/2 
		self.geometry("%dx%d+%d+%d" % (size + (x, y)))
		self.iconbitmap(self.resolver_ruta("pc_icon.ico"))
		self.title("Ventana de eliminación")
		self.notebook=notebook

		#CARGA LOS DATOS DE LA FILA SELECCIONADA
		self.dniToDelete=row['DNI']
		self.surname = row['APELLIDO']
		self.name = row['NOMBRES']

		#MUESTRA LOS DATOS
		Label(self,text="Persona seleccionada: " + self.surname + ", " + self.name + " - DNI N° "+ str(self.dniToDelete),
			font=("Verdana",12)).place(x=100,y=60)

		#CARGA IMAGEN DE PAPELERA
		image_bg=PhotoImage(file=self.resolver_ruta('trash.png'))
		imageLabel=Label(self,image=image_bg,bg="#%02x%02x%02x" % (249,199,162))
		imageLabel.image=image_bg
		imageLabel.place(x="30",y="50")

		#BOTÓN PARA ELIMINAR EL REGISTRO
		Button(self,text="ELIMINAR",font=("Verdana",12),bg="#%02x%02x%02x" % (243,129,132),
			command=lambda:self.delete()).place(x=220,y=120)

		#BOTÓN PARA CANCELAR LA ACCIÓN
		Button(self,text="CANCELAR",font=("Verdana",12),
			command=lambda:self.close()).place(x=350,y=120)

		#ESTABLECE LA VENTANA COMO NO REDIMENSIONABLE Y MODAL
		self.resizable(False,False)
		self.grab_set()

	#REALIZA LA ELIMINACIÓN DEL REGISTRO
	def delete(self):
		if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la eliminación del registro?")):
			DBManager().deletePerson(self.dniToDelete)
			self.notebook.personsTab.showPersons()
			self.close()

	#CIERRA LA VENTANA
	def close(self):
		self.notebook.deletePersonFlag=0
		self.destroy()

	def resolver_ruta(self,ruta_relativa):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, ruta_relativa)
		return os.path.join(os.path.abspath('.'), ruta_relativa)
