import tkinter as tk
from tkinter import messagebox
import random

# INTERFAZ GRÁFICA 
class JuegoDeApuestas:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Simulación de Juego de Apuestas")
        self.ventana.geometry("750x650")
        self.ventana.configure(bg="#EEF2F7")
        self.ventana.resizable(False, False)

        self.numApuestaBase = 10

        panel = tk.Frame(self.ventana, bg="#FFFFFF", bd=2, relief="groove")
        panel.pack(padx=25, pady=25, fill="both", expand=True)

        titulo = tk.Label(
            panel,
            text="Simulación de Juego de Apuestas",
            font=("Segoe UI", 18, "bold"),
            bg="#FFFFFF",
            fg="#2C3E50"
        )
        titulo.pack(pady=15)

        # grafica para las entradas
        frame_inputs = tk.LabelFrame(
            panel,
            text="Parámetros de Simulación",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#2471A3",
            padx=20,
            pady=15
        )
        frame_inputs.pack(padx=30, pady=15, fill="x")

        tk.Label(frame_inputs, text="Capital Inicial (Bs):", bg="#FFFFFF").grid(row=0, column=0, sticky="e", pady=8)
        self.textCapInicial = tk.Entry(frame_inputs, width=25)
        self.textCapInicial.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(frame_inputs, text="Meta a Alcanzar (Bs):", bg="#FFFFFF").grid(row=1, column=0, sticky="e", pady=8)
        self.textMeta = tk.Entry(frame_inputs, width=25)
        self.textMeta.grid(row=1, column=1, pady=8, padx=10)

        tk.Label(frame_inputs, text="Número de Simulaciones:", bg="#FFFFFF").grid(row=2, column=0, sticky="e", pady=8)
        self.textNumSimulaciones = tk.Entry(frame_inputs, width=25)
        self.textNumSimulaciones.grid(row=2, column=1, pady=8, padx=10)

        self.boton = tk.Button(
            panel,
            text="EJECUTAR SIMULACIÓN",
            font=("Segoe UI", 12, "bold"),
            bg="#3498DB",
            fg="white",
            activebackground="#2E86C1",
            activeforeground="white",
            padx=15,
            pady=10,
            command=self.jugar
        )
        self.boton.pack(pady=20)

        self.boton.bind("<Enter>", lambda e: self.boton.config(bg="#2E86C1"))
        self.boton.bind("<Leave>", lambda e: self.boton.config(bg="#3498DB"))

        # Grafica de resultados
        frame_resultados = tk.LabelFrame(
            panel,
            text="Reporte Estadístico",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#27AE60",
            padx=20,
            pady=15
        )
        frame_resultados.pack(padx=30, pady=15, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_resultados)
        scrollbar.pack(side="right", fill="y")

        self.textResultado = tk.Text(
            frame_resultados,
            height=20,              
            font=("Consolas", 11),
            bg="#F8F9F9",
            relief="flat",
            yscrollcommand=scrollbar.set,
            wrap="word"
        )
        self.textResultado.pack(fill="both", expand=True)
        scrollbar.config(command=self.textResultado.yview)


# LÓGICA DE SIMULACIÓN

    def jugar(self):

        self.textResultado.delete("1.0", tk.END)

        try:
            capitalInicial = float(self.textCapInicial.get())
            meta = float(self.textMeta.get())
            numSimulacion = int(self.textNumSimulaciones.get())

            if capitalInicial <= 0 or meta <= 0 or numSimulacion <= 0:
                messagebox.showerror("Error", "Todos los valores deben ser mayores a 0.")
                return

            if capitalInicial >= meta:
                messagebox.showerror("Error", "La meta debe ser mayor que el capital inicial.")
                return

            exitos = 0
            fracasos = 0

            for _ in range(numSimulacion):

                capital = capitalInicial
                apuesta = self.numApuestaBase

                while capital > 0 and capital < meta:
                    # donde se deside si pierde o gana(gana si el valor es < que 0.5)
                    if random.random() < 0.5:
                        capital += apuesta
                        apuesta = self.numApuestaBase
                    else:
                        capital -= apuesta
                        apuesta *= 2

                if capital >= meta:
                    exitos += 1
                else:
                    fracasos += 1

            probabilidad_exito = (exitos / numSimulacion) * 100
            probabilidad_fracaso = (fracasos / numSimulacion) * 100

            # REPORTE DE LOS RESULTADOS
            self.textResultado.insert(tk.END, "================= REPORTE DE SIMULACIÓN =================\n\n")

            self.textResultado.insert(tk.END, "📌 PARÁMETROS INICIALES\n")
            self.textResultado.insert(tk.END, f"Capital inicial:        {capitalInicial:,.2f} Bs\n")
            self.textResultado.insert(tk.END, f"Meta objetivo:          {meta:,.2f} Bs\n")
            self.textResultado.insert(tk.END, f"Total simulaciones:     {numSimulacion:,}\n\n")

            self.textResultado.insert(tk.END, "📊 RESULTADOS ESTADÍSTICOS\n")
            self.textResultado.insert(tk.END, f"Simulaciones exitosas:  {exitos:,}\n")
            self.textResultado.insert(tk.END, f"Simulaciones fallidas:  {fracasos:,}\n\n")

            self.textResultado.insert(tk.END, "📈 PROBABILIDADES\n")
            self.textResultado.insert(tk.END, f"Probabilidad de éxito:   {probabilidad_exito:.2f}%\n")
            self.textResultado.insert(tk.END, f"Probabilidad de fracaso: {probabilidad_fracaso:.2f}%\n\n")

            self.textResultado.insert(tk.END, " INTERPRETACIÓN\n")
            if probabilidad_exito > 50:
                self.textResultado.insert(tk.END, "La estrategia presenta alta probabilidad de alcanzar la meta.\n")
            else:
                self.textResultado.insert(tk.END, "La estrategia implica un riesgo considerable de perder el capital.\n")

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

# EJECUCIÓN
    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    juego = JuegoDeApuestas()
    juego.ejecutar()