from tkinter import *
from tkinter import ttk
import datetime
from dbManager import * 

#PANEL DE CREACIÓN DE NUEVA INFRACCIÓN
class NewInfractionTab(Frame):
	def __init__(self,frame,domain):

		#CARACTERÍSITCAS DE VENTANA	
		bgcolor="#%02x%02x%02x" % (166,185,180)
		super().__init__(frame,bg=bgcolor)
		self.frame=frame
		font=("Verdana",12)
		
		Label(self,bg=bgcolor,text="Ingrese datos de infracción:",font=("Arial",18,"italic")).place(
			relx=0.10,rely=0.08)

		#PANEL PARA INGRESAR DATOS DE INFRACCIÓN
		dataInfraction=Frame(self,bg=bgcolor)
		dataInfraction.place(relx=0.15,rely=0.15)

		Label(dataInfraction,text="Dominio",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=1,column=1,pady=15)
		Label(dataInfraction,text="DNI conductor",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=2,column=1,pady=15)
		Label(dataInfraction,text="Causa",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=3,column=1,pady=15)
		Label(dataInfraction,text="Agente",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=4,column=1,pady=15)
		Label(dataInfraction,text="Fecha",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=5,column=1,pady=15)
		Label(dataInfraction,text="Lugar",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=6,column=1,pady=15)
		Label(dataInfraction,text="Monto",width=15,bg="lightblue",relief="groove",borderwidth=4,font=font).grid(
			row=7,column=1,pady=15)

		#SE CREAN LAS VARIABLES CORRESPONDIENTES, EL DOMINIO ES ESTÁTICO
		self.domain=domain
		self.dni=StringVar()
		self.cause=StringVar()
		self.agent=StringVar()
		self.day=IntVar()
		self.month=StringVar()
		self.year=IntVar()
		self.hour=IntVar()
		self.minutes=IntVar()
		self.place=StringVar()
		self.mount=DoubleVar()
		self.mount.set("%.2f"%(0.00))

		#CUADRO DE TEXTO DE DOMINIO
		self.domainBox=Label(dataInfraction,text=self.domain,font=font,highlightbackground="red",justify="center",width=18)
		self.domainBox.grid(row=1,column=2,padx=20)
		self.errorDomainLabel=Label(dataInfraction,text="El dominio no está registrado",fg="red")

		#CUADRO DE TEXTO DE DNI Y SU MENSAJE DE ERROR CORRESPONDIENTE SI NO ESTÁ REGISTRADO
		self.dniBox=Entry(dataInfraction,textvariable=self.dni,font=font,highlightbackground="red",justify="center",width=18)
		self.dniBox.grid(row=2,column=2,padx=20)
		self.dniBox.bind('<FocusOut>',lambda x:self.evaluateDni())
		self.errorDniLabel=Label(dataInfraction,text="El conductor no está registrado",fg="red")

		#SELECCIÓN DE CAUSA DE INFRACCIÓN
		causeBox=ttk.Combobox(dataInfraction,textvariable=self.cause,state="readonly",font=font,justify="center",width=16)
		causeBox["values"]=["S/ CASCO","S/ PATENTE","S/ LUCES","FALTA PAPELES","CONDUCCIÓN PELIGROSA","SEMÁFORO EN ROJO","ESTAC. DOBLE FILA"]
		causeBox.grid(row=3,column=2,padx=20)

		#CUADRO DE TEXTO DE AGENTE DE TRÁNSITO
		agentBox=Entry(dataInfraction,textvariable=self.agent,font=font,justify="center",width=18)
		agentBox.grid(row=4,column=2,padx=20)


		#PANEL DE SELECCIÓN DE FECHA Y HORA
		dateGrid=Frame(dataInfraction,bg=bgcolor)

		#OBTIENE FECHA Y HORA ACTUAL
		self.actual_date=datetime.datetime.now()
		
		#SELECCIÓN DE DÍA
		Label(dateGrid,bg=bgcolor,text="día",font=("Arial",8)).place(x=25,y=9)
		self.dayBox=ttk.Combobox(dateGrid,textvariable=self.day,state="readonly",font=font,width=3)
		self.dayBox.set(self.actual_date.day)
		self.dayBox.grid(row=1,column=1,columnspan=2,padx=10,pady=25)

		#SELECCIÓN DE MES
		self.meses=["Enero","Febrero","Marzo","Abril","Mayo","Junio",
			"Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
		Label(dateGrid,bg=bgcolor,text="mes",font=("Arial",8)).place(x=140,y=9)
		monthBox=ttk.Combobox(dateGrid,textvariable=self.month,state="readonly",font=font,width=12)
		monthBox["values"]=self.meses
		monthBox.bind("<<ComboboxSelected>>", lambda x:self.setdays())
		monthBox.current(self.actual_date.month-1)
		monthBox.grid(row=1,column=3,columnspan=2,padx=10,pady=25)
		
		#SELECCIÓN DE AÑO
		Label(dateGrid,bg=bgcolor,text="año",font=("Arial",8)).place(x=280,y=9)
		yearBox=ttk.Combobox(dateGrid,textvariable=self.year,state="readonly",font=font,width=7)
		initial_year=self.actual_date.year
		for i in range(30):
			yearBox["values"]=list(yearBox["values"])+[str(initial_year - i)]
		yearBox.bind("<<ComboboxSelected>>", lambda x:self.setdays())
		yearBox.set(self.actual_date.year)
		yearBox.grid(row=1,column=5,columnspan=2,padx=10,pady=25)
		self.setdays()

		#SELECCIÓN DE HORA
		Label(dateGrid,bg=bgcolor,text="hora",font=("Arial",8)).place(x=98,y=57)
		hourBox=Spinbox(dateGrid,textvariable=self.hour,from_=0,to=23,font=font,width=3,state="readonly")
		hourBox.grid(row=2,column=3)

		#SELECCIÓN DE MINUTOS
		Label(dateGrid,bg=bgcolor,text="minutos",font=("Arial",8)).place(x=173,y=57)
		minuteBox=Spinbox(dateGrid,textvariable=self.minutes,from_=0,to=59,font=font,width=3,state="readonly")
		minuteBox.grid(row=2,column=4)

		dateGrid.grid(row=5,column=2,padx=20)
		
		#MUESTRA MENSAJE DE ERROR SI LA FECHA ES INVÁLIDA
		self.errorDateLabel=Label(dataInfraction,text="Fecha inválida",fg="red")
		
		#CUADRO DE TEXTO DE LUGAR
		placeBox=Entry(dataInfraction,textvariable=self.place,font=font,justify="center",width=18)
		placeBox.grid(row=6,column=2,padx=20)

		#CUADRO DE TEXTO DE MONTO DE INFRACCIÓN
		#EVALÚA QUE SOLO SE INGRESE VALORES NUMÉRICOS
		vcmd = (self.register(self.checkNumberOnly), '%d', '%P')
		mountBox=Entry(dataInfraction,textvariable=self.mount,font=font,justify="center",width=18,validate='key',validatecommand=vcmd)
		mountBox.bind('<KeyPress>',self.check)
		mountBox.bind('<BackSpace>',self.clear_action)
		mountBox.grid(row=7,column=2,padx=40)

		#MENSAJE DE ERROR SI FALTA COMPLETAR CAMPOS
		self.evaluateLabel=Label(self,text="*Falta completar uno o más campos",bg=bgcolor,width=30,fg="red",font=("Verdana",10))

		#BOTÓN PARA CREAR LA INFRACCIÓN
		Button(self,text="GUARDAR DATOS",font=("Arial",14),command=lambda:self.save()).place(relx=0.15,rely=0.85)

		#BOTÓN PARA CANCELAR LA ACCIÓN
		Button(self,text="CANCELAR",font=("Arial",14),command=lambda:self.close()).place(relx=0.45,rely=0.85)

	#FUNCIONES AUXILIARES PARA FORMATEAR EL MONTO INGRESADO
	def check(self,event):
		if(event.char.isdigit()):
			to_add=int(event.char)/100
			result=self.mount.get()*10+to_add
			self.mount.set("%.2f"%round(result,2))
	def clear_action(self,event):
		result=self.mount.get()/10
		self.mount.set("%.2f"%round(result,2))

	#FUNCIÓN QUE EVALUA LOS VALORES INGRESADOS EN EL CUADRO DE TEXTO DE MONTO
	def checkNumberOnly(self, action, value_if_allowed):
		if action != '1':
			return True
		try:
			return value_if_allowed.isnumeric()
		except ValueError:
			return False

	#FUNCIÓN AUXILIAR PARA CAMBIAR DINÁMICAMENTE EL CONTENIDO DE LOS COMBOBOX DE FECHA
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

	#EVALÚA EL DOMINIO
	def evaluateDomain(self):
		if(DBManager().searchDomain(self.domain.get())==None):
			self.errorDomainLabel.grid(row=1,column=3)
			self.domainBox.configure(highlightthickness=1)
			return False
		else:
			self.errorDomainLabel.grid_forget()
			self.domainBox.configure(highlightthickness=0)
			return True

	#EVALÚA SI EL DNI SE ENCUENTRA REGISTRADO
	def evaluateDni(self):
		if(DBManager().searchDni(self.dni.get())==None):
			self.errorDniLabel.grid(row=2,column=3)
			self.dniBox.configure(highlightthickness=1)
			return False
		else:
			self.errorDniLabel.grid_forget()
			self.dniBox.configure(highlightthickness=0)
			return True

	#EVALÚA SI TODOS LOS CAMPOS FUERON COMPLETADOS
	def evaluateForm(self):
		if(self.cause.get()!="" and self.agent.get()!="" and self.place.get()!="" and self.mount.get()!="0.0"):
			self.evaluateLabel.place_forget()
			return True
		else:
			self.evaluateLabel.place(relx=0.15,rely=0.81)
			return False

	#EVALÚA QUE LA FECHA INGRESADA SEA VÁLIDA
	def evaluateDate(self):
			datetime_str=("%4d-%02d-%02d %02d:%02d:00.000000"%(self.year.get(),self.meses.index(self.month.get())+1,self.day.get(),self.hour.get(),self.minutes.get()))
			self.dateandhour=datetime.datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S.%f')
			if(self.dateandhour>datetime.datetime.now()):
				self.errorDateLabel.grid(row=5,column=3)
				return False
			else:
				self.errorDateLabel.grid_forget()
				return True

	#FUNCIÓN PARA CREAR LA INFRACCIÓN Y GUARDARLA EN LA BASE DE DATOS
	def save(self):
		okDni=self.evaluateDni()
		okForm=self.evaluateForm()
		okDate=self.evaluateDate()
		if(okDni and okForm and okDate):
			if(messagebox.askyesno("Mensaje de confirmación","¿Agregar la infracción a la base de datos?")):
				datetime_str=("%4d-%02d-%02d %02d:%02d:00.000000"%(self.year.get(),self.meses.index(self.month.get())+1,self.day.get(),self.hour.get(),self.minutes.get()))
				datetime_obj=datetime.datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S.%f')
				DBManager().addInfraction(
					Infraccion(
						'Null',self.dni.get(),self.domain,self.cause.get(),self.agent.get(),datetime_obj,self.place.get(),self.mount.get()))
				self.close()

	#FUNCIÓN QUE CIERRA LA PESTAÑA
	def close(self):
		self.frame.principalFrame.search()
		self.frame.principalFrame.searchBox["state"]="normal"
		self.frame.newInfractionFlag=0
		self.destroy()

#PESTAÑA DE ELIMINACIÓN DE INFRACCIÓN
class DeleteInfractionTab(Frame):
	def __init__(self,frame,domain,infraction,bgcolor):
		
		#CARACTERÍSTICAS DE PESTAÑA
		self.frame=frame
		super().__init__(self.frame,bg=bgcolor)

		#MENSAJE INFORMATIVO
		self.mensaje = Label(self,bg=bgcolor,
			text="¿Eliminar la siguiente infracción?",font=("Arial",18,"italic"))
		self.mensaje.place(relx=0.10,rely=0.08)

		#FUENTES A UTILIZAR
		font=("Verdana",11)
		fontbold=("Verdana",11,"bold")

		#NÚMERO DE INFRACCIÓN
		Label(self,text="Infracción N° ",font=font,bg=bgcolor).place(
			relx=0.2,rely=0.18)	
		Label(self,text="%07d"%(int(infraction['ID'])),font=fontbold).place(
			relx=0.35,rely=0.18)

		#DOMINIO DEL VEHÍCULO	
		Label(self,text="Realizada a:",font=font,bg=bgcolor).place(
			relx=0.2,rely=0.27)
		Label(self,text="Dominio: ",font=font,bg=bgcolor).place(
			relx=0.25,rely=0.31)
		Label(self,text=domain,font=fontbold).place(
			relx=0.35,rely=0.31)

		#DNI DEL RESPONSABLE
		Label(self,text="DNI: ",font=font,bg=bgcolor).place(
			relx=0.50,rely=0.31)
		Label(self,text=infraction['DNI RESPONSABLE'],font=fontbold).place(
			relx=0.55,rely=0.31)

		#MOTIVO DE LA INFRACCIÓN
		Label(self,text="Motivo: ",font=font,bg=bgcolor).place(
			relx=0.2,rely=0.38)
		Label(self,text=infraction['CAUSA'],font=fontbold).place(
			relx=0.35,rely=0.38)

		#AGENTE DE TRÁNSITO
		Label(self,text="Agente de Tránsito: ",font=font,bg=bgcolor).place(
			relx=0.2,rely=0.47)	
		Label(self,text=infraction['AGENTE'],font=fontbold).place(
			relx=0.35,rely=0.47)	

		#FECHA Y HORA
		dateandhour=datetime.datetime.strptime(infraction['FECHA'],'%d-%m-%Y %H:%M')
		Label(self,text="El día: ",font=font,bg=bgcolor).place(
				relx=0.2,rely=0.56)
		Label(self,text="%02d / %02d / %4d"%(dateandhour.day,dateandhour.month,dateandhour.year),font=fontbold).place(
				relx=0.26,rely=0.56)
		Label(self,text=" a las ",font=font,bg=bgcolor).place(
				relx=0.40,rely=0.56)
		Label(self,text="%2d : %02d"%(dateandhour.hour,dateandhour.minute),font=fontbold).place(
				relx=0.46,rely=0.56)
		Label(self,text=" hs.",font=font,bg=bgcolor).place(
				relx=0.53,rely=0.56)

		#LUGAR DE LA INFRACCIÓN
		Label(self,text="En: ",font=font,bg=bgcolor).place(
				relx=0.2,rely=0.65)
		Label(self,text=infraction['LUGAR'],font=fontbold).place(
				relx=0.26,rely=0.65)

		#MONTO DE LA INFRACCIÓN
		Label(self,text="Por un monto de $ ",font=font,bg=bgcolor).place(
			relx=0.2,rely=0.74)
		Label(self,text=infraction['MONTO'],font=fontbold).place(
			relx=0.35,rely=0.74)

		#BOTÓN PARA PROCEDER CON LA ELIMINACIÓN
		self.acceptButton=Button(
			self,text="ELIMINAR INFRACCIÓN",font=("Arial",14),command=lambda:self.save(infraction['ID']),bg="#%02x%02x%02x" % (243,129,132))
		self.acceptButton.place(relx=0.15,rely=0.85)

		#BOTÓN PARA CANCELAR LA ACCIÓN
		Button(self,text="CANCELAR",font=("Arial",14),command=lambda:self.close()).place(relx=0.45,rely=0.85)

	#CIERRA LA PESTAÑA
	def close(self):
		self.frame.principalFrame.search()
		self.frame.deleteInfractionFlag=0
		self.frame.principalFrame.searchBox["state"]="normal"
		self.destroy()

	#REFLEJA LA ELIMINACIÓN EN LA BASE DE DATOS
	def save(self,id_infraction):
		if(messagebox.askyesno("Mensaje de confirmación","¿Confirma la eliminación de la infracción?")):
			DBManager().deleteInfraction(id_infraction)
			self.close()

#PESTAÑA DE PAGO DE INFRACCIÓN
class PayInfractionTab(DeleteInfractionTab):
	def __init__(self,frame,domain,infraction):
		
		#CARACTERÍSTICAS DE PESTAÑA
		self.frame=frame
		super().__init__(self.frame,domain,infraction,"#%02x%02x%02x" % (166,185,180))

		#MENSAJE INFORMATIVO
		self.mensaje["text"]="¿Registrar el pago de la siguiente infracción?"

		#BOTÓN DE PAGO DE INFRACCIÓN
		self.acceptButton["text"]="CONFIRMAR PAGO"
		self.acceptButton["bg"]="white"

	#REFLEJA EL PAGO EN LA BASE DE DATOS
	def save(self,id_infraction):
		if(messagebox.askyesno("Mensaje de confirmación","¿Confirma el pago de la infracción?")):
			actual_date=datetime.datetime.now()
			DBManager().payInfraction(id_infraction,actual_date)
			self.close()

	#CIERRA LA PESTAÑA
	def close(self):
		self.frame.principalFrame.search()
		self.frame.payInfractionFlag=0
		self.frame.principalFrame.searchBox["state"]="normal"
		self.destroy()