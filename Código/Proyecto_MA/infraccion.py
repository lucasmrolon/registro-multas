
#CLASE INFRACCIÓN
class Infraccion:

	def __init__(self,id_infraction,dni_resp,domain,cause,agent,date,place,mount):
		self.__id_infraction=id_infraction 	#ID INFRACCIÓN
		self.__dni_resp=dni_resp 			#DNI RESPONSABLE
		self.__domain=domain 				#DOMINIO VEHÍCULO
		self.__cause=cause 					#MOTIVO INFRACCIÓN
		self.__agent=agent 					#AGENTE DE TRÁNSITO
		self.__date=date 					#FECHA Y HORA
		self.__place=place 					#LUGAR
		self.__mount=mount 					#MONTO A PAGAR
		self.__paid=0 						#¿SE HA ABONADO?
		self.__paiddate=None 				#FECHA DE PAGO

	def getId(self):
		return self.__id_infraction

	def getDniResp(self):
		return self.__dni_resp

	def getDomain(self):
		return self.__domain

	def getCause(self):
		return self.__cause

	def getAgent(self):
		return self.__agent

	def getDate(self):
		return self.__date

	def getPlace(self):
		return self.__place

	def getMount(self):
		return self.__mount

	def isPaid(self):
		return self.__paid

	def setDniResp(self,dni_resp):
		self.__dni_resp=dni_resp

	def setDomain(self,domain):
		self.__domain=domain

	def setCause(self,cause):
		self.__cause=cause

	def setAgent(self,agent):
		self.__agent=agent

	def setDate(self,date):
		self.__date=date

	def setPlace(self,place):
		self.__place=place

	def setMount(self,mount):
		self.__mount=mount
