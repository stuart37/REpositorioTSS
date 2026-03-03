import tkinter as tk
from tkinter import messagebox
import random

class JuegoApuestasV2:

    def __init__(self):

        self.ventana = tk.Tk()
        self.ventana.title("Simulador de Juego de Apuestas")
        self.ventana.geometry("600x600")

        # ----- PANEL SUPERIOR -----
        frame = tk.Frame(self.ventana)
        frame.pack(pady=10)

        tk.Label(frame, text="Capital Inicial:").grid(row=0, column=0, padx=10, pady=5)
        self.txtCapital = tk.Entry(frame)
        self.txtCapital.grid(row=0, column=1)

        tk.Label(frame, text="Meta a Alcanzar:").grid(row=1, column=0, padx=10, pady=5)
        self.txtMeta = tk.Entry(frame)
        self.txtMeta.grid(row=1, column=1)

        tk.Label(frame, text="Número de Simulaciones:").grid(row=2, column=0, padx=10, pady=5)
        self.txtSimulaciones = tk.Entry(frame)
        self.txtSimulaciones.grid(row=2, column=1)

        btnSimular = tk.Button(frame, text="Ejecutar Simulación", command=self.ejecutarSimulacion)
        btnSimular.grid(row=3, column=0, pady=10)

        btnPasoAPaso = tk.Button(frame, text="Simulación Paso a Paso", command=self.simulacionPasoAPaso)
        btnPasoAPaso.grid(row=3, column=1, pady=10)

        # ----- ÁREA DE RESULTADOS CON SCROLL -----
        scroll = tk.Scrollbar(self.ventana)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.txtResultado = tk.Text(self.ventana, yscrollcommand=scroll.set)
        self.txtResultado.pack(expand=True, fill=tk.BOTH)

        scroll.config(command=self.txtResultado.yview)

    # =============================
    # EJECUTAR SIMULACIÓN COMPLETA
    # =============================
    def ejecutarSimulacion(self):

        self.txtResultado.delete("1.0", tk.END)

        try:
            capitalInicial = float(self.txtCapital.get())
            meta = float(self.txtMeta.get())
            nSim = int(self.txtSimulaciones.get())

            if capitalInicial <= 0 or meta <= capitalInicial or nSim <= 0:
                self.txtResultado.insert(tk.END, "⚠ Error: Valores inválidos.\n")
                return

            exitos = 0

            for _ in range(nSim):

                capital = capitalInicial

                while capital > 0 and capital < meta:
                    if random.random() > 0.5:
                        capital *= 2
                    else:
                        capital = 0

                if capital >= meta:
                    exitos += 1

            probabilidad = exitos / nSim

            self.txtResultado.insert(tk.END, "=== RESULTADOS ===\n")
            self.txtResultado.insert(tk.END, f"Capital inicial: ${capitalInicial}\n")
            self.txtResultado.insert(tk.END, f"Meta: ${meta}\n")
            self.txtResultado.insert(tk.END, f"Simulaciones: {nSim}\n")
            self.txtResultado.insert(tk.END, f"Éxitos: {exitos}\n")
            self.txtResultado.insert(tk.END, f"Probabilidad de éxito: {probabilidad*100:.2f}%\n")

            if exitos > 0:
                intentosProm = nSim / exitos
                self.txtResultado.insert(tk.END, f"Intentos promedio por éxito: {intentosProm:.1f}\n")

        except:
            self.txtResultado.insert(tk.END, "⚠ Error: Verifique que los datos sean válidos.\n")

    # =============================
    # SIMULACIÓN PASO A PASO
    # =============================
    def simulacionPasoAPaso(self):

        self.txtResultado.delete("1.0", tk.END)

        try:
            capitalInicial = float(self.txtCapital.get())
            meta = float(self.txtMeta.get())

            if capitalInicial <= 0 or meta <= capitalInicial:
                self.txtResultado.insert(tk.END, "⚠ Error: Valores inválidos.\n")
                return

            capital = capitalInicial
            ronda = 1

            self.txtResultado.insert(tk.END, "=== SIMULACIÓN PASO A PASO ===\n")

            while capital > 0 and capital < meta:

                gana = random.random() > 0.5

                if gana:
                    capital *= 2
                    self.txtResultado.insert(tk.END, f"Ronda {ronda}: GANA | Capital: ${capital}\n")
                else:
                    capital = 0
                    self.txtResultado.insert(tk.END, f"Ronda {ronda}: PIERDE | Capital: $0\n")

                ronda += 1

            self.txtResultado.insert(tk.END, f"\nResultado final: ${capital}\n")

        except:
            self.txtResultado.insert(tk.END, "⚠ Error: Datos no válidos.\n")

    def ejecutar(self):
        self.ventana.mainloop()


# ========= MAIN =========
if __name__ == "__main__":
    app = JuegoApuestasV2()
    app.ejecutar()