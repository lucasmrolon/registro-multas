from tkinter import *
from tkinter import ttk
from dbManager import * 
from tkintertable import TableCanvas, TableModel
import datetime
from PIL import Image,ImageTk
from vehiculo import *
import os, sys

#PANEL DE PESTAÑAS PARA TRABAJAR CON VEHÍCULOS
class VehiclesNotebook(ttk.Notebook):
	def __init__(self,principalNotebook):

		#CARACTERÍSTICAS DE VENTANA
		width=principalNotebook.cget("width")*3/4
		height=principalNotebook.cget("height")
		super().__init__(principalNotebook,width=int(width),height=int(height)-105)

		#CREA INICIALMENTE PESTAÑA DE TABLA DE VEHÍCULOS
		self.container=principalNotebook
		self.vehiclesTab = VehiclesTab(self)
		self.add(self.vehiclesTab,text="Lista")

		#BANDERAS DE PESTAÑAS ABIERTAS
		self.addVehicleFlag=0
		self.modifyVehicleFlag=0
		self.deleteVehicleFlag=0
		
		#PESTAÑAS POSIBLES
		self.addVehicleTab=None
		self.modifyVehicleTab=None

	#CREAR PANEL DE REGISTRO DE VEHÍCULO
	def createAddVehicleTab(self):
		#ANTES DE CREAR VERIFICA QUE YA NO ESTÉ ABIERTA
		if(self.addVehicleFlag==0):
			self.addVehicleTab = AddVehicleTab(self)
			self.add(self.addVehicleTab,text="Registrar Vehículo")
			self.addVehicleFlag=1
		self.select(self.addVehicleTab)

	#CREAR PANEL DE MODIFICACIÓN DE REGISTRO
	def createModifyVehicleTab(self):
		#ANTES DE CREAR VERIFICA QUE YA NO ESTÉ ABIERTA
		if(self.modifyVehicleFlag==0):
			self.modifyVehicleTab = ModifyVehicleTab(self,self.vehiclesTab.getSelectedRow())
			self.add(self.modifyVehicleTab,text="Modificar Vehículo")
			self.modifyVehicleFlag=1
		self.select(self.modifyVehicleTab)

	#VENTANA DE ELIMINACIÓN DE REGISTRO
	def createDeleteVehicleToplevel(self):
		if(self.deleteVehicleFlag==0):
			self.deleteVehicleFlag=1
			DeleteVehicleToplevel(self,self.vehiclesTab.getSelectedRow())

