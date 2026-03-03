import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import math


class SimuladorPi:

    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Simulador Pi - Método Monte Carlo")
        self.ventana.geometry("500x400")

        self.init_components()

    def init_components(self):
        frame = tk.Frame(self.ventana, padx=10, pady=10)
        frame.pack(fill="x")

        tk.Label(frame, text="Número de corridas (n):").pack(anchor="w")

        self.txt_n = tk.Entry(frame)
        self.txt_n.insert(0, "1000000")
        self.txt_n.pack(fill="x")

        self.btn_simular = tk.Button(
            frame,
            text="Ejecutar Simulación",
            command=self.ejecutar_simulacion
        )
        self.btn_simular.pack(pady=5)

        self.txt_resultados = scrolledtext.ScrolledText(
            self.ventana,
            font=("Courier", 12)
        )
        self.txt_resultados.pack(fill="both", expand=True, padx=10, pady=10)

    # Funcion principal para seguir los pasos de la simulacion y control de las variables

    def ejecutar_simulacion(self):
        self.txt_resultados.delete("1.0", tk.END)

        try:
            n = int(self.txt_n.get())

            if n <= 0:
                messagebox.showerror("Error", "El número de corridas debe ser positivo.")
                return
            # contador de puntos dentro
            x = 0  

            # Repetir proceso n veces
            for _ in range(n):

                # 1. Generar R1 y R2 uniformes
                R1 = random.random()
                R2 = random.random()

                # 2. Calcular √(R1² + R2²)
                distancia = math.sqrt(R1**2 + R2**2)

                # 3 y 4. Verificar y contabilizar
                if distancia <= 1:
                    x += 1

            # 6. Calcular π estimado
            pi_estimado = 4 * x / n

            # Valor real de π
            pi_real = math.pi

            # Error absoluto
            error_absoluto = abs(pi_estimado - pi_real)

            # Mostrar resultados
            self.txt_resultados.insert(tk.END, "-------> RESULTADOS <-------\n\n")
            self.txt_resultados.insert(tk.END, f"Número de corridas (n): {n}\n")
            self.txt_resultados.insert(tk.END, f"Puntos dentro (x): {x}\n\n")
            self.txt_resultados.insert(tk.END, "π estimado = 4 * x / n\n")
            self.txt_resultados.insert(tk.END, f"π estimado: {pi_estimado:.10f}\n")
            self.txt_resultados.insert(tk.END, f"Valor real de π: {pi_real:.10f}\n")
            self.txt_resultados.insert(tk.END, f"Error absoluto: {error_absoluto:.10f}\n")

        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número válido.")


if __name__ == "__main__":
    calculoPi = tk.Tk()
    app = SimuladorPi(calculoPi)
    calculoPi.mainloop()