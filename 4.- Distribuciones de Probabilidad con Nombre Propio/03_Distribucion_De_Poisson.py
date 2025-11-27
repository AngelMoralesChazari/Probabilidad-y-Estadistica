import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
from scipy.stats import poisson

class AplicacionPoisson:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Distribución de Poisson - Calculadora y Visualización")
        self.raiz.geometry("1200x800")
        
        # Configurar fuentes
        self.fuente_grande = ('Arial', 12)
        self.fuente_mediana = ('Arial', 11)
        self.fuente_titulo = ('Arial', 14, 'bold')
        
        # Variables
        self.lambda_val = tk.DoubleVar(value=2.0)
        self.n_ensayos = tk.IntVar(value=100)
        self.p_exito = tk.DoubleVar(value=0.02)
        self.k_valor = tk.IntVar(value=2)
        self.tipo_probabilidad = tk.StringVar(value="=")
        self.k_minimo = tk.IntVar(value=2)
        self.k_maximo = tk.IntVar(value=5)
        
        # Almacenar referencias a los entries
        self.entries = {}
        
        self.crear_interfaz()
        self.actualizar_grafica()
    
    def crear_interfaz(self):
        # Marco principal
        marco_principal = ttk.Frame(self.raiz, padding="15")
        marco_principal.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Controles
        panel_controles = ttk.Frame(marco_principal, width=400)
        panel_controles.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        panel_controles.pack_propagate(False)
        
        # Panel derecho - Gráfica
        panel_grafica = ttk.Frame(marco_principal)
        panel_grafica.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # ===== PANEL DE CONTROLES =====
        
        # Sección: Distribución Poisson Directa
        marco_poisson = ttk.LabelFrame(panel_controles, text="Distribución Poisson Directa", padding="10")
        marco_poisson.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(marco_poisson, text="λ (Lambda - Tasa promedio):", font=self.fuente_mediana).pack(anchor=tk.W)
        ttk.Scale(marco_poisson, from_=0.1, to=20, variable=self.lambda_val, 
                 orient=tk.HORIZONTAL, command=self.actualizar_desde_control).pack(fill=tk.X, pady=5)
        frame_lambda = ttk.Frame(marco_poisson)
        frame_lambda.pack(fill=tk.X)
        self.entries['lambda'] = ttk.Entry(frame_lambda, textvariable=self.lambda_val, width=10, font=self.fuente_mediana)
        self.entries['lambda'].pack(side=tk.LEFT)
        ttk.Label(frame_lambda, text="(0.1 - 20)", font=('Arial', 9)).pack(side=tk.LEFT, padx=(5,0))
        
        # Tipo de probabilidad
        ttk.Label(marco_poisson, text="Tipo de probabilidad:", font=self.fuente_mediana).pack(anchor=tk.W, pady=(10,5))
        frame_tipo = ttk.Frame(marco_poisson)
        frame_tipo.pack(fill=tk.X)
        
        ttk.Radiobutton(frame_tipo, text="P(X = k)", variable=self.tipo_probabilidad, 
                       value="=", command=self.actualizar_controles).pack(side=tk.LEFT)
        ttk.Radiobutton(frame_tipo, text="P(X ≤ k)", variable=self.tipo_probabilidad, 
                       value="<=", command=self.actualizar_controles).pack(side=tk.LEFT, padx=(10,0))
        ttk.Radiobutton(frame_tipo, text="P(X ≥ k)", variable=self.tipo_probabilidad, 
                       value=">=", command=self.actualizar_controles).pack(side=tk.LEFT, padx=(10,0))
        
        # Valor k
        ttk.Label(marco_poisson, text="Valor de k:", font=self.fuente_mediana).pack(anchor=tk.W, pady=(10,5))
        ttk.Scale(marco_poisson, from_=0, to=20, variable=self.k_valor, 
                 orient=tk.HORIZONTAL, command=self.actualizar_desde_control).pack(fill=tk.X)
        self.entries['k_valor'] = ttk.Entry(marco_poisson, textvariable=self.k_valor, width=10, font=self.fuente_mediana)
        self.entries['k_valor'].pack(anchor=tk.W, pady=5)
        
        # Sección: Aproximación Poisson de Binomial
        marco_binomial = ttk.LabelFrame(panel_controles, text="Aproximación Poisson de Binomial", padding="10")
        marco_binomial.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(marco_binomial, text="n (Número de ensayos):", font=self.fuente_mediana).pack(anchor=tk.W)
        ttk.Scale(marco_binomial, from_=10, to=500, variable=self.n_ensayos, 
                 orient=tk.HORIZONTAL, command=self.actualizar_aproximacion).pack(fill=tk.X, pady=5)
        self.entries['n_ensayos'] = ttk.Entry(marco_binomial, textvariable=self.n_ensayos, width=10, font=self.fuente_mediana)
        self.entries['n_ensayos'].pack(anchor=tk.W)
        
        ttk.Label(marco_binomial, text="p (Probabilidad de éxito):", font=self.fuente_mediana).pack(anchor=tk.W, pady=(10,0))
        ttk.Scale(marco_binomial, from_=0.001, to=0.1, variable=self.p_exito, 
                 orient=tk.HORIZONTAL, command=self.actualizar_aproximacion).pack(fill=tk.X, pady=5)
        self.entries['p_exito'] = ttk.Entry(marco_binomial, textvariable=self.p_exito, width=10, font=self.fuente_mediana)
        self.entries['p_exito'].pack(anchor=tk.W)
        
        # Sección: Rango para probabilidad acumulada
        marco_rango = ttk.LabelFrame(panel_controles, text="Probabilidad en Rango", padding="10")
        marco_rango.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(marco_rango, text="k mínimo:", font=self.fuente_mediana).pack(anchor=tk.W)
        ttk.Scale(marco_rango, from_=0, to=20, variable=self.k_minimo, 
                 orient=tk.HORIZONTAL, command=self.actualizar_desde_control).pack(fill=tk.X, pady=5)
        self.entries['k_minimo'] = ttk.Entry(marco_rango, textvariable=self.k_minimo, width=10, font=self.fuente_mediana)
        self.entries['k_minimo'].pack(anchor=tk.W)
        
        ttk.Label(marco_rango, text="k máximo:", font=self.fuente_mediana).pack(anchor=tk.W, pady=(10,0))
        ttk.Scale(marco_rango, from_=0, to=20, variable=self.k_maximo, 
                 orient=tk.HORIZONTAL, command=self.actualizar_desde_control).pack(fill=tk.X, pady=5)
        self.entries['k_maximo'] = ttk.Entry(marco_rango, textvariable=self.k_maximo, width=10, font=self.fuente_mediana)
        self.entries['k_maximo'].pack(anchor=tk.W)
        
        # Botones de acción
        marco_botones = ttk.Frame(panel_controles)
        marco_botones.pack(fill=tk.X, pady=(10,0))
        
        ttk.Button(marco_botones, text="Calcular Probabilidad", 
                  command=self.calcular_probabilidad).pack(fill=tk.X, pady=2)
        ttk.Button(marco_botones, text="Calcular Rango", 
                  command=self.calcular_rango).pack(fill=tk.X, pady=2)
        ttk.Button(marco_botones, text="Calcular Aproximación", 
                  command=self.calcular_aproximacion).pack(fill=tk.X, pady=2)
        ttk.Button(marco_botones, text="Limpiar Gráfica", 
                  command=self.actualizar_grafica).pack(fill=tk.X, pady=2)
        
        # Área de resultados
        self.marco_resultados = ttk.LabelFrame(panel_controles, text="Resultados", padding="10")
        self.marco_resultados.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
        self.texto_resultados = tk.Text(self.marco_resultados, height=15, width=45, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(self.marco_resultados, orient=tk.VERTICAL, command=self.texto_resultados.yview)
        self.texto_resultados.configure(yscrollcommand=scrollbar.set)
        self.texto_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ===== PANEL DE GRÁFICA =====
        self.figura, self.eje = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figura, panel_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar eventos
        self.configurar_eventos()
        self.actualizar_controles()
    
    def configurar_eventos(self):
        # Configurar eventos para todos los entries
        for entry_name, entry_widget in self.entries.items():
            entry_widget.bind('<KeyRelease>', self.actualizar_con_retraso)
    
    def actualizar_con_retraso(self, event=None):
        if hasattr(self, '_after_id'):
            self.raiz.after_cancel(self._after_id)
        self._after_id = self.raiz.after(500, self.actualizar_grafica)
    
    def actualizar_desde_control(self, event=None):
        self.actualizar_grafica()
    
    def actualizar_controles(self):
        self.actualizar_grafica()
    
    def actualizar_aproximacion(self, event=None):
        try:
            n = self.n_ensayos.get()
            p = self.p_exito.get()
            lambda_aprox = n * p
            self.lambda_val.set(round(lambda_aprox, 2))
            self.actualizar_grafica()
        except:
            pass
    
    def actualizar_grafica(self):
        try:
            self.eje.clear()
            lambda_val = self.lambda_val.get()
            k_valor = self.k_valor.get()
            
            # Generar datos para la distribución
            k_max_plot = min(int(lambda_val * 3) + 5, 50)
            k_values = np.arange(0, k_max_plot + 1)
            prob_values = poisson.pmf(k_values, lambda_val)
            
            # Graficar distribución completa
            self.eje.bar(k_values, prob_values, alpha=0.7, color='skyblue', 
                        label=f'Poisson(λ={lambda_val:.2f})', width=0.8)
            
            # Resaltar probabilidad según el tipo seleccionado
            color_resaltar = 'red'
            label_added = False
            
            if self.tipo_probabilidad.get() == "=":
                if k_valor <= k_max_plot:
                    prob_k = poisson.pmf(k_valor, lambda_val)
                    self.eje.bar(k_valor, prob_k, color=color_resaltar, alpha=0.9, 
                               width=0.8, label=f'P(X = {k_valor})')
                    label_added = True
            
            elif self.tipo_probabilidad.get() == "<=":
                mask = k_values <= k_valor
                k_resaltar = k_values[mask]
                prob_resaltar = prob_values[mask]
                if len(k_resaltar) > 0:
                    self.eje.bar(k_resaltar, prob_resaltar, color=color_resaltar, alpha=0.9,
                               width=0.8, label=f'P(X ≤ {k_valor})')
                    label_added = True
            
            elif self.tipo_probabilidad.get() == ">=":
                mask = k_values >= k_valor
                k_resaltar = k_values[mask]
                prob_resaltar = prob_values[mask]
                if len(k_resaltar) > 0:
                    self.eje.bar(k_resaltar, prob_resaltar, color=color_resaltar, alpha=0.9,
                               width=0.8, label=f'P(X ≥ {k_valor})')
                    label_added = True
            
            # Configurar gráfica
            self.eje.set_xlabel('k (Número de eventos)', fontsize=12)
            self.eje.set_ylabel('Probabilidad P(X=k)', fontsize=12)
            self.eje.set_title(f'Distribución de Poisson - λ = {lambda_val:.2f}', 
                             fontsize=14, fontweight='bold')
            self.eje.legend()
            self.eje.grid(True, alpha=0.3)
            
            # Ajustar ticks del eje x
            if k_max_plot > 20:
                self.eje.set_xticks(k_values[::max(2, k_max_plot//10)])
            else:
                self.eje.set_xticks(k_values)
            
            self.eje.set_ylim(0, max(prob_values) * 1.1)
            
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error al actualizar gráfica: {e}")
    
    def calcular_probabilidad(self):
        try:
            lambda_val = self.lambda_val.get()
            k = self.k_valor.get()
            tipo = self.tipo_probabilidad.get()
            
            resultado = ""
            
            if tipo == "=":
                prob = poisson.pmf(k, lambda_val)
                resultado = f"POISSON DIRECTA\n{'='*40}\n"
                resultado += f"λ (lambda) = {lambda_val:.4f}\n"
                resultado += f"k = {k}\n"
                resultado += f"P(X = {k}) = {prob:.6f}\n"
                resultado += f"→ {prob*100:.4f}%\n\n"
                resultado += f"Fórmula: e^(-{lambda_val:.4f}) × {lambda_val:.4f}² / {k}!"
                
            elif tipo == "<=":
                prob = poisson.cdf(k, lambda_val)
                resultado = f"POISSON ACUMULADA\n{'='*40}\n"
                resultado += f"λ (lambda) = {lambda_val:.4f}\n"
                resultado += f"k máximo = {k}\n"
                resultado += f"P(X ≤ {k}) = {prob:.6f}\n"
                resultado += f"→ {prob*100:.4f}%\n\n"
                resultado += "Desglose:\n"
                for i in range(k + 1):
                    p_i = poisson.pmf(i, lambda_val)
                    resultado += f"P(X = {i}) = {p_i:.6f}\n"
                
            elif tipo == ">=":
                prob_complemento = poisson.cdf(k - 1, lambda_val) if k > 0 else 0
                prob = 1 - prob_complemento
                resultado = f"POISSON COMPLEMENTO\n{'='*40}\n"
                resultado += f"λ (lambda) = {lambda_val:.4f}\n"
                resultado += f"k mínimo = {k}\n"
                resultado += f"P(X ≥ {k}) = {prob:.6f}\n"
                resultado += f"→ {prob*100:.4f}%\n\n"
                if k > 0:
                    resultado += f"Cálculo: 1 - P(X ≤ {k-1})\n"
                    resultado += f"P(X ≤ {k-1}) = {prob_complemento:.6f}"
                else:
                    resultado += "P(X ≥ 0) = 1.0 (siempre verdadero)"
            
            self.mostrar_resultados(resultado)
            self.actualizar_grafica()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {e}")
    
    def calcular_rango(self):
        try:
            lambda_val = self.lambda_val.get()
            k_min = self.k_minimo.get()
            k_max = self.k_maximo.get()
            
            if k_min > k_max:
                messagebox.showerror("Error", "k mínimo debe ser menor o igual a k máximo")
                return
            
            prob_acum = 0
            resultado = f"PROBABILIDAD EN RANGO\n{'='*40}\n"
            resultado += f"λ (lambda) = {lambda_val:.4f}\n"
            resultado += f"Rango: {k_min} ≤ X ≤ {k_max}\n\n"
            resultado += "Desglose:\n"
            
            for k in range(k_min, k_max + 1):
                prob_k = poisson.pmf(k, lambda_val)
                prob_acum += prob_k
                resultado += f"P(X = {k}) = {prob_k:.6f}\n"
            
            resultado += f"\nTOTAL: P({k_min} ≤ X ≤ {k_max}) = {prob_acum:.6f}\n"
            resultado += f"→ {prob_acum*100:.4f}%"
            
            self.mostrar_resultados(resultado)
            self.actualizar_grafica()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo de rango: {e}")
    
    def calcular_aproximacion(self):
        try:
            n = self.n_ensayos.get()
            p = self.p_exito.get()
            k = self.k_valor.get()
            lambda_aprox = n * p
            
            resultado = f"APROXIMACIÓN POISSON DE BINOMIAL\n{'='*50}\n"
            resultado += f"Parámetros binomiales:\n"
            resultado += f"  n = {n} (ensayos)\n"
            resultado += f"  p = {p:.4f} (prob. éxito)\n"
            resultado += f"  k = {k} (éxitos deseados)\n"
            resultado += f"  λ = n × p = {lambda_aprox:.4f}\n\n"
            
            # Verificar condiciones
            resultado += "Condiciones para aproximación:\n"
            condiciones_ok = True
            
            if n >= 30:
                resultado += f"  ✅ n = {n} ≥ 30\n"
            else:
                resultado += f"  ⚠️  n = {n} < 30 (ideal: n ≥ 30)\n"
                condiciones_ok = False
                
            if p <= 0.1:
                resultado += f"  ✅ p = {p:.4f} ≤ 0.1\n"
            else:
                resultado += f"  ⚠️  p = {p:.4f} > 0.1 (ideal: p ≤ 0.1)\n"
                condiciones_ok = False
                
            if lambda_aprox <= 20:
                resultado += f"  ✅ λ = {lambda_aprox:.4f} ≤ 20\n"
            else:
                resultado += f"  ⚠️  λ = {lambda_aprox:.4f} > 20 (considerar normal)\n"
            
            # Cálculos
            prob_poisson = poisson.pmf(k, lambda_aprox)
            resultado += f"\nRESULTADOS:\n"
            resultado += f"Probabilidad Poisson: P(X = {k}) = {prob_poisson:.6f}\n"
            
            # Cálculo binomial exacto (si es posible)
            try:
                from scipy.special import comb
                prob_binomial = comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
                resultado += f"Probabilidad Binomial: = {prob_binomial:.6f}\n"
                diferencia = abs(prob_poisson - prob_binomial)
                resultado += f"Diferencia: {diferencia:.6f}\n"
                if prob_binomial > 0:
                    error_relativo = diferencia / prob_binomial * 100
                    resultado += f"Error relativo: {error_relativo:.2f}%"
                else:
                    resultado += "Error relativo: N/A"
            except:
                resultado += "\n⚠️ No se pudo calcular binomial exacta (n muy grande)"
            
            if condiciones_ok and lambda_aprox <= 20:
                resultado += f"\n\n✅ Condiciones adecuadas para aproximación Poisson"
            else:
                resultado += f"\n\n⚠️  Condiciones no ideales para aproximación Poisson"
            
            self.mostrar_resultados(resultado)
            self.actualizar_grafica()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en aproximación: {e}")
    
    def mostrar_resultados(self, texto):
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(1.0, texto)

def main():
    raiz = tk.Tk()
    app = AplicacionPoisson(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()