#PESTAÑA QUE MUESTRA LOS VEHÍCULOS REGISTRADOS
class VehiclesTab(Frame):

	def __init__(self,notebook):

		super().__init__(notebook,bg="#%02x%02x%02x" % (166,185,180),highlightthickness=1,highlightbackground="black")

		#TÍTULO DE LA PESTAÑA
		Label(self,text="LISTA DE VEHÍCULOS REGISTRADOS",font=("Verdana",16,"bold"),bg="#%02x%02x%02x" % (166,185,180)).place(relx="0.05",rely="0.05")

		#CREA TABLA DE VEHÍCULOS
		self.tableFrame = Frame(self)
		self.model=TableModel()
		self.model.addColumn(colname="DOMINIO")
		self.model.columnwidths["DOMINIO"]=90
		self.model.addColumn(colname="TITULAR")
		self.model.columnwidths["TITULAR"]=90
		self.model.addColumn(colname="TIPO")
		self.model.addColumn(colname="MARCA")
		self.model.addColumn(colname="MODELO")
		self.model.columnwidths["MODELO"]=90
		self.model.addColumn(colname="AÑO")
		self.model.columnwidths["AÑO"]=75
		self.model.addColumn(colname="VIN")
		self.model.columnwidths["VIN"]=200
		self.vehiclesTable = TableCanvas(self.tableFrame,model=self.model,width=790,thefont=("Arial",10),read_only=True)
		self.vehiclesTable.show()
		self.tableFrame.place(relx="0.10",rely="0.15")
		self.showVehicles()

		#BOTÓN PARA CERRAR LAS PESTAÑAS DE VEHÍCULO
		Button(self,text="Cerrar Menú",font=("Verdana",12),
			command=lambda:self.close(notebook)).place(relx="0.85",rely="0.05")

		#BOTÓN PARA AÑADIR REGISTRO
		Button(self,text='AÑADIR REGISTRO',width=20,font=("Verdana",14),
			command=lambda:notebook.createAddVehicleTab()).place(
			relx=0.1,rely=0.7)

		#BOTÓN PARA MODIFICAR REGISTRO
		Button(self,text='MODIFICAR REGISTRO',width=20,font=("Verdana",14),
			command=lambda:notebook.createModifyVehicleTab()).place(
			relx=0.39,rely=0.7)

		#BOTÓN PARA ELIMINAR REGISTRO
		Button(self,text='ELIMINAR REGISTRO',width=20,font=("Verdana",14),
			command=lambda:notebook.createDeleteVehicleToplevel()).place(relx=0.68,rely=0.7)

	#FUNCIÓN PARA CARGAR LA TABLE DE VEHÍCULOS
	def showVehicles(self):
		vehicles=DBManager().getAllVehicles()
		self.model.deleteRows()
		dataModel={}
		for vehicle in vehicles:
			dataModel[vehicle[0]]={'DOMINIO':vehicle[0],
				'TITULAR':vehicle[6],
				'TIPO':vehicle[1],
				'MARCA':vehicle[2],
				'MODELO':vehicle[3],
				'AÑO':str(vehicle[4]),
				'VIN':vehicle[5]}
		self.model.importDict(dataModel)
		self.vehiclesTable.redraw()
		#self.vehiclesTable.adjustColumnWidths()

	#DEVUELVE LA FILA SELECCIONADA
	def getSelectedRow(self):
		return(self.vehiclesTable.get_currentRecord())

	#CIERRA EL PANEL ACTUAL Y REALIZA LOS CAMBIOS CORRESPONDIENTES. 
	#PARA CERRAR EL PANEL, LOS PANELES DE CREACIÓN, MODIFICACIÓN Y ELIMINACIÓN DEBEN ESTAR CERRADOS
	def close(self,notebook):
		if notebook.addVehicleFlag==0 and notebook.modifyVehicleFlag==0 and notebook.deleteVehicleFlag==0:
			notebook.container.vehiclesFlag=0
			notebook.container.principalFrame.searchBox["state"]="normal"
			notebook.container.principalFrame.search()
			notebook.destroy()
		else:
			messagebox.showwarning("Advertencia","Para poder cerrar el menú no debe haber ninguna pestaña abierta")

