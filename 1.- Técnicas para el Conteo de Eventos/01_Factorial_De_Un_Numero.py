import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class FactorialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Factorial de un Número - Probabilidad y Estadística")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = tk.Frame(root, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Título
        title_label = tk.Label(main_frame, text="🧮 Calculadora de Factorial", 
                               font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Frame de entrada
        input_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        input_frame.pack(pady=10, padx=10, fill='x')
        
        tk.Label(input_frame, text="Ingresa un número (0-20):", 
                font=('Arial', 12), bg='#ffffff').pack(side='left', padx=10, pady=10)
        
        self.entry_numero = tk.Entry(input_frame, font=('Arial', 12), width=10)
        self.entry_numero.pack(side='left', padx=5, pady=10)
        self.entry_numero.bind('<Return>', lambda e: self.calcular_factorial())
        
        btn_calcular = tk.Button(input_frame, text="Calcular", 
                                command=self.calcular_factorial,
                                bg='#3498db', fg='white', 
                                font=('Arial', 11, 'bold'),
                                cursor='hand2', padx=20)
        btn_calcular.pack(side='left', padx=10, pady=10)
        
        btn_limpiar = tk.Button(input_frame, text="Limpiar", 
                               command=self.limpiar,
                               bg='#e74c3c', fg='white', 
                               font=('Arial', 11, 'bold'),
                               cursor='hand2', padx=20)
        btn_limpiar.pack(side='left', padx=5, pady=10)
        
        # Frame de resultados
        results_frame = tk.Frame(main_frame, bg='#ffffff', relief='raised', bd=2)
        results_frame.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Resultado principal
        self.label_resultado = tk.Label(results_frame, text="", 
                                       font=('Arial', 16, 'bold'), 
                                       bg='#ffffff', fg='#27ae60')
        self.label_resultado.pack(pady=10)
        
        # Frame para tabla y gráfica
        content_frame = tk.Frame(results_frame, bg='#ffffff')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame izquierdo - Tabla y proceso
        left_frame = tk.Frame(content_frame, bg='#ffffff')
        left_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Proceso paso a paso
        tk.Label(left_frame, text="📝 Proceso de Cálculo:", 
                font=('Arial', 11, 'bold'), bg='#ffffff').pack(anchor='w', pady=5)
        
        self.text_proceso = tk.Text(left_frame, height=8, width=35, 
                                   font=('Courier', 10), wrap='word')
        self.text_proceso.pack(fill='both', expand=True)
        
        scrollbar_proceso = tk.Scrollbar(left_frame, command=self.text_proceso.yview)
        self.text_proceso.config(yscrollcommand=scrollbar_proceso.set)
        
        # Tabla de valores
        tk.Label(left_frame, text="📋 Tabla de Factoriales:", 
                font=('Arial', 11, 'bold'), bg='#ffffff').pack(anchor='w', pady=(10,5))
        
        # Frame para la tabla con scrollbar
        table_frame = tk.Frame(left_frame)
        table_frame.pack(fill='both', expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=('n', 'factorial'), 
                                show='headings', height=8)
        self.tree.heading('n', text='n')
        self.tree.heading('factorial', text='n!')
        self.tree.column('n', width=50, anchor='center')
        self.tree.column('factorial', width=150, anchor='center')
        
        scrollbar_table = tk.Scrollbar(table_frame, orient='vertical', 
                                      command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_table.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar_table.pack(side='right', fill='y')
        
        # Frame derecho - Gráfica
        right_frame = tk.Frame(content_frame, bg='#ffffff')
        right_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        tk.Label(right_frame, text="📈 Gráfica de Crecimiento:", 
                font=('Arial', 11, 'bold'), bg='#ffffff').pack(pady=5)
        
        self.canvas_frame = tk.Frame(right_frame, bg='#ffffff')
        self.canvas_frame.pack(fill='both', expand=True)
        
        # Información adicional
        info_frame = tk.Frame(main_frame, bg='#e8f4f8', relief='solid', bd=1)
        info_frame.pack(pady=10, padx=10, fill='x')
        
        info_text = """ℹ️ El factorial de un número n (n!) es el producto de todos los números enteros positivos desde 1 hasta n.
        Ejemplo: 5! = 5 × 4 × 3 × 2 × 1 = 120  |  Por definición: 0! = 1"""
        
        tk.Label(info_frame, text=info_text, font=('Arial', 9), 
                bg='#e8f4f8', fg='#34495e', justify='left').pack(padx=10, pady=8)
    
    def calcular_factorial(self):
        try:
            n = int(self.entry_numero.get())
            
            if n < 0:
                messagebox.showerror("Error", "El factorial no está definido para números negativos")
                return
            
            if n > 20:
                messagebox.showwarning("Advertencia", 
                                      "Número muy grande. Se limitará a 20 para mejor visualización")
                n = 20
                self.entry_numero.delete(0, tk.END)
                self.entry_numero.insert(0, "20")
            
            # Calcular factorial
            resultado = math.factorial(n)
            
            # Mostrar resultado principal
            self.label_resultado.config(text=f"✨ {n}! = {resultado:,}")
            
            # Mostrar proceso paso a paso
            self.text_proceso.delete(1.0, tk.END)
            if n == 0:
                self.text_proceso.insert(tk.END, "Por definición:\n0! = 1")
            else:
                proceso = f"{n}! = "
                factores = " × ".join([str(i) for i in range(n, 0, -1)])
                proceso += factores + f"\n\n"
                
                # Cálculo paso a paso
                proceso += "Cálculo paso a paso:\n"
                acumulado = 1
                for i in range(1, n+1):
                    acumulado *= i
                    proceso += f"{i}! = {acumulado:,}\n"
                
                self.text_proceso.insert(tk.END, proceso)
            
            # Llenar tabla
            self.tree.delete(*self.tree.get_children())
            for i in range(n+1):
                fact = math.factorial(i)
                self.tree.insert('', 'end', values=(i, f"{fact:,}"))
            
            # Crear gráfica
            self.crear_grafica(n)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número entero válido")
    
    def crear_grafica(self, n):
        # Limpiar canvas anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        fig.patch.set_facecolor('#ffffff')
        
        # Datos
        x = list(range(n+1))
        y = [math.factorial(i) for i in x]
        
        # Gráfica lineal
        ax1.plot(x, y, marker='o', linewidth=2, markersize=6, 
                color='#3498db', markerfacecolor='#e74c3c')
        ax1.set_xlabel('n', fontsize=10, fontweight='bold')
        ax1.set_ylabel('n!', fontsize=10, fontweight='bold')
        ax1.set_title('Crecimiento del Factorial', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#f8f9fa')
        
        # Gráfica de barras
        ax2.bar(x, y, color='#2ecc71', alpha=0.7, edgecolor='#27ae60', linewidth=1.5)
        ax2.set_xlabel('n', fontsize=10, fontweight='bold')
        ax2.set_ylabel('n!', fontsize=10, fontweight='bold')
        ax2.set_title('Comparación de Valores', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_facecolor('#f8f9fa')
        
        plt.tight_layout()
        
        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def limpiar(self):
        self.entry_numero.delete(0, tk.END)
        self.label_resultado.config(text="")
        self.text_proceso.delete(1.0, tk.END)
        self.tree.delete(*self.tree.get_children())
        
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FactorialApp(root)
    root.mainloop()