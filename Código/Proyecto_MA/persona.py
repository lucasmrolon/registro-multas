
#CLASE PERSONA
class Person:

	def __init__(self,dni,surname,name,birth,residence,nationality,category,bloodtype):
		self.__dni=dni 					#DNI
		self.__surname=surname 			#APELLIDO
		self.__name=name 				#NOMBRE
		self.__birth=birth 				#FECHA DE NACIMIENTO
		self.__residence=residence 		#DOMICILIO
		self.__nationality=nationality 	#NACIONALIDAD
		self.__category=category 		#CATEGORÍA DE LICENCIA
		self.__bloodtype=bloodtype 		#TIPO DE SANGRE

	def getDni(self):
		return self.__dni

	def getSurname(self):
		return self.__surname

	def getName(self):
		return self.__name

	def getBirth(self):
		return self.__birth

	def getResidence(self):
		return self.__residence

	def getNationality(self):
		return self.__nationality

	def getCategory(self):
		return self.__category

	def getBloodtype(self):
		return self.__bloodtype

	def setDni(self,dni):
		self.__dni=dni

	def setSurname(self,surname):
		self.__surname=surname

	def setName(self,name):
		self.__name=name

	def setBirth(self,birth):
		self.__birth=birth

	def setResidence(self,residence):
		self.__residence=residence

	def setNationality(self,nationality):
		self.__nationality = nationality

	def setCategory(self,category):
		self.__category=category

	def setBloodtype(self,bloodtype):
		self.__bloodtype=bloodtype