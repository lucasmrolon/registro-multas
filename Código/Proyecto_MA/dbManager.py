import pymysql
from infraccion import *
import datetime
from tkinter import messagebox

class DBManager:

	#REALIZA LA CONEXIÓN CON LA BASE DE DATOS
	def connectDB(self):
		try:
			self.db = pymysql.connect(host="localhost", user="root", password="", db="TransitoDB")
			self.cursor=self.db.cursor()
		except:
			messagebox.showwarning("Error","No se pudo conectar con la base de datos")


	#DESCONECTA LA BASE DE DATOS
	def disconnectDB(self):
		self.cursor.close()
		self.db.close()	

	#PERMITE AÑADIR USUARIOS DEL SISTEMA
	def addUser(self,user,password):
		self.connectDB()
		self.cursor.execute("INSERT INTO users(user,password) VALUES (NULL,'" + user + "','" + password + "')")
		self.disconnectDB()

	#OBTIENE USUARIO Y CONTRASEÑA
	def login(self,user):
		self.connectDB()
		self.cursor.execute("SELECT user,password FROM users WHERE user='"+ user + "'")
		result=self.cursor.fetchone()
		self.disconnectDB()
		return result

	#AÑADE INFRACCIÓN
	def addInfraction(self,infraction):
		self.connectDB()
		self.cursor.execute("INSERT INTO infractions(dni_resp,domain,cause,agent,datea,place,mount,paid) VALUES (" +
			"'"  +str(infraction.getDniResp()) + "'" +
			",'" +infraction.getDomain() + "'" +
			",'" +infraction.getCause() + "'" +
			",'" +infraction.getAgent() + "'" +
			",'" +str(infraction.getDate())  + "'" +
			",'" +infraction.getPlace() + "'" +
			",'" +str(infraction.getMount()) + "'" +
			",'" +str(infraction.isPaid())+ "')")
		self.db.commit()
		self.disconnectDB()

	#OBTIENE INFRACCIONES ASOCIADAS AL DOMINIO
	def getInfractions(self,domain):
		self.connectDB()
		self.cursor.execute("SELECT * FROM infractions WHERE domain='" + domain + "' AND erased=0")
		result=self.cursor.fetchall()
		self.disconnectDB()
		return result

	#BORRA UNA INFRACCIÓN
	def deleteInfraction(self,id_infraction):
		self.connectDB()
		self.cursor.execute("UPDATE infractions SET erased = 1 WHERE id=" + str(id_infraction))
		self.db.commit()
		self.disconnectDB()

	#REGISTRA EL PAGO DE UNA INFRACCIÓN
	def payInfraction(self,id_infraction,pay_date):
		self.connectDB()
		self.cursor.execute("UPDATE infractions SET paid = 1,paydate='" + str(pay_date) + "' WHERE id=" + str(id_infraction))
		self.db.commit()
		self.disconnectDB()

	#PERMITE AÑADIR UNA PERSONA A LA BD
	def addPerson(self,person):
		self.connectDB()
		self.cursor.execute("SELECT COUNT(dni) FROM persons WHERE dni='" + person.getDni() + "'")
		existe=self.cursor.fetchone()[0]
		if(existe==0):
			self.cursor.execute("INSERT INTO persons(dni,surname,name,birth,residence,nationality,category,bloodtype) VALUES" +
				"('" +str(person.getDni()) + "'" +
				",'" +person.getSurname() + "'" +
				",'" +person.getName() + "'" +
				",'" +str(person.getBirth())  + "'" +
				",'" +person.getResidence() + "'" +
				",'" +person.getNationality() + "'" +
				",'" +person.getCategory() + "'" +
				",'" +person.getBloodtype()+ "')")
		else:
			self.cursor.execute("UPDATE persons SET " +
			"surname='" + person.getSurname() + "'" +
			",name='" + person.getName() + "'" +
			",birth='" + str(person.getBirth()) + "'" +
			",residence='" +person.getResidence() + "'" +
			",nationality='" +person.getNationality() + "'" +
			",category='" +person.getCategory() + "'" +
			",bloodtype='" +person.getBloodtype() + "'" +
			",erased=0" +
			" WHERE dni='" + person.getDni()+ "'")
		self.db.commit()
		self.disconnectDB()

	#PERMITE MODIFICAR EL REGISTRO DE UNA PERSONA
	def modifyPerson(self,person):
		self.connectDB()
		self.cursor.execute("UPDATE persons SET " +
			"surname='" + person.getSurname() + "'" +
			",name='" + person.getName() + "'" +
			",birth='" + str(person.getBirth()) + "'" +
			",residence='" +person.getResidence() + "'" +
			",nationality='" +person.getNationality() + "'" +
			",category='" +person.getCategory() + "'" +
			",bloodtype='" +person.getBloodtype() + "'" +
			" WHERE dni='" + person.getDni()+ "'")
		self.db.commit()
		self.disconnectDB()

	#OBTIENE LOS REGISTROS DE PERSONAS ALMACENADAS EN LA BASE DE DATOS
	def getAllPersons(self):
		self.connectDB()
		self.cursor.execute("SELECT dni,surname,name,birth,residence,nationality,category,bloodtype " + 
			"FROM persons WHERE erased=0")
		result=self.cursor.fetchall()
		self.disconnectDB()
		return result

	#ELIMINA UN REGISTRO DE LA BASE DE DATOS
	def deletePerson(self,dni):
		self.connectDB()
		self.cursor.execute("UPDATE persons SET erased=1 WHERE dni='" + str(dni) + "'")
		self.db.commit()
		self.disconnectDB()

	#REGISTRA UN VEHÍCULO EN LA BASE DE DATOS
	def addVehicle(self,vehicle):
		self.connectDB()
		self.cursor.execute("SELECT COUNT(domain) FROM vehicles WHERE domain='" + vehicle.getDomain() + "'")
		existe=self.cursor.fetchone()[0]
		if(existe==0):
			self.cursor.execute("INSERT INTO vehicles(domain,kind,brand,model,year,vin,owner) VALUES" +
				"('" +vehicle.getDomain() + "'" +
				",'" +vehicle.getKind() + "'" +
				",'" +vehicle.getBrand() + "'" +
				",'" +vehicle.getModel()  + "'" +
				",'" +str(vehicle.getYear()) + "'" +
				",'" +vehicle.getVin() + "'" +
				",'" +str(vehicle.getOwner())+ "')")
		else:
			self.cursor.execute("UPDATE vehicles SET " +
			"kind='" +vehicle.getKind() + "'" +
			",brand='" +vehicle.getBrand() + "'" +
			",model='" +vehicle.getModel() + "'" +
			",year='" +str(vehicle.getYear()) + "'" +
			",vin='" +str(vehicle.getVin()) + "'" +
			",owner='" +str(vehicle.getOwner()) + "'" +
			",erased=1" +
			" WHERE domain='" +vehicle.getDomain()+ "'")
		self.db.commit()
		self.disconnectDB()

	#MODIFICA UN REGISTRO DE LA BASE DE DATOS
	def modifyVehicle(self,vehicle):
		self.connectDB()
		self.cursor.execute("UPDATE vehicles SET " +
			"kind='" +vehicle.getKind() + "'" +
			",brand='" +vehicle.getBrand() + "'" +
			",model='" +vehicle.getModel() + "'" +
			",year='" +str(vehicle.getYear()) + "'" +
			",vin='" +str(vehicle.getVin()) + "'" +
			",owner='" +str(vehicle.getOwner()) + "'" +
			" WHERE domain='" +vehicle.getDomain()+ "'")
		self.db.commit()
		self.disconnectDB()

	#OBTIENE VEHÍCULO A PARTIR DE SU DOMINIO
	def getVehicle(self,domain):
		self.connectDB()
		self.cursor.execute("SELECT domain,kind,brand,model,year,vin,owner,persons.surname,persons.name " + 
			"FROM vehicles INNER JOIN persons ON vehicles.owner = persons.dni WHERE domain=%s AND vehicles.erased=0",domain)
		result=self.cursor.fetchone()
		self.disconnectDB()
		return result

	#OBTIENE LOS VEHÍCULOS REGISTRADOS EN LA BASE DE DATOS
	def getAllVehicles(self):
		self.connectDB()
		self.cursor.execute("SELECT domain,kind,brand,model,year,vin,owner " + 
			"FROM vehicles WHERE erased=0")
		result=self.cursor.fetchall()
		self.disconnectDB()
		return result

	#ELIMINA UN VEHÍCULO REGISTRADO
	def deleteVehicle(self,domain):
		self.connectDB()
		self.cursor.execute("UPDATE vehicles SET erased=1 WHERE domain='" + domain + "'")
		self.db.commit()
		self.disconnectDB()

	#OBTIENE LAS MARCAS DE VEHÍCULOS 
	def getBrands(self,kind):
		self.connectDB()
		self.cursor.execute("SELECT DISTINCT brands.brand FROM brands INNER JOIN models ON brands.id = models.brand WHERE models.kind='" + kind + "'")
		result=self.cursor.fetchall()
		self.disconnectDB()
		return result

	#OBTIENE LOS MODELOS DE VEHÍCULOS
	def getModels(self,brand,kind):
		self.connectDB()
		self.cursor.execute("SELECT model FROM models WHERE brand=(SELECT id FROM brands WHERE brand='" + brand + "')" + 
			" AND kind='" + kind + "'")
		result=self.cursor.fetchall()
		self.disconnectDB()
		return result

	#VERIFICA SI UN DOMINIO SE ENCUENTRA REGISTRADO
	def searchDomain(self,domain):
		self.connectDB()
		self.cursor.execute("SELECT domain FROM vehicles WHERE domain='" + domain + "' AND erased=0")
		result=self.cursor.fetchone()
		self.disconnectDB()
		return result

	#VERIFICA SI UN DNI SE ENCUENTRA REGISTRADO
	def searchDni(self,dni):
		self.connectDB()
		self.cursor.execute("SELECT dni FROM persons WHERE dni='" + dni + "' AND erased=0")
		result=self.cursor.fetchone()
		self.disconnectDB()
		return result