#PESTAÑA DE REGISTRO DE VEHÍCULO
class AddVehicleTab(Frame):
	def __init__(self,frame):
		
		#CARACTERÍSTICAS DE PESTAÑA
		bgcolor="#%02x%02x%02x" % (166,185,180)
		super().__init__(frame,bg=bgcolor,highlightthickness=1,highlightbackground="black")
		self.container=frame
		font=("Verdana",12)

		#VARIABLES A UTILIZAR
		self.domain=StringVar()
		self.domain.trace("w",lambda x,y,z:self.domain.set(self.domain.get().upper()))
		self.kind=StringVar()
		self.dni=StringVar()
		self.brand=StringVar()
		self.model=StringVar()
		self.year=StringVar()
		self.vin=StringVar()	
		self.vin.trace("w",lambda x,y,z:self.vin.set(self.vin.get().upper()))

		#MENSAJE INFORMATIVO		
		Label(self,bg=bgcolor,text="Ingrese datos del vehículo:",font=("Arial",18,"italic")).place(
			relx=0.10,rely=0.08)

		#PANEL PARA INGRESAR DATOS DE VEHÍCULO
		dataVehicle=Frame(self,bg=bgcolor)
		dataVehicle.place(relx=0.15,rely=0.15)

		Label(dataVehicle,text="Dominio",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=1,column=1,pady=15)
		Label(dataVehicle,text="Tipo",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=2,column=1,pady=15)
		Label(dataVehicle,text="DNI Titular",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=3,column=1,pady=15)
		Label(dataVehicle,text="Marca",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=4,column=1,pady=15)
		Label(dataVehicle,text="Modelo",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=5,column=1,pady=15)
		Label(dataVehicle,text="Año",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=6,column=1,pady=15)
		Label(dataVehicle,text="VIN",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=7,column=1,pady=15)

		#CUADRO DE TEXTO DE DOMINIO Y SU CORRESPONDIENTE MENSAJE DE ERROR
		self.domainBox=Entry(dataVehicle,textvariable=self.domain,font=font,highlightbackground="red",justify="center",width=18)
		self.domainBox.grid(row=1,column=2,padx=20)
		self.errorDomainLabel=Label(dataVehicle,text="El dominio ingresado tiene un formato incorrecto",fg="red")

		#SELECCIÓN DE TIPO DE VEHÍCULO
		kindBox=ttk.Combobox(dataVehicle,textvariable=self.kind,state="readonly",font=font,justify="center",width=16)
		kindBox["values"]=["CICLOMOTOR","AUTOMÓVIL","CAMIONETA","CAMIÓN","OTROS"]
		kindBox.current(1)
		kindBox.bind("<<ComboboxSelected>>", lambda x:self.obtainBrands())
		kindBox.grid(row=2,column=2,padx=20)

		#CUADRO DE TEXTO DE DNI Y SU CORRESPONDIENTE MENSAJE DE ERROR
		self.dniBox=Entry(dataVehicle,textvariable=self.dni,font=font,highlightbackground="red",justify="center",width=18)
		self.dniBox.grid(row=3,column=2,padx=20)
		self.dniBox.bind('<FocusOut>',lambda x:self.evaluateDni())
		self.errorDniLabel=Label(dataVehicle,text="El titular no se encuentra registrado en la base de datos",fg="red")

		#SELECCIÓN DE MARCA
		self.brandBox=ttk.Combobox(dataVehicle,textvariable=self.brand,state="readonly",font=font,justify="center",width=16)
		self.brandBox.bind("<<ComboboxSelected>>", lambda x:self.getModels())
		self.brandBox.grid(row=4,column=2,padx=20)

		#SELECCIÓN DE MODELO
		self.modelBox=ttk.Combobox(dataVehicle,textvariable=self.model,font=font,justify="center",width=18)
		self.modelBox.grid(row=5,column=2,padx=20)

		self.obtainBrands()
		self.getModels()

		#SELECCIÓN DE AÑO 
		actual_year=datetime.datetime.now().year
		yearBox=Spinbox(dataVehicle,textvariable=self.year,from_=actual_year-50,to=actual_year,font=font,width=5,state="readonly")
		yearBox.grid(row=6,column=2,padx=20)
		
		#CUADRO DE TEXTO DE VIN Y SU CORRESPONDIENTE ERROR
		self.vinBox=Entry(dataVehicle,textvariable=self.vin,font=font,highlightbackground="red",justify="center",width=18)
		self.vinBox.grid(row=7,column=2,padx=20)
		self.errorVinLabel=Label(dataVehicle,text="El VIN ingresado tiene un formato incorrecto",fg="red")

		#MENSAJE DE ERROR EN CASO DE QUE FALTE COMPLETAR CAMPOS
		self.evaluateLabel=Label(self,text="*Falta completar uno o más campos",bg=bgcolor,width=30,fg="red",font=("Verdana",10))

		#BOTÓN PARA REGISTRAR EL VEHÍCULO
		self.saveButton=Button(self,text="GUARDAR DATOS",font=("Arial",14),command=lambda:self.save())
		self.saveButton.place(relx=0.15,rely=0.85)

		#BOTÓN PARA CANCELAR LA ACCIÓN
		Button(self,text="CANCELAR",font=("Arial",14),command=lambda:self.close()).place(relx=0.45,rely=0.85)

	#OBTIENE MARCAS REGISTRADAS EN LA BASE DE DATOS
	def obtainBrands(self):
		self.brandBox["values"]=[]
		brands=DBManager().getBrands(self.kind.get())
		if len(brands) > 0:
			brandsList=[]
			for brand in brands:
				brandsList.append(brand[0])
			self.brandBox["values"]=brandsList
			self.brandBox.current(0)
		else:
			self.brand.set("")
			self.model.set("")
		self.getModels()	

	#OBTIENE MODELOS REGISTRADOS EN LA BASE DE DATOS A PARTIR DE LA MARCA SELECCIONADA Y EL TIPO DE VEHÍCULO
	def getModels(self):
		self.modelBox["values"]=[]
		models=DBManager().getModels(self.brand.get(),self.kind.get())
		if len(models) > 0:
			modelsList=[]
			for model in models:
				modelsList.append(model[0])
			self.modelBox["values"]=modelsList
			self.modelBox.current(0)

	#EVALÚA EL DNI INGRESADO
	def evaluateDni(self):
		if(DBManager().searchDni(self.dni.get())==None):
			self.errorDniLabel.grid(row=3,column=3)
			self.dniBox.configure(highlightthickness=1)
			return False
		else:
			self.errorDniLabel.grid_forget()
			self.dniBox.configure(highlightthickness=0)
			return True

	#EVALÚA EL DOMINIO INGRESADO
	def evaluateDomain(self):
		domain=self.domain.get()

		#FORMATO DE DOMINIO 'AA000AA'
		if domain[0:2].isalpha() and domain[2:5].isdigit() and domain[5:7].isalpha() and len(domain)==7:
			self.errorDomainLabel.grid_forget()
			self.domainBox.configure(highlightthickness=0)
			return True

		#FORMATO DE DOMINIO 'AAA000'
		elif domain[0:3].isalpha() and domain[3:6].isdigit() and len(domain)==6:
			self.errorDomainLabel.grid_forget()
			self.domainBox.configure(highlightthickness=0)
			return True

		#FORMATO DE DOMINIO 'A000AAA' (MOTOS)
		elif domain[0:1].isalpha() and domain[1:4].isdigit() and domain[4:7].isalpha() and len(domain)==7:
			self.errorDomainLabel.grid_forget()
			self.domainBox.configure(highlightthickness=0)
			return True

		#SI NO COINCIDE CON NINGÚN FORMATO, MUESTRA MENSAJE DE ERROR
		else:
			self.errorDomainLabel.grid(row=1,column=3)
			self.domainBox.configure(highlightthickness=1)
			return False

	#EVALÚA EL VIN INGRESADO
	def evaluateVin(self):
		vin=self.vin.get()
		if vin[0:13].isalnum() and vin[13:17].isdigit() and len(vin)==16:
			self.errorVinLabel.grid_forget()
			self.vinBox.configure(highlightthickness=0)
			return True
		#SI EL FORMATO ES INVÁLIDO, MUESTRA MENSAJE DE ERROR
		else:
			self.errorVinLabel.grid(row=7,column=3)
			self.vinBox.configure(highlightthickness=1)
			return False

	#EVALÚA QUE NO EXISTAN CAMPOS EN BLANCO
	def evaluateForm(self):
		if(self.domain.get()!="" and self.brand.get()!="" and self.model.get()!="" and self.vin.get()!=""):
			self.evaluateLabel.place_forget()
			return True
		else:
			self.evaluateLabel.place(relx=0.15,rely=0.81)
			return False

	#REGISTRA EL VEHÍCULO EN LA BASE DE DATOS
	def save(self):

		#EVALÚA LOS CAMPOS
		okDomain=self.evaluateDomain()
		okDni=self.evaluateDni()
		okForm=self.evaluateForm()
		okVin=self.evaluateVin()

		#SI TODO ES CORRECTO, PROCEDE CON ELREGISTRO
		if(okDni and okForm and okDomain and okVin):
			if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la creación del registro?")):
					DBManager().addVehicle(Vehiculo(self.kind.get(),self.domain.get(),self.brand.get(),
						self.model.get(),self.year.get(),self.vin.get(),self.dni.get()))
					self.container.vehiclesTab.showVehicles()
					self.close()
					
	#CIERRA LA PESTAÑA
	def close(self):
		self.container.addVehicleFlag=0
		self.evaluateDomain()
		self.destroy()

