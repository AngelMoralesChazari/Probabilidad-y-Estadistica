import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
from scipy.stats import norm

class DistribucionNormal:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Distribución Normal - Campana de Gauss")
        self.raiz.geometry("1000x750")
        
        # Variables para los parámetros
        self.media = tk.DoubleVar(value=0)
        self.desviacion = tk.DoubleVar(value=1)
        self.probabilidad = tk.DoubleVar(value=0.95)
        self.limite_inferior = tk.DoubleVar(value=-1)
        self.limite_superior = tk.DoubleVar(value=1)
        
        self.crear_interfaz()
        self.actualizar_grafica()
    
    def crear_interfaz(self):
        # Marco principal
        marco_principal = ttk.Frame(self.raiz, padding="10")
        marco_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Marco de controles
        marco_controles = ttk.LabelFrame(marco_principal, text="Parámetros de la Distribución", padding="10")
        marco_controles.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Controles para media y desviación estándar
        ttk.Label(marco_controles, text="Media (μ):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Scale(marco_controles, from_=-5, to=5, variable=self.media, 
                 orient=tk.HORIZONTAL, command=self.actualizar_desde_deslizador).grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Entry(marco_controles, textvariable=self.media, width=8).grid(row=0, column=2, padx=(5, 0))
        
        ttk.Label(marco_controles, text="Desviación Estándar (σ):").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Scale(marco_controles, from_=0.1, to=3, variable=self.desviacion, 
                 orient=tk.HORIZONTAL, command=self.actualizar_desde_deslizador).grid(row=1, column=1, sticky=(tk.W, tk.E))
        ttk.Entry(marco_controles, textvariable=self.desviacion, width=8).grid(row=1, column=2, padx=(5, 0))
        
        # Marco para cálculos de probabilidad
        marco_probabilidad = ttk.LabelFrame(marco_principal, text="Cálculos de Probabilidad", padding="10")
        marco_probabilidad.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Probabilidad entre dos valores
        ttk.Label(marco_probabilidad, text="Límite Inferior:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(marco_probabilidad, textvariable=self.limite_inferior, width=8).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(marco_probabilidad, text="Límite Superior:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        ttk.Entry(marco_probabilidad, textvariable=self.limite_superior, width=8).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Button(marco_probabilidad, text="Calcular Probabilidad", 
                  command=self.calcular_probabilidad_rango).grid(row=0, column=4, padx=(10, 0))
        
        # Probabilidad acumulada
        ttk.Label(marco_probabilidad, text="Valor Z:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.valor_z = ttk.Entry(marco_probabilidad, width=8)
        self.valor_z.grid(row=1, column=1, padx=(0, 10))
        
        ttk.Button(marco_probabilidad, text="Probabilidad Acumulada (P(X ≤ z))", command=self.calcular_probabilidad_acumulada).grid(row=1, column=2, columnspan=2, padx=(0, 10))
        
        # Botones de acciones rápidas
        marco_acciones = ttk.Frame(marco_principal)
        marco_acciones.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(marco_acciones, text="Distribución Estándar (μ=0, σ=1)", 
                  command=self.establecer_estandar).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(marco_acciones, text="Área 1 Desviación Estándar", 
                  command=self.area_una_desviacion).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(marco_acciones, text="Área 2 Desviaciones Estándar", 
                  command=self.area_dos_desviaciones).pack(side=tk.LEFT, padx=(0, 5))
        
        # Marco para la gráfica
        marco_grafica = ttk.Frame(marco_principal)
        marco_grafica.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar la figura de matplotlib
        self.figura, self.eje = plt.subplots(figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.figura, marco_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar el grid para que se expanda
        marco_principal.columnconfigure(0, weight=1)
        marco_principal.rowconfigure(3, weight=1)
        marco_controles.columnconfigure(1, weight=1)
        marco_probabilidad.columnconfigure(1, weight=1)
    
    def actualizar_desde_deslizador(self, event=None):
        """Actualizar la gráfica cuando se mueven los deslizadores"""
        self.actualizar_grafica()
    
    def actualizar_grafica(self):
        """Actualizar la gráfica de la distribución normal"""
        self.eje.clear()
        
        media = self.media.get()
        desviacion = self.desviacion.get()
        
        # Generar puntos para la curva
        x = np.linspace(media - 4*desviacion, media + 4*desviacion, 1000)
        y = norm.pdf(x, media, desviacion)
        
        # Dibujar la curva
        self.eje.plot(x, y, 'b-', linewidth=2, label=f'N(μ={media}, σ={desviacion})')
        
        # Sombrear el área entre los límites
        limite_inf = self.limite_inferior.get()
        limite_sup = self.limite_superior.get()
        
        if limite_inf < limite_sup:
            mascara = (x >= limite_inf) & (x <= limite_sup)
            self.eje.fill_between(x[mascara], y[mascara], alpha=0.3, color='red', 
                                label=f'Área: {limite_inf} a {limite_sup}')
        
        # Configurar la gráfica
        self.eje.set_xlabel('Valores')
        self.eje.set_ylabel('Densidad de Probabilidad')
        self.eje.set_title('Distribución Normal - Campana de Gauss')
        self.eje.legend()
        self.eje.grid(True, alpha=0.3)
        
        self.canvas.draw()
    
    def calcular_probabilidad_rango(self):
        """Calcular la probabilidad entre dos valores"""
        try:
            media = self.media.get()
            desviacion = self.desviacion.get()
            limite_inf = self.limite_inferior.get()
            limite_sup = self.limite_superior.get()
            
            if limite_inf >= limite_sup:
                messagebox.showerror("Error", "El límite inferior debe ser menor al límite superior")
                return
            
            prob = norm.cdf(limite_sup, media, desviacion) - norm.cdf(limite_inf, media, desviacion)
            
            messagebox.showinfo("Resultado", 
                              f"P({limite_inf} ≤ X ≤ {limite_sup}) = {prob:.4f}\n"
                              f"({prob*100:.2f}% del área total)")
            
            self.actualizar_grafica()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def calcular_probabilidad_acumulada(self):
        """Calcular la probabilidad acumulada hasta un valor Z"""
        try:
            z = float(self.valor_z.get())
            media = self.media.get()
            desviacion = self.desviacion.get()
            
            prob = norm.cdf(z, media, desviacion)
            
            messagebox.showinfo("Resultado", 
                              f"P(X ≤ {z}) = {prob:.4f}\n"
                              f"({prob*100:.2f}% de los valores son ≤ {z})")
            
            # Actualizar límites para mostrar esta área
            self.limite_inferior.set(media - 4*desviacion)
            self.limite_superior.set(z)
            self.actualizar_grafica()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un valor Z numérico válido")
    
    def establecer_estandar(self):
        """Establecer la distribución normal estándar"""
        self.media.set(0)
        self.desviacion.set(1)
        self.limite_inferior.set(-1)
        self.limite_superior.set(1)
        self.actualizar_grafica()
    
    def area_una_desviacion(self):
        """Mostrar el área dentro de una desviación estándar"""
        media = self.media.get()
        desviacion = self.desviacion.get()
        self.limite_inferior.set(media - desviacion)
        self.limite_superior.set(media + desviacion)
        self.actualizar_grafica()
        
        # Calcular y mostrar la probabilidad
        prob = norm.cdf(media + desviacion, media, desviacion) - norm.cdf(media - desviacion, media, desviacion)
        messagebox.showinfo("Regla Empírica", 
                          f"Área dentro de 1σ: {prob:.4f}\n"
                          f"Aproximadamente 68.27% de los datos")
    
    def area_dos_desviaciones(self):
        """Mostrar el área dentro de dos desviaciones estándar"""
        media = self.media.get()
        desviacion = self.desviacion.get()
        self.limite_inferior.set(media - 2*desviacion)
        self.limite_superior.set(media + 2*desviacion)
        self.actualizar_grafica()
        
        # Calcular y mostrar la probabilidad
        prob = norm.cdf(media + 2*desviacion, media, desviacion) - norm.cdf(media - 2*desviacion, media, desviacion)
        messagebox.showinfo("Regla Empírica", 
                          f"Área dentro de 2σ: {prob:.4f}\n"
                          f"Aproximadamente 95.45% de los datos")

def main():
    raiz = tk.Tk()
    app = AplicacionDistribucionNormal(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()