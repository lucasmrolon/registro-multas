from tkinter import *
from tkinter import ttk
from dbManager import *
from infractionTabs import *
from vehiclesTabs import *
from personsTabs import *
from tkintertable import TableCanvas, TableModel

#PANEL DE PESTAÑAS
class TabsFrame(ttk.Notebook):
	def __init__(self,principalFrame):

		#CARACTERÍSTICAS DEL PANEL (ANCHO Y ALTO)
		width=principalFrame.cget("width")*3/4
		height=principalFrame.cget("height")
		super().__init__(principalFrame,width=int(width),height=int(height)-105)

		#CARGA INICIALMENTE EL PANEL DE INFRACCIONES DEL DOMINIO INGRESADO
		self.principalFrame=principalFrame
		self.resultSearchTab = ResultSearchTab(self)
		self.add(self.resultSearchTab,text="Infracciones")

		#BANDERAS PARA EVITAR QUE SE CREE DOS PANELES IGUALES
		self.newInfractionFlag=0
		self.deleteInfractionFlag=0
		self.payInfractionFlag=0
		self.vehiclesFlag=0
		self.personsFlag=0

		#PANELES POSIBLES
		self.newInfractionTab='NULL'
		self.deleteInfractionTab='NULL'
		self.payInfractionTab='NULL'
		self.vehiclesTab='NULL'
		self.personsTab='NULL'

		self.pressed_index=None

	#CREAR PANEL DE NUEVA INFRACCIÓN
	def createNewInfractionTab(self,domain):
		#ANTES DE CREAR, VERIFICA QUE YA NO ESTÉ INSTANCIADO
		if(self.newInfractionFlag==0):
			self.newInfractionTab = NewInfractionTab(self,domain)
			self.add(self.newInfractionTab,text="Nueva Infracción")
			self.newInfractionFlag=1
			self.principalFrame.searchBox["state"]="disabled"
		self.select(self.newInfractionTab)

	#CREAR PANEL DE ELIMINAR INFRACCIÓN
	def createDeleteInfractionTab(self,domain,infraction):
		#SI LA INFRACCIÓN SE PAGÓ NO SE PUEDE ELIMINAR
		if(infraction['PAGADO']=='NO'):
			#ANTES DE CREAR, VERIFICA QUE YA NO ESTÉ INSTANCIADO
			if(self.deleteInfractionFlag==0):
				self.deleteInfractionTab = DeleteInfractionTab(self,domain,infraction,"#%02x%02x%02x" % (166,185,180))
				self.add(self.deleteInfractionTab,text="Eliminar Infracción")
				self.deleteInfractionFlag=1
				self.principalFrame.searchBox["state"]="disabled"
			self.select(self.deleteInfractionTab)
		else:
			messagebox.showwarning("Error","No se puede eliminar una infracción que ya fue abonada.")
		
	#CREAR PANEL DE PAGO DE INFRACCIÓN
	def createPayInfractionTab(self,domain,infraction):
		#VERIFICA QUE NO SE HAYA PAGADO CON ANTERIORIDAD
		if(infraction['PAGADO']=='NO'):
			#ANTES DE CREAR, VERIFICA QUE YA NO ESTÉ INSTANCIADO
			if(self.payInfractionFlag==0):
				self.payInfractionTab = PayInfractionTab(self,domain,infraction)
				self.add(self.payInfractionTab,text="Abonar Infracción")
				self.payInfractionFlag=1
				self.principalFrame.searchBox["state"]="disabled"
			self.select(self.payInfractionTab)
		else:
			messagebox.showwarning("Error","La infracción ya fue abonada.")

	#CREAR PANEL DE VEHÍCULOS
	def createVehiclesTab(self):
		#ANTES DE CREAR, VERIFICA QUE YA NO ESTÉ INSTANCIADO
		if(self.vehiclesFlag==0):
			self.vehiclesNotebook = VehiclesNotebook(self)
			self.add(self.vehiclesNotebook,text="Vehículos")
			self.vehiclesFlag=1
			self.principalFrame.searchBox["state"]="disabled"
			self.principalFrame.paidInfractionButton["state"]="disabled"
			self.principalFrame.deleteInfractionButton["state"]="disabled"
			self.principalFrame.addInfractionButton["state"]="disabled"
		self.select(self.vehiclesNotebook)

	#CREAR PANEL DE PERSONAS
	def createPersonsTab(self):
		#ANTES DE CREAR, VERIFICA QUE YA NO ESTÉ INSTANCIADO
		if(self.personsFlag==0):
			self.personsNotebook = PersonsNotebook(self)
			self.add(self.personsNotebook,text="Personas")
			self.personsFlag=1
			self.principalFrame.searchBox["state"]="disabled"
			self.principalFrame.paidInfractionButton["state"]="disabled"
			self.principalFrame.deleteInfractionButton["state"]="disabled"
			self.principalFrame.addInfractionButton["state"]="disabled"
		self.select(self.personsNotebook)

