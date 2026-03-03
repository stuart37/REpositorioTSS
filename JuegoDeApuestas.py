import tkinter as tk
import random

class JuegoDeApuestas:
    #constructor
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Juego de Apuestas")
        self.ventana.geometry("450x400")

        self.numApuesta = 10

        # para graficar las entradas
        tk.Label(self.ventana,text="Capital Inicial:").grid(row=0, column=0, padx=10, pady=10)
        self.textCapInicial = tk.Entry(self.ventana)
        self.textCapInicial.grid(row=0, column=1)

        tk.Label(self.ventana,text="Meta a Alcanzar:").grid(row=1, column=0, padx=10, pady=10)
        self.textMeta = tk.Entry(self.ventana)
        self.textMeta.grid(row=1, column=1)

        tk.Label(self.ventana,text="Numero de Simulaciones:").grid(row=2, column=0, padx=10, pady=10)
        self.textNumSimulaciones = tk.Entry(self.ventana)
        self.textNumSimulaciones.grid(row=2, column=1)

        # boton para ejecutar simulacion
        boton = tk.Button(self.ventana, text="Ejecutar Simulación", command=self.jugar)
        boton.grid(row=3, column=0, columnspan=2, pady=10)

        # para la grafica de los resultados
        self.textResultado = tk.Text(self.ventana, height=10, width=50)
        self.textResultado.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


        # Funcion para apostar y controlar los valores de capital inicial, meta, numero de simulaciones
        # tambien muestra los resultados 
    def jugar(self):

        self.textResultado.delete("1.0", tk.END)

        try:
            capitalInicial = float(self.textCapInicial.get())
            meta = float(self.textMeta.get())
            numSimulacion = int(self.textNumSimulaciones.get())

            exitos = 0

            for _ in range(numSimulacion):

                capital = capitalInicial
                apuesta = 10

                while capital > 0 and capital < meta:

                    if random.uniform(0,1) < 0.5:
                        capital += apuesta
                        apuesta = 10
                    else:
                        capital -= apuesta
                        apuesta *= 2

                if capital >= meta:
                    exitos += 1

            probabilidad = (exitos / numSimulacion) * 100

            # Mostrar resultados
            self.textResultado.insert(tk.END, "----- RESULTADOS -----\n")
            self.textResultado.insert(tk.END, f"Capital inicial: {capitalInicial} Bs\n")
            self.textResultado.insert(tk.END, f"Meta: {meta} Bs\n")
            self.textResultado.insert(tk.END, f"Simulaciones: {numSimulacion}\n")
            self.textResultado.insert(tk.END, f"Éxitos: {exitos}\n")
            self.textResultado.insert(tk.END, f"Probabilidad de éxito: {probabilidad:.2f}%\n")

        except ValueError:
            self.textResultado.insert(tk.END, " Ingrese valores numéricos válidos\n")

    def ejecutar(self):
        self.ventana.mainloop()


if __name__=="__main__":
    juego = JuegoDeApuestas()
    juego.ejecutar()  
    
