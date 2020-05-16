from loginFrame import *
from PIL import Image,ImageTk
import os, sys

#CLASE INICIAL QUE INSTANCIA LA VENTANA DE LA APLICACIÓN
class WindowApp(Tk):
	def __init__(self):
		super().__init__()
		self.main()
	def main(self):
		
		#ESTABLECE ICONO, TITULO, TAMAÑO Y CARACTERÍSITICAS DE LA VENTANA
		#self.iconbitmap("pc_icon.ico")
		self.title("S.M.G.I.  v1.0")
		self.state('zoomed')
		self.resizable(0,0)
		self.overrideredirect(True)

		xframe=self.winfo_screenwidth()
		yframe=self.winfo_screenheight()

		style = ttk.Style()
		settings = {"TNotebook.Tab": {"configure": {"padding": [5, 1],"background": "#%02x%02x%02x" % (150,203,202),"font":('Verdana',14)},
										"map": {"background":[("selected", "#%02x%02x%02x" % (75,115,167)),("active", "#%02x%02x%02x" % (136,164,202))],
										"foreground": [("selected", "#ffffff"),("active", "#000000")]
										}
									}	
					}  
		style.theme_create("my_style", parent="alt", settings=settings)
		style.theme_use("my_style")

		#SELECCIONA IMAGEN DE FONDO DE LA PANTALLA DE LOGIN
		image_bg=ImageTk.PhotoImage(Image.open(self.resolver_ruta("maxresdefault.png")).resize((xframe,yframe)))
		Label(self,image=image_bg,width=xframe,height=yframe).place(x="0",y="0",relwidth=1,relheight=1)
		#Label(self,bg="gray",width=xframe,height=yframe).place(x="0",y="0",relwidth=1,relheight=1)

		#BOTÓN DE CIERRE DE LA APLICACIÓN
		Button(self,text="X",font=("Verdana",14,"bold"),bg="red",width=2,height=1,command=lambda:self.close_app()).place(x=xframe-39,y=0)

		#INSTANCIA EL CUADRO DE LOGIN
		LoginFrame(self,xframe,yframe).place(x=xframe/2-200,y=yframe/2-100)

		self.mainloop()

	#FUNCIÓN QUE CIERRA LA APLICACIÓN
	def close_app(self):
		if(messagebox.askyesno("Mensaje de confirmación","¿Desea salir de la aplicación?")):
			self.destroy()

	def resolver_ruta(self,rute):
		if hasattr(sys, '_MEIPASS'):
			return os.path.join(sys._MEIPASS, rute)
		return os.path.join(os.path.abspath('.'), rute)

#LANZA LA APLICACIÓN
if __name__ == "__main__":
	app=WindowApp()
