import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QPushButton, QSpinBox, 
                             QGroupBox, QFormLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt

# =========================================================
# SECCIÓN 1: EL GRÁFICO (MANEJO DE MATPLOTLIB)
# =========================================================
class CanvasPi(FigureCanvas):
    """Clase para gestionar el área de dibujo"""
    def __init__(self, parent=None):
        # Crear la figura y los ejes (fondo blanco)
        self.fig, self.ax = plt.subplots(figsize=(5, 5), dpi=100, facecolor='#FFFFFF')
        super().__init__(self.fig)
        self.reset_plot()

    def reset_plot(self):
        """Limpia el gráfico y dibuja el arco base del cuadrante"""
        self.ax.clear()
        self.ax.set_xlim(0, 1) # Límites de 0 a 1 en eje X
        self.ax.set_ylim(0, 1) # Límites de 0 a 1 en eje Y
        self.ax.set_aspect('equal') # Mantiene la proporción cuadrada
        
        # Generar los puntos para dibujar el arco del círculo (curva negra)
        t = np.linspace(0, np.pi/2, 100)
        self.ax.plot(np.cos(t), np.sin(t), color='#2c3e50', linewidth=2)
        
        self.ax.set_facecolor('#FFFFFF')
        self.fig.tight_layout()

# =========================================================
# SECCIÓN 2: INTERFAZ DE USUARIO (GUI CON PYQT6)
# =========================================================
class AppEstimacionPi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estimador de Pi ")
        self.resize(1000, 650) 
        
        # Estilos CSS para mejorar la apariencia y visibilidad
        self.setStyleSheet("""
            QMainWindow { background-color: #F5F6FA; }
            QLabel { color: #2D3436; font-family: 'Segoe UI'; font-size: 14px; }
            QGroupBox { 
                font-weight: bold; color: #0984E3; 
                border: 1px solid #DCDDE1; border-radius: 10px; 
                margin-top: 10px; padding: 10px; background-color: #FFFFFF;
            }
            QSpinBox { 
                background-color: #FFFFFF; color: #000000; 
                border: 2px solid #74B9FF; padding: 5px; border-radius: 5px; 
            }
            /* Estilo de las flechas del contador para que siempre sean visibles */
            QSpinBox::up-button, QSpinBox::down-button { width: 20px; background: #F1F2F6; }
            QSpinBox::up-arrow { border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 4px solid #0984E3; }
            QSpinBox::down-arrow { border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 4px solid #0984E3; }
            
            QPushButton {
                background-color: #0984E3; color: white; font-weight: bold; 
                height: 40px; border-radius: 8px; font-size: 14px;
            }
            QPushButton:hover { background-color: #00A8FF; }
        """)

        # Configuración del widget central y layout principal
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_main = QHBoxLayout(widget_central)

        # --- PANEL IZQUIERDO: CONTROLES Y CONFIGURACIÓN ---
        panel_izq = QVBoxLayout()
        
        # Caja de entrada para el número de dardos (iteraciones)
        box_input = QGroupBox("Simulación")
        form = QFormLayout()
        self.input_n = QSpinBox()
        self.input_n.setRange(0, 10000000) # Rango hasta 10 millones
        self.input_n.setValue(10000)      # Valor por defecto
        self.input_n.setGroupSeparatorShown(True) # Muestra comas en miles
        # Conectar la tecla ENTER para ejecutar la simulación
        self.input_n.lineEdit().returnPressed.connect(self.ejecutar_simulacion) 
        
        form.addRow("Dardos:", self.input_n)
        box_input.setLayout(form)
        panel_izq.addWidget(box_input)

        # Botón para disparar la simulación manualmente
        self.btn = QPushButton("EJECUTAR")
        self.btn.clicked.connect(self.ejecutar_simulacion)
        panel_izq.addWidget(self.btn)

        # Caja de visualización de resultados numéricos
        box_res = QGroupBox("Resultados")
        res_vbox = QVBoxLayout()
        self.lbl_pi = QLabel("π estimado: --")
        self.lbl_pi.setStyleSheet("font-size: 26px; font-weight: bold; color: #27AE60;")

        self.lbl_real = QLabel("π real: 3.141592")
        self.lbl_puntos = QLabel("Puntos dentro: --")
        self.lbl_total = QLabel("Total dardos: --")

        self.lbl_error_abs = QLabel("Error absoluto: --")

        res_vbox.addWidget(self.lbl_pi)
        res_vbox.addWidget(self.lbl_real)
        res_vbox.addWidget(self.lbl_total)
        res_vbox.addWidget(self.lbl_puntos)
        res_vbox.addWidget(self.lbl_error_abs)

        box_res.setLayout(res_vbox)
        panel_izq.addWidget(box_res)

        panel_izq.addStretch() # Espacio flexible para empujar todo hacia arriba
        layout_main.addLayout(panel_izq, 1) # Proporción 1

        # --- PANEL DERECHO: ÁREA DE GRÁFICO ---
        self.canvas = CanvasPi(self)
        layout_main.addWidget(self.canvas, 2) # Proporción 2 (más ancho)