#PANEL QUE MUESTRA LOS RESULTADOS DE LA BÚSQUEDA POR DOMINIO DEL VEHÍCULO
class ResultSearchTab(Frame):

	def __init__(self,frame):

		#CARACTERÍSTICAS DEL PANEL
		width=frame.cget("width")*3/5
		height=frame.cget("height")
		bgcolor1="#%02x%02x%02x" % (157,168,244)
		super().__init__(frame,bg=bgcolor1,highlightthickness=1,highlightbackground="black")

		#TITULO DE VENTANA
		Label(self,text="DATOS DEL VEHÍCULO",font=("Verdana",14,"bold"),bg=bgcolor1).place(relx=0.35,rely=0.04)

		#PANEL DE DATOS DEL VEHÍCULO
		dataVehicle=Frame(self,bg=bgcolor1,width=width,height=100)
		dataVehicle.place(relx=0.02,rely=0.1)
		bgcolor2="#%02x%02x%02x" % (198,204,249)

		Label(dataVehicle,text="Dominio",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=1,column=1)
		Label(dataVehicle,text="Tipo",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=1,column=3)
		Label(dataVehicle,text="N° de Motor",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=1,column=5)
		Label(dataVehicle,text="Marca",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=2,column=1)
		Label(dataVehicle,text="Modelo",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=2,column=3)
		Label(dataVehicle,text="Año",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=2,column=5)
		Label(dataVehicle,text="Titular",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=3,column=1)
		Label(dataVehicle,text="DNI",width=15,bg=bgcolor1,relief="groove",borderwidth=4,
			font=("Verdana",11,"italic")).grid(row=3,column=5)

		#DOMINIO
		self.domainLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=15,bg=bgcolor2)
		self.domainLabel.grid(row=1,column=2)

		#TIPO DE VEHÍCULO
		self.kindLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=15,bg=bgcolor2)
		self.kindLabel.grid(row=1,column=4)

		#NÚMERO DE MOTOR
		self.engineLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=20,bg=bgcolor2)
		self.engineLabel.grid(row=1,column=6)

		#MARCA
		self.brandLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=15,bg=bgcolor2)
		self.brandLabel.grid(row=2,column=2)

		#MODELO
		self.modelLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=15,bg=bgcolor2)
		self.modelLabel.grid(row=2,column=4)

		#AÑO
		self.yearLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=20,bg=bgcolor2)
		self.yearLabel.grid(row=2,column=6)

		#TITULAR
		self.titularLabel=Label(dataVehicle,font=("Verdana",12,"italic"),anchor="w",width=45,bg=bgcolor2)
		self.titularLabel.grid(row=3,column=2,columnspan=3)

		#DNI DEL TITULAR
		self.dniLabel=Label(dataVehicle,font=("Verdana",12,"italic"),width=20,bg=bgcolor2)
		self.dniLabel.grid(row=3,column=6)

		#CREA TABLA DE INFRACCIONES
		self.tableFrame = Frame(self)
		self.model=TableModel()
		self.model.addColumn(colname="ID")
		self.model.columnwidths["ID"]=80
		self.model.addColumn(colname="DNI RESPONSABLE")
		self.model.columnwidths["DNI RESPONSABLE"]=90
		self.model.addColumn(colname="CAUSA")
		self.model.addColumn(colname="AGENTE")
		self.model.addColumn(colname="FECHA")
		self.model.addColumn(colname="LUGAR")
		self.model.addColumn(colname="MONTO")
		self.model.columnwidths["MONTO"]=70
		self.model.addColumn(colname="PAGADO")
		self.model.columnwidths["PAGADO"]=70
		self.infractionsTable = TableCanvas(self.tableFrame,model=self.model,width=938,thefont=("Arial",10),read_only=True)
		self.infractionsTable.show()
		self.tableFrame.place(x="20",rely="0.35")

		#CREA MENSAJE DE ESTADO DE CUENTA
		self.message=StringVar()
		self.debtLabel=Label(self,textvariable=self.message,font=("Verdana",12))
		self.debtLabel.place(x="30",rely="0.30")

	#FUNCIÓN QUE DEVUELVE LA FILA SELECCIONADA
	def getSelectedRow(self):
		return(self.infractionsTable.get_currentRecord())

	#FUNCIÓN QUE CARGA EL PANEL Y LA TABLA DE INFRACCIONES CON LOS DATOS CORRESPONDIENTES
	def showData(self,data):
		self.model.deleteRows()
		dataModel={}

		if data!=None:
			self.domainLabel.configure(text=data[0])
			self.kindLabel.configure(text=data[1])
			self.brandLabel.configure(text=data[2])
			self.modelLabel.configure(text=data[3])
			self.yearLabel.configure(text=data[4])
			self.engineLabel.configure(text=data[5])
			self.titularLabel.configure(text=data[7] + ", " + data[8])
			self.dniLabel.configure(text=data[6])

			infractions=DBManager().getInfractions(data[0])
			self.debt=0.00
			for infraction in infractions:
				isPay='NO'
				if(infraction[8]==1):
					isPay='SI'
				dateandhour="%02d-%02d-%4d %02d:%02d"%(infraction[5].day,infraction[5].month,infraction[5].year,infraction[5].hour,infraction[5].minute)
				dateandhourpaid="-"
				if(infraction[9]!=None):
					dateandhourpaid="%02d-%02d-%4d %02d:%02d"%(infraction[9].day,infraction[9].month,infraction[9].year,infraction[9].hour,infraction[9].minute)
				dataModel[infraction[0]]={'ID':"%07d"%(infraction[0]),
					'DNI RESPONSABLE':str(infraction[1]),
					'CAUSA':str(infraction[3]),
					'AGENTE':str(infraction[4]),
					'FECHA':dateandhour,
					'LUGAR':str(infraction[6]),
					'MONTO':"%.2f"%(infraction[7]),
					'PAGADO':isPay,
					'FECHA PAGO':dateandhourpaid}
				if(infraction[8]==0):
					self.debt=self.debt+float(infraction[7])
			if(self.debt>0):
				self.message.set("Presenta una deuda de $ " + str(self.debt))
			else:	
				self.message.set("No presenta deudas.")
		#SI LA BÚSQUEDA NO ARROJA RESULTADOS, LOS CAMPOS SE MUESTRAN EN BLANCO
		else:
			self.domainLabel.configure(text="")
			self.kindLabel.configure(text="")
			self.brandLabel.configure(text="")
			self.modelLabel.configure(text="")
			self.yearLabel.configure(text="")
			self.engineLabel.configure(text="")
			self.titularLabel.configure(text="")
			self.dniLabel.configure(text="")
			self.message.set("")

		#ACTUALIZA EL CONTENIDO DE LA TABLA
		self.model.importDict(dataModel)
		self.infractionsTable.redraw()
		self.infractionsTable.autoResizeColumns()
