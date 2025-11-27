import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from math import factorial, exp, comb


class DistribucionesDiscretasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribuciones de Probabilidad Discretas")
        self.root.geometry("1150x800")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            main_frame,
            text="Distribuciones de Probabilidad de Variables Aleatorias Discretas",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        # Notebook con 3 pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)

        self.tab_binomial = tk.Frame(self.notebook, bg="#fff5f5")
        self.tab_poisson = tk.Frame(self.notebook, bg="#f5fff5")
        self.tab_geometrica = tk.Frame(self.notebook, bg="#f5f5ff")

        self.notebook.add(self.tab_binomial, text="1. Binomial")
        self.notebook.add(self.tab_poisson, text="2. Poisson")
        self.notebook.add(self.tab_geometrica, text="3. Geométrica")

        self.crear_tab_binomial()
        self.crear_tab_poisson()
        self.crear_tab_geometrica()

    # ===================== BINOMIAL =====================

    def crear_tab_binomial(self):
        frame = self.tab_binomial

        tk.Label(
            frame,
            text="Distribución Binomial: X ~ B(n, p)",
            font=("Arial", 16, "bold"),
            bg="#fff5f5",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            frame,
            text="Número de éxitos en n ensayos independientes, cada uno con probabilidad p de éxito.",
            font=("Arial", 11),
            bg="#fff5f5",
            fg="#34495e",
            wraplength=1000
        ).pack(pady=(0, 10))

        # Entradas
        input_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            input_frame,
            text="n (número de ensayos):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.entry_n_binom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_n_binom.grid(row=0, column=1, padx=5, pady=8)
        self.entry_n_binom.insert(0, "10")

        tk.Label(
            input_frame,
            text="p (probabilidad de éxito):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

        self.entry_p_binom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_p_binom.grid(row=0, column=3, padx=5, pady=8)
        self.entry_p_binom.insert(0, "0.5")

        tk.Label(
            input_frame,
            text="k (valor específico para P(X=k)):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.entry_k_binom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_k_binom.grid(row=1, column=1, padx=5, pady=8)
        self.entry_k_binom.insert(0, "5")

        tk.Label(
            input_frame,
            text="k₂ (para P(X ≤ k₂)):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=2, padx=10, pady=8, sticky="w")

        self.entry_k2_binom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_k2_binom.grid(row=1, column=3, padx=5, pady=8)
        self.entry_k2_binom.insert(0, "7")

        # Botones
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_frame,
            text="Calcular y Graficar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_binomial
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo: 10 monedas",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_binomial
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar_binomial
        ).pack(side="left", padx=5)

        # Resultados
        results_frame = tk.Frame(frame, bg="#fff5f5")
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Resultados (Binomial):",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.text_binom = tk.Text(left_frame, height=12, font=("Courier", 10), wrap="word")
        self.text_binom.pack(fill="both", expand=True, padx=5, pady=5)

        # Tabla
        tk.Label(
            left_frame,
            text="Tabla de probabilidades:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.tree_binom = ttk.Treeview(
            left_frame,
            columns=("k", "P(X=k)", "P(X≤k)"),
            show="headings",
            height=8
        )
        self.tree_binom.heading("k", text="k")
        self.tree_binom.heading("P(X=k)", text="P(X=k)")
        self.tree_binom.heading("P(X≤k)", text="P(X≤k)")

        self.tree_binom.column("k", width=60, anchor="center")
        self.tree_binom.column("P(X=k)", width=100, anchor="center")
        self.tree_binom.column("P(X≤k)", width=100, anchor="center")

        self.tree_binom.pack(fill="both", expand=True, padx=5, pady=5)

        # Gráfico
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="Gráfico FMP (Binomial)",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_binom_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_binom_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def ejemplo_binomial(self):
        self.entry_n_binom.delete(0, tk.END)
        self.entry_p_binom.delete(0, tk.END)
        self.entry_k_binom.delete(0, tk.END)
        self.entry_k2_binom.delete(0, tk.END)

        self.entry_n_binom.insert(0, "10")
        self.entry_p_binom.insert(0, "0.5")
        self.entry_k_binom.insert(0, "5")
        self.entry_k2_binom.insert(0, "7")

        self.calcular_binomial()

    def limpiar_binomial(self):
        self.entry_n_binom.delete(0, tk.END)
        self.entry_p_binom.delete(0, tk.END)
        self.entry_k_binom.delete(0, tk.END)
        self.entry_k2_binom.delete(0, tk.END)

        self.text_binom.delete("1.0", tk.END)
        self.tree_binom.delete(*self.tree_binom.get_children())
        for w in self.canvas_binom_frame.winfo_children():
            w.destroy()

    def calcular_binomial(self):
        try:
            n = int(self.entry_n_binom.get())
            p = float(self.entry_p_binom.get())
            k = int(self.entry_k_binom.get())
            k2 = int(self.entry_k2_binom.get())

            if n <= 0:
                raise ValueError("n debe ser > 0")
            if not (0 <= p <= 1):
                raise ValueError("p debe estar entre 0 y 1")
            if k < 0 or k > n:
                raise ValueError("k debe estar entre 0 y n")
            if k2 < 0 or k2 > n:
                raise ValueError("k₂ debe estar entre 0 y n")
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        # Calcular probabilidades
        def binom_pmf(n, p, k):
            return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

        prob_k = binom_pmf(n, p, k)
        prob_acum_k2 = sum(binom_pmf(n, p, i) for i in range(k2 + 1))

        media = n * p
        varianza = n * p * (1 - p)
        desv = varianza ** 0.5

        # Texto
        self.text_binom.delete("1.0", tk.END)
        txt = f"Distribución: X ~ Binomial(n={n}, p={p:.4f})\n\n"
        txt += f"Media E[X] = n·p = {media:.4f}\n"
        txt += f"Varianza Var(X) = n·p·(1-p) = {varianza:.4f}\n"
        txt += f"Desviación estándar σ = {desv:.4f}\n\n"
        txt += f"P(X = {k}) = C({n},{k}) · p^{k} · (1-p)^{n-k}\n"
        txt += f"           = {prob_k:.6f}\n\n"
        txt += f"P(X ≤ {k2}) = Σ P(X=i) para i=0..{k2}\n"
        txt += f"            = {prob_acum_k2:.6f}\n"
        self.text_binom.insert(tk.END, txt)

        # Tabla
        self.tree_binom.delete(*self.tree_binom.get_children())
        acum = 0.0
        for i in range(n + 1):
            pi = binom_pmf(n, p, i)
            acum += pi
            self.tree_binom.insert("", "end", values=(i, f"{pi:.6f}", f"{acum:.6f}"))

        # Gráfico
        self.dibujar_grafico_binomial(n, p)

    def dibujar_grafico_binomial(self, n, p):
        for w in self.canvas_binom_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 4))
        fig.patch.set_facecolor("#ffffff")

        x_vals = list(range(n + 1))
        y_vals = [comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in x_vals]

        ax.bar(x_vals, y_vals, color="#e74c3c", width=0.6)
        ax.set_xlabel("k (número de éxitos)")
        ax.set_ylabel("P(X=k)")
        ax.set_title(f"Binomial(n={n}, p={p:.2f})")
        ax.set_ylim(0, max(y_vals) * 1.2)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_binom_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ===================== POISSON =====================

    def crear_tab_poisson(self):
        frame = self.tab_poisson

        tk.Label(
            frame,
            text="Distribución de Poisson: X ~ Poisson(λ)",
            font=("Arial", 16, "bold"),
            bg="#f5fff5",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            frame,
            text="Número de eventos en un intervalo de tiempo/espacio, con tasa promedio λ.",
            font=("Arial", 11),
            bg="#f5fff5",
            fg="#34495e",
            wraplength=1000
        ).pack(pady=(0, 10))

        # Entradas
        input_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            input_frame,
            text="λ (tasa promedio):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.entry_lambda_poisson = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_lambda_poisson.grid(row=0, column=1, padx=5, pady=8)
        self.entry_lambda_poisson.insert(0, "3")

        tk.Label(
            input_frame,
            text="k (valor específico para P(X=k)):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

        self.entry_k_poisson = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_k_poisson.grid(row=0, column=3, padx=5, pady=8)
        self.entry_k_poisson.insert(0, "2")

        tk.Label(
            input_frame,
            text="k₂ (para P(X ≤ k₂)):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.entry_k2_poisson = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_k2_poisson.grid(row=1, column=1, padx=5, pady=8)
        self.entry_k2_poisson.insert(0, "5")

        # Botones
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_frame,
            text="Calcular y Graficar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_poisson
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo: λ=3",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_poisson
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar_poisson
        ).pack(side="left", padx=5)

        # Resultados
        results_frame = tk.Frame(frame, bg="#f5fff5")
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Resultados (Poisson):",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.text_poisson = tk.Text(left_frame, height=12, font=("Courier", 10), wrap="word")
        self.text_poisson.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Tabla de probabilidades:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.tree_poisson = ttk.Treeview(
            left_frame,
            columns=("k", "P(X=k)", "P(X≤k)"),
            show="headings",
            height=8
        )
        self.tree_poisson.heading("k", text="k")
        self.tree_poisson.heading("P(X=k)", text="P(X=k)")
        self.tree_poisson.heading("P(X≤k)", text="P(X≤k)")

        self.tree_poisson.column("k", width=60, anchor="center")
        self.tree_poisson.column("P(X=k)", width=100, anchor="center")
        self.tree_poisson.column("P(X≤k)", width=100, anchor="center")

        self.tree_poisson.pack(fill="both", expand=True, padx=5, pady=5)

        # Gráfico
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="Gráfico FMP (Poisson)",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_poisson_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_poisson_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def ejemplo_poisson(self):
        self.entry_lambda_poisson.delete(0, tk.END)
        self.entry_k_poisson.delete(0, tk.END)
        self.entry_k2_poisson.delete(0, tk.END)

        self.entry_lambda_poisson.insert(0, "3")
        self.entry_k_poisson.insert(0, "2")
        self.entry_k2_poisson.insert(0, "5")

        self.calcular_poisson()

    def limpiar_poisson(self):
        self.entry_lambda_poisson.delete(0, tk.END)
        self.entry_k_poisson.delete(0, tk.END)
        self.entry_k2_poisson.delete(0, tk.END)

        self.text_poisson.delete("1.0", tk.END)
        self.tree_poisson.delete(*self.tree_poisson.get_children())
        for w in self.canvas_poisson_frame.winfo_children():
            w.destroy()

    def calcular_poisson(self):
        try:
            lam = float(self.entry_lambda_poisson.get())
            k = int(self.entry_k_poisson.get())
            k2 = int(self.entry_k2_poisson.get())

            if lam <= 0:
                raise ValueError("λ debe ser > 0")
            if k < 0:
                raise ValueError("k debe ser ≥ 0")
            if k2 < 0:
                raise ValueError("k₂ debe ser ≥ 0")
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        def poisson_pmf(lam, k):
            return (lam ** k) * exp(-lam) / factorial(k)

        prob_k = poisson_pmf(lam, k)
        
        # Calcular hasta k2 o un límite razonable
        max_k = max(k2, int(lam + 5 * lam ** 0.5)) + 10
        prob_acum_k2 = sum(poisson_pmf(lam, i) for i in range(k2 + 1))

        media = lam
        varianza = lam
        desv = lam ** 0.5

        # Texto
        self.text_poisson.delete("1.0", tk.END)
        txt = f"Distribución: X ~ Poisson(λ={lam:.4f})\n\n"
        txt += f"Media E[X] = λ = {media:.4f}\n"
        txt += f"Varianza Var(X) = λ = {varianza:.4f}\n"
        txt += f"Desviación estándar σ = {desv:.4f}\n\n"
        txt += f"P(X = {k}) = (λ^{k} · e^(-λ)) / {k}!\n"
        txt += f"           = {prob_k:.6f}\n\n"
        txt += f"P(X ≤ {k2}) = Σ P(X=i) para i=0..{k2}\n"
        txt += f"            = {prob_acum_k2:.6f}\n"
        self.text_poisson.insert(tk.END, txt)

        # Tabla (hasta un límite razonable)
        self.tree_poisson.delete(*self.tree_poisson.get_children())
        acum = 0.0
        limite_tabla = min(max_k, 30)
        for i in range(limite_tabla):
            pi = poisson_pmf(lam, i)
            acum += pi
            self.tree_poisson.insert("", "end", values=(i, f"{pi:.6f}", f"{acum:.6f}"))

        # Gráfico
        self.dibujar_grafico_poisson(lam, max_k)

    def dibujar_grafico_poisson(self, lam, max_k):
        for w in self.canvas_poisson_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 4))
        fig.patch.set_facecolor("#ffffff")

        limite_grafico = min(max_k, 25)
        x_vals = list(range(limite_grafico))
        y_vals = [(lam ** k) * exp(-lam) / factorial(k) for k in x_vals]

        ax.bar(x_vals, y_vals, color="#27ae60", width=0.6)
        ax.set_xlabel("k (número de eventos)")
        ax.set_ylabel("P(X=k)")
        ax.set_title(f"Poisson(λ={lam:.2f})")
        ax.set_ylim(0, max(y_vals) * 1.2 if y_vals else 1)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_poisson_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ===================== GEOMÉTRICA =====================

    def crear_tab_geometrica(self):
        frame = self.tab_geometrica

        tk.Label(
            frame,
            text="Distribución Geométrica: X ~ Geom(p)",
            font=("Arial", 16, "bold"),
            bg="#f5f5ff",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            frame,
            text="Número de ensayos hasta el primer éxito (incluyendo el éxito). P(X=k) = (1-p)^(k-1) · p",
            font=("Arial", 11),
            bg="#f5f5ff",
            fg="#34495e",
            wraplength=1000
        ).pack(pady=(0, 10))

        # Entradas
        input_frame = tk.Frame(frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            input_frame,
            text="p (probabilidad de éxito):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.entry_p_geom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_p_geom.grid(row=0, column=1, padx=5, pady=8)
        self.entry_p_geom.insert(0, "0.3")

        tk.Label(
            input_frame,
            text="k (valor específico para P(X=k)):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

        self.entry_k_geom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_k_geom.grid(row=0, column=3, padx=5, pady=8)
        self.entry_k_geom.insert(0, "3")

        tk.Label(
            input_frame,
            text="k₂ (para P(X ≤ k₂)):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.entry_k2_geom = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_k2_geom.grid(row=1, column=1, padx=5, pady=8)
        self.entry_k2_geom.insert(0, "5")

        # Botones
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_frame,
            text="Calcular y Graficar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_geometrica
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo: p=0.3",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_geometrica
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar_geometrica
        ).pack(side="left", padx=5)

        # Resultados
        results_frame = tk.Frame(frame, bg="#f5f5ff")
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Resultados (Geométrica):",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.text_geom = tk.Text(left_frame, height=12, font=("Courier", 10), wrap="word")
        self.text_geom.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Tabla de probabilidades:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.tree_geom = ttk.Treeview(
            left_frame,
            columns=("k", "P(X=k)", "P(X≤k)"),
            show="headings",
            height=8
        )
        self.tree_geom.heading("k", text="k")
        self.tree_geom.heading("P(X=k)", text="P(X=k)")
        self.tree_geom.heading("P(X≤k)", text="P(X≤k)")

        self.tree_geom.column("k", width=60, anchor="center")
        self.tree_geom.column("P(X=k)", width=100, anchor="center")
        self.tree_geom.column("P(X≤k)", width=100, anchor="center")

        self.tree_geom.pack(fill="both", expand=True, padx=5, pady=5)

        # Gráfico
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="Gráfico FMP (Geométrica)",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_geom_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_geom_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def ejemplo_geometrica(self):
        self.entry_p_geom.delete(0, tk.END)
        self.entry_k_geom.delete(0, tk.END)
        self.entry_k2_geom.delete(0, tk.END)

        self.entry_p_geom.insert(0, "0.3")
        self.entry_k_geom.insert(0, "3")
        self.entry_k2_geom.insert(0, "5")

        self.calcular_geometrica()

    def limpiar_geometrica(self):
        self.entry_p_geom.delete(0, tk.END)
        self.entry_k_geom.delete(0, tk.END)
        self.entry_k2_geom.delete(0, tk.END)

        self.text_geom.delete("1.0", tk.END)
        self.tree_geom.delete(*self.tree_geom.get_children())
        for w in self.canvas_geom_frame.winfo_children():
            w.destroy()

    def calcular_geometrica(self):
        try:
            p = float(self.entry_p_geom.get())
            k = int(self.entry_k_geom.get())
            k2 = int(self.entry_k2_geom.get())

            if not (0 < p <= 1):
                raise ValueError("p debe estar entre 0 y 1 (exclusivo 0)")
            if k < 1:
                raise ValueError("k debe ser ≥ 1")
            if k2 < 1:
                raise ValueError("k₂ debe ser ≥ 1")
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        def geom_pmf(p, k):
            return ((1 - p) ** (k - 1)) * p

        prob_k = geom_pmf(p, k)
        prob_acum_k2 = sum(geom_pmf(p, i) for i in range(1, k2 + 1))

        media = 1.0 / p
        varianza = (1 - p) / (p ** 2)
        desv = varianza ** 0.5

        # Texto
        self.text_geom.delete("1.0", tk.END)
        txt = f"Distribución: X ~ Geométrica(p={p:.4f})\n\n"
        txt += f"Media E[X] = 1/p = {media:.4f}\n"
        txt += f"Varianza Var(X) = (1-p)/p² = {varianza:.4f}\n"
        txt += f"Desviación estándar σ = {desv:.4f}\n\n"
        txt += f"P(X = {k}) = (1-p)^({k}-1) · p\n"
        txt += f"           = {prob_k:.6f}\n\n"
        txt += f"P(X ≤ {k2}) = Σ P(X=i) para i=1..{k2}\n"
        txt += f"            = {prob_acum_k2:.6f}\n"
        self.text_geom.insert(tk.END, txt)

        # Tabla
        self.tree_geom.delete(*self.tree_geom.get_children())
        acum = 0.0
        limite_tabla = max(k2, int(media + 3 * desv)) + 5
        limite_tabla = min(limite_tabla, 30)
        for i in range(1, limite_tabla + 1):
            pi = geom_pmf(p, i)
            acum += pi
            self.tree_geom.insert("", "end", values=(i, f"{pi:.6f}", f"{acum:.6f}"))

        # Gráfico
        self.dibujar_grafico_geometrica(p, limite_tabla)

    def dibujar_grafico_geometrica(self, p, max_k):
        for w in self.canvas_geom_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 4))
        fig.patch.set_facecolor("#ffffff")

        x_vals = list(range(1, max_k + 1))
        y_vals = [((1 - p) ** (k - 1)) * p for k in x_vals]

        ax.bar(x_vals, y_vals, color="#9b59b6", width=0.6)
        ax.set_xlabel("k (número de ensayos hasta el primer éxito)")
        ax.set_ylabel("P(X=k)")
        ax.set_title(f"Geométrica(p={p:.2f})")
        ax.set_ylim(0, max(y_vals) * 1.2 if y_vals else 1)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_geom_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = DistribucionesDiscretasApp(root)
    root.mainloop()