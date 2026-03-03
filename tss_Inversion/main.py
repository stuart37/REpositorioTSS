import sys
import numpy as np
import numpy_financial as npf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QDoubleSpinBox, 
                             QGroupBox, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt

# COMPONENTES DE VISUALIZACIÓN (GRÁFICOS)

class CanvasGrafico(FigureCanvas):
    """Clase para integrar Matplotlib dentro de la interfaz de PyQt6"""
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        super().__init__(self.fig)
        self.ax.set_title("Distribución de la TIR")
        self.fig.tight_layout()

# SECCIÓN 2: INTERFAZ DE USUARIO (UI)

class AppInversion(QMainWindow):
    def __init__(self):
        super().__init__()
        # 1. Configuración básica de la ventana
        self.setWindowTitle("Simulador de Inversión")
        self.setMinimumSize(1000, 700) 
        
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f6fa; }
            QLabel { color: #2f3640; font-size: 13px; }
            QGroupBox { 
                font-weight: bold; 
                color: #2f3640; 
                border: 2px solid #dcdde1; 
                border-radius: 8px; 
                margin-top: 15px; 
                padding-top: 10px;
            }
            QDoubleSpinBox { 
                background-color: white; 
                color: black; 
                border: 1px solid #bdc3c7; 
                padding: 5px; 
                border-radius: 4px; 
            }
        """)

        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QHBoxLayout(widget_central) # Horizontal: Controles | Gráfico

        # PANEL DE CONTROLES (IZQUIERDA) 
        panel_controles = QVBoxLayout()

        # Datos de Inversión
        self.grupo_inv = QGroupBox("1. Inversión Inicial (Triangular)")
        form_inv = QFormLayout()
        self.inv_min = self.crear_input(60000)
        self.inv_mod = self.crear_input(80000)
        self.inv_max = self.crear_input(100000)
        form_inv.addRow("Mínimo ($):", self.inv_min)
        form_inv.addRow("Probable ($):", self.inv_mod)
        form_inv.addRow("Máximo ($):", self.inv_max)
        self.grupo_inv.setLayout(form_inv)
        panel_controles.addWidget(self.grupo_inv)

        # Datos de Ingresos
        self.grupo_ing = QGroupBox("2. Ingresos Anuales Estimados")
        form_ing = QFormLayout()
        self.ing_min = self.crear_input(30000)
        self.ing_mod = self.crear_input(35000)
        self.ing_max = self.crear_input(45000)
        form_ing.addRow("Mínimo ($):", self.ing_min)
        form_ing.addRow("Probable ($):", self.ing_mod)
        form_ing.addRow("Máximo ($):", self.ing_max)
        self.grupo_ing.setLayout(form_ing)
        panel_controles.addWidget(self.grupo_ing)

        # Configuración Simulación
        self.grupo_sim = QGroupBox("3. Configuración")
        form_sim = QFormLayout()
        self.trema = self.crear_input(15, 0, 100)
        self.iteraciones = self.crear_input(1000, 1, 10000) # Mínimo forzado a 1
        form_sim.addRow("TREMA (%):", self.trema)
        form_sim.addRow("Nº Iteraciones:", self.iteraciones)
        self.grupo_sim.setLayout(form_sim)
        panel_controles.addWidget(self.grupo_sim)

        # Botón Ejecutar
        self.btn_ejecutar = QPushButton("EJECUTAR")
        self.btn_ejecutar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ejecutar.setStyleSheet("""
            QPushButton {
                background-color: #0984e3; 
                color: white; 
                font-weight: bold; 
                font-size: 14px; 
                height: 40px; 
                border-radius: 6px;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #74b9ff; }
        """)
        self.btn_ejecutar.clicked.connect(self.logica_principal)
        panel_controles.addWidget(self.btn_ejecutar)

        # Etiqueta de Resultados
        self.lbl_resultado = QLabel("Resultado: --")
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resultado.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            padding: 10px; 
            background-color: #dcdde1; 
            border-radius: 5px;
            color: #2f3640;
        """)
        panel_controles.addWidget(self.lbl_resultado)
        
        panel_controles.addStretch()
        layout_principal.addLayout(panel_controles, 1)

        # PANEL DE GRÁFICO (DERECHA)
        self.canvas = CanvasGrafico(self)
        layout_principal.addWidget(self.canvas, 2)

    def crear_input(self, val, mini=0, maxi=1000000):
        """Función auxiliar para crear SpinBoxes estándar"""
        sb = QDoubleSpinBox()
        sb.setRange(mini, maxi)
        sb.setValue(val)
        sb.setGroupSeparatorShown(True) 
        return sb

# LÓGICA DE NEGOCIO (FUNCIONALIDAD)

    def logica_principal(self):

        n = int(self.iteraciones.value())
        if n <= 0:
            QMessageBox.critical(self, "Error", "El número de iteraciones debe ser mayor a 0.")
            return

        if not (self.inv_min.value() <= self.inv_mod.value() <= self.inv_max.value()):
            QMessageBox.warning(self, "Datos Inválidos", "En Inversión: Mínimo ≤ Probable ≤ Máximo")
            return
        
        if not (self.ing_min.value() <= self.ing_mod.value() <= self.ing_max.value()):
            QMessageBox.warning(self, "Datos Inválidos", "En Ingresos: Mínimo ≤ Probable ≤ Máximo")
            return

        try:
            tirs_simuladas = []
            valor_trema = self.trema.value() / 100

            impuesto = 0.50
            vida = 5

            for _ in range(n):

                # Activo fijo y circulante
                activo_fijo = np.random.triangular(
                    self.inv_min.value(), 
                    self.inv_mod.value(), 
                    self.inv_max.value()
                )

                activo_circ = np.random.triangular(25000, 30000, 40000)

                inversion_total = -(activo_fijo + activo_circ)

                # Flujo antes de impuestos
                flujo_base = np.random.triangular(
                    self.ing_min.value(), 
                    self.ing_mod.value(), 
                    self.ing_max.value()
                )

                flujos = [inversion_total]

                for año in range(1, vida + 1):

                    # Inflación triangular por año
                    inflacion = np.random.triangular(0.12, 0.15, 0.18)
                    flujo_ajustado = flujo_base * ((1 + inflacion) ** año)

                    flujo_neto = flujo_ajustado * (1 - impuesto)

                    flujos.append(flujo_neto)

                # Valor de rescate (20%)
                valor_rescate = activo_fijo * 0.20
                flujos[-1] += valor_rescate

                # Recuperación del circulante
                flujos[-1] += activo_circ

                tir = npf.irr(flujos)

                if tir is not None and not np.isnan(tir):
                    tirs_simuladas.append(tir)

            if tirs_simuladas:

                tir_min = min(tirs_simuladas)
                tir_max = max(tirs_simuladas)
                tir_prom = np.mean(tirs_simuladas)

                exitos = [t for t in tirs_simuladas if t > valor_trema]
                probabilidad = (len(exitos) / len(tirs_simuladas)) * 100

                self.lbl_resultado.setText(
                    f"TIR Min: {tir_min*100:.2f}% | "
                    f"TIR Prom: {tir_prom*100:.2f}% | "
                    f"TIR Max: {tir_max*100:.2f}%\n"
                    f"Probabilidad TIR > TREMA: {probabilidad:.2f}%"
                )

                self.dibujar_histograma(tirs_simuladas, valor_trema)

            else:
                QMessageBox.warning(self, "Sin Resultados", "No se pudo calcular la TIR.")

        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", str(e))

    def dibujar_histograma(self, datos, corte):
        """Actualiza el gráfico de Matplotlib"""
        self.canvas.ax.clear()
        self.canvas.ax.hist(datos, bins=40, color='#3498db', edgecolor='white', alpha=0.7)
        self.canvas.ax.axvline(corte, color='#e74c3c', linestyle='--', linewidth=2, label='TREMA')
        self.canvas.ax.set_title("Resultados de Simulación")
        self.canvas.ax.set_xlabel("TIR")
        self.canvas.ax.set_ylabel("Frecuencia")
        self.canvas.ax.legend()
        self.canvas.draw()

# EJECUCIÓN

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AppInversion()
    ventana.show()
    sys.exit(app.exec())