#PESTAÑA DE MODIFICACIÓN DE VEHÍCULO
class ModifyVehicleTab(AddVehicleTab):
	def __init__(self,frame,dataVehicle):
		super().__init__(frame)

		#BLOQUEA EL CUADRO DE TEXTO DE DOMINIO PARA QUE NO PUEDA MODIFICARSE
		self.domain.set(dataVehicle["DOMINIO"])
		self.domainBox["state"]="disabled"

		#OBTIENE Y MUESTRA LA INFORMACIÓN DEL VEHÍCULO
		self.kind.set(dataVehicle["TIPO"])
		self.dni.set(dataVehicle["TITULAR"])
		self.brand.set(dataVehicle["MARCA"])
		self.model.set(dataVehicle["MODELO"])
		self.year.set(dataVehicle["AÑO"])
		self.vin.set(dataVehicle["VIN"])

		#MENSAJE PARA APLICAR LOS CAMBIOS
		self.saveButton["text"]="APLICAR CAMBIOS"

	#EVALÚA LOS VALORES INGRESADOS Y REALIZA LOS CAMBIOS EN LA BASE DE DATOS
	def save(self):
		okDomain=self.evaluateDomain()
		okDni=self.evaluateDni()
		okForm=self.evaluateForm()
		okVin=self.evaluateVin()
		if(okDni and okForm and okDomain and okVin):
			if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la modificación del registro?")):
				DBManager().modifyVehicle(Vehiculo(self.kind.get(),self.domain.get(),self.brand.get(),
					self.model.get(),self.year.get(),self.vin.get(),self.dni.get()))
				self.container.vehiclesTab.showVehicles()
				self.close()

	#CIERRA LA PESTAÑA
	def close(self):
		self.container.modifyVehicleFlag=0
		self.destroy()

