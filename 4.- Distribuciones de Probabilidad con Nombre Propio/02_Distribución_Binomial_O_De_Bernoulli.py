import tkinter as tk
from tkinter import ttk, messagebox
from math import comb, factorial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BernoulliBinomialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Distribución Bernoulli y Binomial")
        self.root.geometry("1100x720")
        self.root.configure(bg="#f5f7fa")

        style = ttk.Style()
        style.theme_use("clam")

        header = tk.Label(root, text="Distribuciones: Bernoulli y Binomial",
                          font=("Arial", 16, "bold"), bg="#f5f7fa")
        header.pack(pady=8)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=6)

        self.tab_bernoulli = tk.Frame(notebook, bg="#fffaf0")
        self.tab_binomial = tk.Frame(notebook, bg="#f0fff5")

        notebook.add(self.tab_bernoulli, text="Bernoulli (p)")
        notebook.add(self.tab_binomial, text="Binomial (n, p)")

        self._crear_tab_bernoulli()
        self._crear_tab_binomial()

    # ------------------- Bernoulli -------------------
    def _crear_tab_bernoulli(self):
        f = self.tab_bernoulli
        tk.Label(f, text="Distribución Bernoulli: X ∈ {0,1}", font=("Arial", 13, "bold"),
                 bg="#fffaf0").pack(pady=6)

        frame = tk.Frame(f, bg="#ffffff", bd=1, relief="solid")
        frame.pack(fill="x", padx=10, pady=8)

        tk.Label(frame, text="p (probabilidad de éxito, P(X=1)):", bg="#ffffff").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.entry_p_ber = tk.Entry(frame, width=12, font=("Arial", 11))
        self.entry_p_ber.grid(row=0, column=1, padx=6, pady=8)
        self.entry_p_ber.insert(0, "0.5")

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=0, column=2, padx=8)

        tk.Button(btn_frame, text="Calcular y Graficar", bg="#27ae60", fg="white",
                  command=self.calcular_bernoulli).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Ejemplo p=0.3", bg="#3498db", fg="white",
                  command=self.ejemplo_bernoulli).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Limpiar", bg="#e74c3c", fg="white",
                  command=self.limpiar_bernoulli).pack(side="left", padx=4)

        results_frame = tk.Frame(f, bg="#fffaf0")
        results_frame.pack(fill="both", expand=True, padx=10, pady=6)

        left = tk.Frame(results_frame, bg="#ffffff", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(left, text="Resultados (Bernoulli):", bg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=6)
        self.text_ber = tk.Text(left, height=10, font=("Courier", 10))
        self.text_ber.pack(fill="both", expand=True, padx=8, pady=(0,8))

        right = tk.Frame(results_frame, bg="#ffffff", bd=1, relief="solid")
        right.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(right, text="Gráfico P(X):", bg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=6)
        self.canvas_ber_frame = tk.Frame(right, bg="#ffffff")
        self.canvas_ber_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def ejemplo_bernoulli(self):
        self.entry_p_ber.delete(0, tk.END); self.entry_p_ber.insert(0, "0.3")
        self.calcular_bernoulli()

    def limpiar_bernoulli(self):
        self.entry_p_ber.delete(0, tk.END)
        self.text_ber.delete("1.0", tk.END)
        for w in self.canvas_ber_frame.winfo_children():
            w.destroy()

    def calcular_bernoulli(self):
        try:
            p = float(self.entry_p_ber.get())
            if not (0 <= p <= 1):
                raise ValueError("p debe estar entre 0 y 1")
        except Exception as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        p0 = 1 - p
        mean = p
        var = p * (1 - p)
        sd = var ** 0.5

        self.text_ber.delete("1.0", tk.END)
        txt = f"Distribución Bernoulli(p={p:.4f})\n\n"
        txt += f"P(X=1) = p = {p:.6f}\n"
        txt += f"P(X=0) = 1 - p = {p0:.6f}\n\n"
        txt += f"Media E[X] = p = {mean:.6f}\n"
        txt += f"Var(X) = p(1-p) = {var:.6f}\n"
        txt += f"Desviación estándar σ = {sd:.6f}\n"
        self.text_ber.insert(tk.END, txt)

        # Gráfico
        for w in self.canvas_ber_frame.winfo_children():
            w.destroy()
        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        xs = [0, 1]
        ys = [p0, p]
        bars = ax.bar(xs, ys, color=["#3498db", "#e74c3c"], width=0.5)
        ax.set_xticks(xs); ax.set_xticklabels(["0", "1"])
        ax.set_ylabel("P(X=x)")
        ax.set_title(f"Bernoulli(p={p:.2f})")
        ax.set_ylim(0, 1)
        for i, v in enumerate(ys):
            ax.text(xs[i], v + 0.03, f"{v:.3f}", ha="center")
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_ber_frame)
        canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)

    # ------------------- Binomial -------------------
    def _crear_tab_binomial(self):
        f = self.tab_binomial
        tk.Label(f, text="Distribución Binomial: X ~ Binomial(n, p)", font=("Arial", 13, "bold"),
                 bg="#f0fff5").pack(pady=6)

        frame = tk.Frame(f, bg="#ffffff", bd=1, relief="solid")
        frame.pack(fill="x", padx=10, pady=8)

        tk.Label(frame, text="n (ensayos):", bg="#ffffff").grid(row=0, column=0, padx=6, pady=8, sticky="w")
        self.entry_n = tk.Entry(frame, width=10, font=("Arial", 11))
        self.entry_n.grid(row=0, column=1, padx=6, pady=8)
        self.entry_n.insert(0, "10")

        tk.Label(frame, text="p (éxito):", bg="#ffffff").grid(row=0, column=2, padx=6, pady=8, sticky="w")
        self.entry_p = tk.Entry(frame, width=10, font=("Arial", 11))
        self.entry_p.grid(row=0, column=3, padx=6, pady=8)
        self.entry_p.insert(0, "0.5")

        tk.Label(frame, text="k (P(X=k)):", bg="#ffffff").grid(row=1, column=0, padx=6, pady=8, sticky="w")
        self.entry_k = tk.Entry(frame, width=10, font=("Arial", 11))
        self.entry_k.grid(row=1, column=1, padx=6, pady=8)
        self.entry_k.insert(0, "5")

        tk.Label(frame, text="k2 (P(X ≤ k2)):", bg="#ffffff").grid(row=1, column=2, padx=6, pady=8, sticky="w")
        self.entry_k2 = tk.Entry(frame, width=10, font=("Arial", 11))
        self.entry_k2.grid(row=1, column=3, padx=6, pady=8)
        self.entry_k2.insert(0, "7")

        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=6)

        tk.Button(btn_frame, text="Calcular y Graficar", bg="#27ae60", fg="white", command=self.calcular_binomial).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Ejemplo: n=10, p=0.5", bg="#3498db", fg="white", command=self.ejemplo_binomial).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Limpiar", bg="#e74c3c", fg="white", command=self.limpiar_binomial).pack(side="left", padx=4)

        results_frame = tk.Frame(f, bg="#f0fff5")
        results_frame.pack(fill="both", expand=True, padx=10, pady=6)

        left = tk.Frame(results_frame, bg="#ffffff", bd=1, relief="solid")
        left.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(left, text="Resultados (Binomial):", bg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=6)
        self.text_bin = tk.Text(left, height=10, font=("Courier", 10))
        self.text_bin.pack(fill="both", expand=True, padx=8, pady=(0,8))

        tk.Label(left, text="Tabla de probabilidades (k, P(X=k), P(X≤k)):", bg="#ffffff", font=("Arial", 11, "bold")).pack(anchor="w", padx=8, pady=(0,6))
        self.tree_bin = ttk.Treeview(left, columns=("k", "pk", "acum"), show="headings", height=8)
        self.tree_bin.heading("k", text="k"); self.tree_bin.heading("pk", text="P(X=k)"); self.tree_bin.heading("acum", text="P(X≤k)")
        self.tree_bin.column("k", width=60, anchor="center"); self.tree_bin.column("pk", width=100, anchor="center"); self.tree_bin.column("acum", width=100, anchor="center")
        self.tree_bin.pack(fill="both", expand=True, padx=8, pady=(0,8))

        right = tk.Frame(results_frame, bg="#ffffff", bd=1, relief="solid")
        right.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(right, text="Gráfico FMP (Binomial):", bg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w", padx=8, pady=6)
        self.canvas_bin_frame = tk.Frame(right, bg="#ffffff")
        self.canvas_bin_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def ejemplo_binomial(self):
        self.entry_n.delete(0, tk.END); self.entry_n.insert(0, "10")
        self.entry_p.delete(0, tk.END); self.entry_p.insert(0, "0.5")
        self.entry_k.delete(0, tk.END); self.entry_k.insert(0, "5")
        self.entry_k2.delete(0, tk.END); self.entry_k2.insert(0, "7")
        self.calcular_binomial()

    def limpiar_binomial(self):
        self.entry_n.delete(0, tk.END); self.entry_p.delete(0, tk.END)
        self.entry_k.delete(0, tk.END); self.entry_k2.delete(0, tk.END)
        self.text_bin.delete("1.0", tk.END)
        self.tree_bin.delete(*self.tree_bin.get_children())
        for w in self.canvas_bin_frame.winfo_children():
            w.destroy()

    def calcular_binomial(self):
        try:
            n = int(self.entry_n.get())
            p = float(self.entry_p.get())
            k = int(self.entry_k.get())
            k2 = int(self.entry_k2.get())
            if n <= 0:
                raise ValueError("n debe ser entero positivo")
            if not (0 <= p <= 1):
                raise ValueError("p debe estar entre 0 y 1")
            if not (0 <= k <= n):
                raise ValueError("k debe estar entre 0 y n")
            if not (0 <= k2 <= n):
                raise ValueError("k2 debe estar entre 0 y n")
        except Exception as e:
            messagebox.showerror("Entrada inválida", str(e))
            return

        def binom_pmf(n, p, k):
            return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

        pk = binom_pmf(n, p, k)
        acum_k2 = sum(binom_pmf(n, p, i) for i in range(k2 + 1))
        mean = n * p
        var = n * p * (1 - p)
        sd = var ** 0.5

        # Texto
        self.text_bin.delete("1.0", tk.END)
        txt = f"Distribución Binomial(n={n}, p={p:.4f})\n\n"
        txt += f"Media E[X] = n·p = {mean:.6f}\n"
        txt += f"Var(X) = n·p·(1-p) = {var:.6f}\n"
        txt += f"Desviación estándar σ = {sd:.6f}\n\n"
        txt += f"P(X = {k}) = {pk:.6f}\n"
        txt += f"P(X ≤ {k2}) = {acum_k2:.6f}\n"
        self.text_bin.insert(tk.END, txt)

        # Tabla
        self.tree_bin.delete(*self.tree_bin.get_children())
        acum = 0.0
        max_display = min(n, 60)  # evitar tablas gigantes
        for i in range(n + 1 if n <= 60 else max_display + 1):
            pi = binom_pmf(n, p, i)
            acum += pi
            self.tree_bin.insert("", "end", values=(i, f"{pi:.6f}", f"{acum:.6f}"))
        if n > 60:
            self.tree_bin.insert("", "end", values=("...", "...", "..."))

        # Gráfico
        for w in self.canvas_bin_frame.winfo_children():
            w.destroy()
        fig, ax = plt.subplots(figsize=(6, 4.2))
        xs = list(range(n + 1 if n <= 80 else max_display + 1))
        ys = [binom_pmf(n, p, xi) for xi in xs]
        ax.bar(xs, ys, color="#5dade2", width=0.6)
        ax.set_xlabel("k")
        ax.set_ylabel("P(X=k)")
        ax.set_title(f"Binomial(n={n}, p={p:.2f})")
        ax.set_ylim(0, max(ys) * 1.2 if ys else 1)
        ax.grid(axis="y", linestyle="--", alpha=0.4)

        # Highlight P(X=k)
        if k in xs:
            ax.bar([k], [binom_pmf(n, p, k)], color="#e74c3c", width=0.6)
        # Shade cumulative up to k2
        if k2 in xs:
            xs_shade = [i for i in xs if i <= k2]
            ys_shade = [binom_pmf(n, p, i) for i in xs_shade]
            ax.bar(xs_shade, ys_shade, color="#f6b26b", width=0.6, alpha=0.6)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_bin_frame)
        canvas.draw(); canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = BernoulliBinomialApp(root)
    root.mainloop()