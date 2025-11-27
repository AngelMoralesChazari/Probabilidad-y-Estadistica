import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DistribucionUniformeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribución Uniforme Continua U(a, b)")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f6f8fb")

        style = ttk.Style()
        style.theme_use("clam")

        main = tk.Frame(root, bg="#f6f8fb")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(
            main,
            text="Distribución Uniforme Continua U(a, b)",
            font=("Arial", 18, "bold"),
            bg="#f6f8fb",
            fg="#1f3b57"
        ).pack(pady=(0, 8))

        desc = (
            "La distribución uniforme continua en [a, b]:\n"
            "   PDF: f(x) = 1/(b-a) para a ≤ x ≤ b, 0 en otro caso.\n"
            "   CDF: F(x) = 0 (x < a), (x-a)/(b-a) (a ≤ x ≤ b), 1 (x > b).\n\n"
            "Usa los campos abajo para calcular probabilidades, cuantiles y ver los gráficos."
        )
        tk.Label(main, text=desc, font=("Arial", 10), bg="#f6f8fb", justify="left", wraplength=1000)\
            .pack(pady=(0, 12))

        # --- Inputs ---
        input_frame = tk.Frame(main, bg="#ffffff", bd=1, relief="solid")
        input_frame.pack(fill="x", padx=6, pady=6)

        tk.Label(input_frame, text="a (inicio):", bg="#ffffff").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.entry_a = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.entry_a.grid(row=0, column=1, padx=6, pady=8)
        self.entry_a.insert(0, "0")

        tk.Label(input_frame, text="b (fin):", bg="#ffffff").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.entry_b = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.entry_b.grid(row=0, column=3, padx=6, pady=8)
        self.entry_b.insert(0, "1")

        # Single x for P(X ≤ x)
        tk.Label(input_frame, text="x (P(X ≤ x)):", bg="#ffffff").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.entry_x = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.entry_x.grid(row=1, column=1, padx=6, pady=8)

        # Interval x1,x2 for P(x1 ≤ X ≤ x2)
        tk.Label(input_frame, text="x1 (intervalo):", bg="#ffffff").grid(row=1, column=2, padx=8, pady=8, sticky="w")
        self.entry_x1 = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.entry_x1.grid(row=1, column=3, padx=6, pady=8)

        tk.Label(input_frame, text="x2 (intervalo):", bg="#ffffff").grid(row=1, column=4, padx=8, pady=8, sticky="w")
        self.entry_x2 = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.entry_x2.grid(row=1, column=5, padx=6, pady=8)

        # Quantile
        tk.Label(input_frame, text="p (cuantil 0-1):", bg="#ffffff").grid(row=2, column=0, padx=8, pady=8, sticky="w")
        self.entry_p = tk.Entry(input_frame, width=12, font=("Arial", 11))
        self.entry_p.grid(row=2, column=1, padx=6, pady=8)

        # Buttons
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=2, columnspan=4, padx=6, pady=8, sticky="w")

        tk.Button(btn_frame, text="Calcular y Graficar", bg="#2e86c1", fg="white",
                  command=self.calcular_y_graficar, font=("Arial", 10, "bold")).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Ejemplo (a=0, b=10)", bg="#27ae60", fg="white",
                  command=self.ejemplo, font=("Arial", 10)).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Limpiar", bg="#c0392b", fg="white",
                  command=self.limpiar, font=("Arial", 10)).pack(side="left", padx=6)

        # --- Results area ---
        results_frame = tk.Frame(main, bg="#f6f8fb")
        results_frame.pack(fill="both", expand=True, padx=6, pady=6)

        left = tk.Frame(results_frame, bg="#ffffff", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        tk.Label(left, text="Resultados:", bg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=6)
        self.text_results = tk.Text(left, height=12, font=("Courier", 10), wrap="word")
        self.text_results.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        right = tk.Frame(results_frame, bg="#ffffff", bd=1, relief="solid")
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)

        # Two plot frames: PDF arriba, CDF abajo
        tk.Label(right, text="Gráficos (PDF y CDF):", bg="#ffffff", font=("Arial", 12, "bold"))\
            .pack(anchor="w", padx=8, pady=6)

        self.canvas_frame = tk.Frame(right, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def ejemplo(self):
        self.entry_a.delete(0, tk.END); self.entry_a.insert(0, "0")
        self.entry_b.delete(0, tk.END); self.entry_b.insert(0, "10")
        self.entry_x.delete(0, tk.END); self.entry_x.insert(0, "3.5")
        self.entry_x1.delete(0, tk.END); self.entry_x1.insert(0, "2")
        self.entry_x2.delete(0, tk.END); self.entry_x2.insert(0, "6")
        self.entry_p.delete(0, tk.END); self.entry_p.insert(0, "0.75")
        self.calcular_y_graficar()

    def limpiar(self):
        for e in (self.entry_a, self.entry_b, self.entry_x, self.entry_x1, self.entry_x2, self.entry_p):
            e.delete(0, tk.END)
        self.text_results.delete("1.0", tk.END)
        for w in self.canvas_frame.winfo_children():
            w.destroy()

    def calcular_y_graficar(self):
        # Leer y validar entradas
        try:
            a = float(self.entry_a.get().strip())
            b = float(self.entry_b.get().strip())
        except Exception:
            messagebox.showerror("Entrada inválida", "a y b deben ser números reales.")
            return

        if not (b > a):
            messagebox.showerror("Entrada inválida", "Se requiere b > a (intervalo válido).")
            return

        # leer opcionales
        x_val = None
        x1 = None
        x2 = None
        p = None
        try:
            if self.entry_x.get().strip() != "":
                x_val = float(self.entry_x.get().strip())
            if self.entry_x1.get().strip() != "":
                x1 = float(self.entry_x1.get().strip())
            if self.entry_x2.get().strip() != "":
                x2 = float(self.entry_x2.get().strip())
            # si ambos x1 y x2 están, asegurar orden
            if x1 is not None and x2 is not None and x2 < x1:
                # invierte automáticamente (facilita la entrada del alumno)
                x1, x2 = x2, x1
            if self.entry_p.get().strip() != "":
                p = float(self.entry_p.get().strip())
                if not (0 <= p <= 1):
                    raise ValueError("p debe estar entre 0 y 1.")
        except ValueError as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        # Parámetros teóricos
        mean = 0.5 * (a + b)
        var = ((b - a) ** 2) / 12.0
        sd = var ** 0.5

        # Probabilidades
        def cdf(u):
            if u < a:
                return 0.0
            elif u > b:
                return 1.0
            else:
                return (u - a) / (b - a)

        def pdf(u):
            return 1.0 / (b - a) if a <= u <= b else 0.0

        prob_x = None
        prob_interval = None
        cuantile = None
        if x_val is not None:
            prob_x = cdf(x_val)

        if x1 is not None and x2 is not None:
            # P(x1 <= X <= x2) = F(x2) - F(x1-) but para continua es F(x2) - F(x1)
            prob_interval = max(0.0, cdf(x2) - cdf(x1))

        if p is not None:
            # cuantile (inversa de CDF): q(p) = a + p*(b-a)
            cuantile = a + p * (b - a)

        # Mostrar resultados
        self.text_results.delete("1.0", tk.END)
        txt = f"Parámetros: a = {a}, b = {b}\n"
        txt += f"Media E[X] = (a + b) / 2 = {mean:.6f}\n"
        txt += f"Var(X) = (b - a)^2 / 12 = {var:.6f}\n"
        txt += f"Desviación estándar σ = {sd:.6f}\n\n"

        if x_val is not None:
            txt += f"P(X ≤ {x_val}) = F({x_val}) = {prob_x:.6f}\n"
        if x1 is not None and x2 is not None:
            txt += f"P({x1} ≤ X ≤ {x2}) = F({x2}) - F({x1}) = {prob_interval:.6f}\n"
        if p is not None:
            txt += f"Cuantil q(p={p}) = a + p·(b-a) = {cuantile:.6f}\n"
        if (x_val is None) and (x1 is None or x2 is None) and (p is None):
            txt += "Nota: introduce x, o x1 y x2, o p (cuantil) para cálculos adicionales.\n"

        txt += "\nObservaciones:\n"
        txt += " - P(X = x) para una variable continua es 0, la probabilidad se da por intervalos.\n"
        txt += " - Si alguno de los límites está fuera de [a, b], la F y las probabilidades se truncarán correctamente.\n"

        self.text_results.insert(tk.END, txt)

        # Dibujar gráficos (PDF y CDF) y sombrear área si corresponde
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 6), constrained_layout=True)
        xs = np.linspace(a - (b - a) * 0.2, b + (b - a) * 0.2, 800)  # algo de margen
        ys_pdf = np.array([pdf(x) for x in xs])
        ys_cdf = np.array([cdf(x) for x in xs])

        # PDF
        ax1.plot(xs, ys_pdf, color="#2c7fb8", lw=2)
        ax1.fill_between(xs, ys_pdf, color="#9fd3ff", alpha=0.6)
        ax1.set_title("PDF de U(a, b)")
        ax1.set_ylabel("f(x)")
        ax1.set_xlim(xs[0], xs[-1])
        ax1.grid(axis="y", linestyle="--", alpha=0.4)

        # Shade interval area on PDF if provided
        if x1 is not None and x2 is not None:
            xs_shade = np.linspace(x1, x2, 200)
            ys_shade = np.array([pdf(x) for x in xs_shade])
            ax1.fill_between(xs_shade, ys_shade, color="#ffbf80", alpha=0.7, label=f"P({x1}≤X≤{x2})")
            ax1.legend()

        # CDF
        ax2.plot(xs, ys_cdf, color="#2ca02c", lw=2)
        ax2.set_title("CDF de U(a, b)")
        ax2.set_ylabel("F(x)")
        ax2.set_xlabel("x")
        ax2.set_xlim(xs[0], xs[-1])
        ax2.grid(axis="y", linestyle="--", alpha=0.4)

        # Mark x (for P(X ≤ x))
        if x_val is not None:
            ax2.axvline(x_val, color="#c44e52", linestyle="--", lw=1.8, label=f"F({x_val})={prob_x:.3f}")
            ax2.scatter([x_val], [prob_x], color="#c44e52")
            ax2.legend()

        # Mark quantile on both plots
        if cuantile is not None:
            ax1.axvline(cuantile, color="#6a4a9a", linestyle=":", lw=1.8, label=f"q({p})={cuantil:.3f}" if False else f"q={cuantile:.3f}")
            ax2.axvline(cuantile, color="#6a4a9a", linestyle=":", lw=1.8)
            # annotate on CDF
            Fq = cdf(cuantile)
            ax2.scatter([cuantile], [Fq], color="#6a4a9a")
            ax2.annotate(f"q={cuantile:.3f}", xy=(cuantile, Fq), xytext=(8, -18), textcoords="offset points",
                         color="#6a4a9a", fontsize=9, bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8))

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = DistribucionUniformeApp(root)
    root.mainloop()