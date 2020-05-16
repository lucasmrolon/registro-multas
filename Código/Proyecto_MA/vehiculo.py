from infraccion import *
from dbManager import *

#CLASE VEHÍCULO
class Vehiculo:

	def __init__(self,kind,domain,brand,model,year,vin,owner):
		self.__domain=domain   	#DOMINIO
		self.__kind=kind 		#TIPO
		self.__brand=brand 		#MARCA
		self.__model=model 		#MODELO
		self.__year=year 		#AÑO
		self.__vin=vin 			#MOTOR
		self.__owner=owner 		#DNI PROPIETARIO

	def modifyOwner(self,new_owner):
		self.__owner=new_owner

	def getDomain(self):
		return self.__domain

	def getKind(self):
		return self.__kind

	def getBrand(self):
		return self.__brand

	def getModel(self):
		return self.__model

	def getYear(self):
		return self.__year

	def getVin(self):
		return self.__vin

	def getOwner(self):
		return self.__owner

	def setDomain(self,domain):
		self.__domain=domain

	def setKind(self,kind):
		self.__kind=kind

	def setBrand(self,brand):
		self.__brand=brand

	def setModel(self,model):
		self.__model=model

	def setYear(self,year):
		self.__year=year

	def setVin(self,vin):
		self.__vin = vin