# =========================================================
# SECCIÓN 3: LÓGICA DE SIMULACIÓN Y MANEJO DE ERRORES
# =========================================================
    def mostrar_aviso_error(self):
        """Muestra una alerta estilizada y protegida contra minimización accidental"""
        alerta = QMessageBox(self)
        alerta.setWindowTitle("Aviso")
        alerta.setIcon(QMessageBox.Icon.Warning)
        alerta.setText("<b>Valor inválido</b>")
        alerta.setInformativeText("El número de dardos debe ser mayor a 0.")
        alerta.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Forzar banderas de ventana para que solo tenga el botón de cerrar (X)
        alerta.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.CustomizeWindowHint | 
            Qt.WindowType.WindowTitleHint | 
            Qt.WindowType.WindowCloseButtonHint
        )
        
        alerta.setStyleSheet("""
            QMessageBox { background-color: #FFFFFF; border: 1px solid #DCDDE1; }
            QLabel { color: #2D3436; font-size: 13px; }
            QPushButton { 
                background-color: #0984E3; color: white; 
                font-weight: bold; padding: 5px 25px; border-radius: 4px; 
            }
        """)
        alerta.exec()

    #funcion principal Inicio
    def ejecutar_simulacion(self):
        """Motor principal del cálculo de Pi """
        n = self.input_n.value()

        # Validación: No permitir 0 o negativos
        if n <= 0:
            self.mostrar_aviso_error()
            return

        try:
            # Desactivar botón durante el proceso
            self.btn.setEnabled(False)
            QApplication.processEvents() # Actualizar la interfaz

            # 1. Generar coordenadas aleatorias uniformes entre 0 y 1
            x = np.random.rand(n)
            y = np.random.rand(n)
            
            # 2. Condición: ¿Está el punto dentro del círculo? (x^2 + y^2 <= 1)
            dentro = (x**2 + y**2) <= 1
            puntos_dentro = np.sum(dentro)
            
            # 3. Estimar Pi usando la relación de áreas
            # Pi es aprox 4 * (Puntos_dentro / Total)
            pi_calc = 4 * (puntos_dentro / n)

            # 4. Actualizar textos en la interfaz
            error_abs = abs(pi_calc - np.pi)

            #Fin del algoritmo del calculo del PI

            self.lbl_pi.setText(f"π estimado: {pi_calc:.8f}")
            self.lbl_real.setText(f"π real: {np.pi:.8f}")
            self.lbl_total.setText(f"Total de dardos: {n:,}")
            self.lbl_puntos.setText(f"Puntos dentro del círculo: {puntos_dentro:,}")
            self.lbl_error_abs.setText(f"Error absoluto: {error_abs:.8f}")

            # 5. Actualizar el gráfico (limpiar y redibujar)
            self.canvas.reset_plot()
            
            # Límite de seguridad visual: No dibujar más de 10,000 puntos para no congelar la PC
            limite = 10000
            if n > limite:
                idx = np.random.choice(n, limite, replace=False) # Tomar muestra aleatoria
                self.canvas.ax.scatter(x[idx][dentro[idx]], y[idx][dentro[idx]], color='#3498DB', s=1, alpha=0.5)
                self.canvas.ax.scatter(x[idx][~dentro[idx]], y[idx][~dentro[idx]], color='#FF7675', s=1, alpha=0.5)
            else:
                self.canvas.ax.scatter(x[dentro], y[dentro], color='#3498DB', s=1, alpha=0.5)
                self.canvas.ax.scatter(x[~dentro], y[~dentro], color='#FF7675', s=1, alpha=0.5)
            
            self.canvas.draw() # Refrescar el lienzo de Matplotlib

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo inesperado: {str(e)}")
        finally:
            self.btn.setEnabled(True) # Reactivar botón al terminar

# =========================================================
# LANZAMIENTO DE LA APLICACIÓN
# =========================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Estilo moderno multiplataforma
    
    win = AppEstimacionPi()
    win.show()
    sys.exit(app.exec())