#VENTANA DE ELIMINACIÓN DE REGISTRO
class DeleteVehicleToplevel(Toplevel):
	def __init__(self,notebook,row):

		#CARACTERÍSTICAS DE VENTANA
		super().__init__(bg="#%02x%02x%02x" % (249,199,162))
		self.notebook=notebook
		width = self.winfo_screenwidth() 
		height = self.winfo_screenheight() 
		size = (500,200)
		x = width/2 - size[0]/2 
		y = height/2 - size[1]/2 
		self.geometry("%dx%d+%d+%d" % (size + (x, y)))
		self.iconbitmap(self.resolver_ruta("pc_icon.ico"))
		self.title("Ventana de eliminación") 

		#ONTIENE DOMINIO DEL VEHÍCULO SELECCIONADO
		self.toDelete=row['DOMINIO']
		
		#MUESTRA VEHÍCULO SELECCIONADO
		Label(self,text="Automóvil seleccionado: Dominio "+self.toDelete,
			font=("Verdana",12)).place(x=100,y=60)

		#IMAGEN DE PAPELERA
		image_bg=PhotoImage(file=self.resolver_ruta('trash.png'))
		imageLabel=Label(self,image=image_bg,bg="#%02x%02x%02x" % (249,199,162))
		imageLabel.image=image_bg
		imageLabel.place(x="30",y="50")

		#BOTÓN PARA ELIMINAR EL REGISTRO
		Button(self,text="ELIMINAR",font=("Verdana",12),bg="#%02x%02x%02x" % (243,129,132),
			command=lambda:self.delete()).place(x=160,y=120)

		#BOTÓN PARA CANCELAR LA ACCIÓN
		Button(self,text="CANCELAR",font=("Verdana",12),
			command=lambda:self.close()).place(x=290,y=120)

		#HACE LA VENTANA NO REDIMENSIONABLE Y MODAL
		self.resizable(False,False)
		self.grab_set()

	#ELIMINA EL REGISTRO DE LA BASE DE DATOS, PREVIA CONFIRMACIÓN DE LA ACCIÓN
	def delete(self):
		if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la eliminación del registro?")):
			DBManager().deleteVehicle(self.toDelete)
			self.notebook.vehiclesTab.showVehicles()
			self.close()

	#CIERRA LA VENTANA
	def close(self):
		self.notebook.deleteVehicleFlag=0
		self.destroy()

	def resolver_ruta(self,ruta_relativa):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, ruta_relativa)
		return os.path.join(os.path.abspath('.'), ruta_relativa)
