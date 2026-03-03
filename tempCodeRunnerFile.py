class JuegoDeApuestas:

    def __init__(self,capInicial, meta, numSimulaciones):
        self.capInicial = capInicial
        self.meta = meta
        self.numSimulaciones = numSimulaciones

    def iniciarVentana(self):
        ventana = tk.Tk()
        ventana.title("Simulación de Juego de Apuestas")
        ventana.geometry("400x300")
        ventana.mainloop()

if __name__=="__main__":
    juego = JuegoDeApuestas(10,100,20)
    juego.iniciarVentana()  