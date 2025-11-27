import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class VariablesAleatoriasInteractivoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Variables Aleatorias: Discretas y Continuas (Interactivo)")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            main_frame,
            text="Variables Aleatorias: Discretas y Continuas (Laboratorio Interactivo)",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        # Notebook con 2 pestañas: Discreta y Continua
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)

        self.tab_discreta = tk.Frame(self.notebook, bg="#f6f6ff")
        self.tab_continua = tk.Frame(self.notebook, bg="#f6fff6")

        self.notebook.add(self.tab_discreta, text="1. Variable Aleatoria Discreta")
        self.notebook.add(self.tab_continua, text="2. Variable Aleatoria Continua (Uniforme)")

        self.crear_tab_discreta()
        self.crear_tab_continua()

    # ===================== TAB DISCRETA =====================

    def crear_tab_discreta(self):
        frame = self.tab_discreta

        # Título
        tk.Label(
            frame,
            text="Variable Aleatoria Discreta",
            font=("Arial", 16, "bold"),
            bg="#f6f6ff",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            frame,
            text="Ingresa los valores posibles de X y sus probabilidades P(X=x).",
            font=("Arial", 11),
            bg="#f6f6ff",
            fg="#34495e"
        ).pack(pady=(0, 10))

        # Panel superior: entradas y botones
        top_frame = tk.Frame(frame, bg="#f6f6ff")
        top_frame.pack(fill="x", padx=10, pady=5)

        # Entradas
        tk.Label(
            top_frame,
            text="Valores de X (separados por comas):",
            font=("Arial", 11),
            bg="#f6f6ff"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_x_vals = tk.Entry(top_frame, font=("Arial", 11), width=40)
        self.entry_x_vals.grid(row=0, column=1, padx=5, pady=5)
        self.entry_x_vals.insert(0, "0,1,2,3")  # ejemplo por defecto

        tk.Label(
            top_frame,
            text="Probabilidades P(X=x) (separadas por comas):",
            font=("Arial", 11),
            bg="#f6f6ff"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_probs = tk.Entry(top_frame, font=("Arial", 11), width=40)
        self.entry_probs.grid(row=1, column=1, padx=5, pady=5)
        self.entry_probs.insert(0, "0.125,0.375,0.375,0.125")  # ejemplo

        # Botones
        btn_frame = tk.Frame(top_frame, bg="#f6f6ff")
        btn_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Calcular y Graficar",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_discreta
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Ejemplo: 3 monedas",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_discreta_monedas
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar_discreta
        ).pack(pady=3, fill="x")

        # Panel medio: resultados numéricos
        middle_frame = tk.Frame(frame, bg="#f6f6ff")
        middle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Resultados (VA Discreta):",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        # Treeview para tabla
        self.tree_discreta = ttk.Treeview(
            left_frame,
            columns=("x", "p", "x*p", "(x-μ)^2*p"),
            show="headings",
            height=8
        )
        self.tree_discreta.heading("x", text="x")
        self.tree_discreta.heading("p", text="P(X=x)")
        self.tree_discreta.heading("x*p", text="x·P(X=x)")
        self.tree_discreta.heading("(x-μ)^2*p", text="(x-μ)²·P(X=x) (desp.)")

        self.tree_discreta.column("x", width=60, anchor="center")
        self.tree_discreta.column("p", width=80, anchor="center")
        self.tree_discreta.column("x*p", width=100, anchor="center")
        self.tree_discreta.column("(x-μ)^2*p", width=160, anchor="center")

        self.tree_discreta.pack(fill="both", expand=True, padx=5, pady=5)

        # Texto para resumen (media, varianza)
        self.text_resumen_discreta = tk.Text(
            left_frame,
            height=6,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_resumen_discreta.pack(fill="x", padx=5, pady=5)

        # Panel derecho: gráfico
        right_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="Gráfico de la FMP (VA Discreta)",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_discreta_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_discreta_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def ejemplo_discreta_monedas(self):
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.entry_x_vals.insert(0, "0,1,2,3")
        self.entry_probs.insert(0, "0.125,0.375,0.375,0.125")
        self.calcular_discreta()

    def limpiar_discreta(self):
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.tree_discreta.delete(*self.tree_discreta.get_children())
        self.text_resumen_discreta.delete("1.0", tk.END)
        for w in self.canvas_discreta_frame.winfo_children():
            w.destroy()

    def calcular_discreta(self):
        # Leer datos
        try:
            x_text = self.entry_x_vals.get().strip()
            p_text = self.entry_probs.get().strip()
            if not x_text or not p_text:
                raise ValueError("Debe ingresar valores de X y sus probabilidades.")

            x_strs = [s.strip() for s in x_text.split(",") if s.strip() != ""]
            p_strs = [s.strip() for s in p_text.split(",") if s.strip() != ""]

            if len(x_strs) != len(p_strs):
                raise ValueError("La cantidad de valores de X y de probabilidades P(X=x) debe coincidir.")

            x_vals = [float(s) for s in x_strs]
            p_vals = [float(s) for s in p_strs]

            if any(p < 0 for p in p_vals):
                raise ValueError("Las probabilidades no pueden ser negativas.")

            suma_p = sum(p_vals)
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        # Avisar si las probabilidades no suman 1 (pero seguir)
        aviso = ""
        if abs(suma_p - 1) > 1e-6:
            aviso = f"Advertencia: La suma de las probabilidades es {suma_p:.4f} (no es exactamente 1).\n"

        # Calcular media y varianza
        media = sum(x * p for x, p in zip(x_vals, p_vals))
        varianza = sum((x - media) ** 2 * p for x, p in zip(x_vals, p_vals))

        # Llenar tabla
        self.tree_discreta.delete(*self.tree_discreta.get_children())
        for x, p in zip(x_vals, p_vals):
            self.tree_discreta.insert(
                "", "end",
                values=(f"{x:.3f}", f"{p:.4f}", f"{x*p:.4f}", "")
            )

        # Segunda pasada para completar (x-μ)^2 p(x)
        children = self.tree_discreta.get_children()
        for idx, (x, p) in enumerate(zip(x_vals, p_vals)):
            valor = (x - media) ** 2 * p
            vals = list(self.tree_discreta.item(children[idx], "values"))
            vals[3] = f"{valor:.4f}"
            self.tree_discreta.item(children[idx], values=vals)

        # Texto de resumen
        self.text_resumen_discreta.delete("1.0", tk.END)
        txt = ""
        if aviso:
            txt += aviso + "\n"
        txt += "Media (E[X]):\n"
        txt += f"   μ = Σ x·P(X=x) = {media:.4f}\n\n"
        txt += "Varianza (Var(X)):\n"
        txt += "   Var(X) = Σ (x - μ)²·P(X=x)\n"
        txt += f"          = {varianza:.4f}\n"
        self.text_resumen_discreta.insert(tk.END, txt)

        # Gráfico
        self.dibujar_grafico_discreta(x_vals, p_vals)

    def dibujar_grafico_discreta(self, x_vals, p_vals):
        for w in self.canvas_discreta_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        fig.patch.set_facecolor("#ffffff")

        ax.bar(x_vals, p_vals, color="#3498db", width=0.6)
        ax.set_xlabel("x")
        ax.set_ylabel("P(X=x)")
        ax.set_title("Función de Masa de Probabilidad (VA Discreta)")
        ax.set_ylim(0, max(p_vals) * 1.2)

        for x, p in zip(x_vals, p_vals):
            ax.text(x, p + 0.01, f"{p:.2f}", ha="center", va="bottom", fontsize=9)

        ax.grid(axis="y", linestyle="--", alpha=0.5)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_discreta_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ===================== TAB CONTINUA (UNIFORME) =====================

    def crear_tab_continua(self):
        frame = self.tab_continua

        # Título
        tk.Label(
            frame,
            text="Variable Aleatoria Continua (Uniforme en [a,b])",
            font=("Arial", 16, "bold"),
            bg="#f6fff6",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            frame,
            text="Usamos una VA continua con distribución Uniforme(a,b). La densidad es f(x) = 1/(b-a) en [a,b].",
            font=("Arial", 11),
            bg="#f6fff6",
            fg="#34495e",
            wraplength=1000
        ).pack(pady=(0, 10))

        # Panel superior
        top_frame = tk.Frame(frame, bg="#f6fff6")
        top_frame.pack(fill="x", padx=10, pady=5)

        # Intervalo [a,b]
        tk.Label(
            top_frame,
            text="a (inicio del intervalo):",
            font=("Arial", 11),
            bg="#f6fff6"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_a = tk.Entry(top_frame, font=("Arial", 11), width=10)
        self.entry_a.grid(row=0, column=1, padx=5, pady=5)
        self.entry_a.insert(0, "0")

        tk.Label(
            top_frame,
            text="b (final del intervalo):",
            font=("Arial", 11),
            bg="#f6fff6"
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.entry_b = tk.Entry(top_frame, font=("Arial", 11), width=10)
        self.entry_b.grid(row=0, column=3, padx=5, pady=5)
        self.entry_b.insert(0, "10")

        # Intervalo [c,d] para probabilidad
        tk.Label(
            top_frame,
            text="c (inicio sub-intervalo):",
            font=("Arial", 11),
            bg="#f6fff6"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_c = tk.Entry(top_frame, font=("Arial", 11), width=10)
        self.entry_c.grid(row=1, column=1, padx=5, pady=5)
        self.entry_c.insert(0, "2")

        tk.Label(
            top_frame,
            text="d (final sub-intervalo):",
            font=("Arial", 11),
            bg="#f6fff6"
        ).grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.entry_d = tk.Entry(top_frame, font=("Arial", 11), width=10)
        self.entry_d.grid(row=1, column=3, padx=5, pady=5)
        self.entry_d.insert(0, "6")

        # Botones
        btn_frame = tk.Frame(top_frame, bg="#f6fff6")
        btn_frame.grid(row=0, column=4, rowspan=2, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Calcular Probabilidad",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_continua
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Ejemplo: Uniforme(0,10), P(2≤X≤6)",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_continua
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar_continua
        ).pack(pady=3, fill="x")

        # Panel medio: resultado y gráfico
        middle_frame = tk.Frame(frame, bg="#f6fff6")
        middle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Resultados (Uniforme Continua):",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.text_resumen_continua = tk.Text(
            left_frame,
            height=10,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_resumen_continua.pack(fill="both", expand=True, padx=5, pady=5)

        right_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="Gráfico de la FDP (Uniforme[a,b])",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_continua_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_continua_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def ejemplo_continua(self):
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_d.delete(0, tk.END)

        self.entry_a.insert(0, "0")
        self.entry_b.insert(0, "10")
        self.entry_c.insert(0, "2")
        self.entry_d.insert(0, "6")

        self.calcular_continua()

    def limpiar_continua(self):
        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.entry_d.delete(0, tk.END)

        self.text_resumen_continua.delete("1.0", tk.END)
        for w in self.canvas_continua_frame.winfo_children():
            w.destroy()

    def calcular_continua(self):
        try:
            a = float(self.entry_a.get())
            b = float(self.entry_b.get())
            c = float(self.entry_c.get())
            d = float(self.entry_d.get())
        except ValueError:
            messagebox.showerror("Error de entrada", "Todos los valores deben ser numéricos.")
            return

        if a >= b:
            messagebox.showerror("Error lógico", "Debe cumplirse a < b.")
            return

        # Ajustar [c,d] al intervalo [a,b] (parte que realmente tiene densidad)
        c_ef = max(a, min(b, c))
        d_ef = max(a, min(b, d))

        if c_ef > d_ef:
            prob = 0.0
        else:
            prob = (d_ef - c_ef) / (b - a)

        densidad = 1.0 / (b - a)
        media = (a + b) / 2.0
        varianza = (b - a) ** 2 / 12.0

        # Mostrar texto
        self.text_resumen_continua.delete("1.0", tk.END)
        txt = ""
        txt += f"Intervalo de la VA: X ~ Uniforme({a:.3f}, {b:.3f})\n"
        txt += f"f(x) = 1/(b-a) = {densidad:.4f}  para x en [{a:.3f}, {b:.3f}]\n\n"
        txt += f"Media E[X] = (a+b)/2 = {media:.4f}\n"
        txt += f"Varianza Var(X) = (b-a)²/12 = {varianza:.4f}\n\n"
        txt += f"Probabilidad solicitada: P({c:.3f} ≤ X ≤ {d:.3f})\n"
        if c_ef > d_ef:
            txt += "   El sub-intervalo no intersecta con [a,b], por lo tanto P = 0.\n"
        else:
            txt += f"   Ajustado al soporte: P({c_ef:.3f} ≤ X ≤ {d_ef:.3f})\n"
            txt += f"   = (d_ef - c_ef) / (b - a) = ({d_ef:.3f} - {c_ef:.3f}) / ({b:.3f} - {a:.3f})\n"
            txt += f"   = {prob:.4f}\n"
        self.text_resumen_continua.insert(tk.END, txt)

        # Gráfico
        self.dibujar_grafico_continua(a, b, c_ef, d_ef, densidad)

    def dibujar_grafico_continua(self, a, b, c_ef, d_ef, densidad):
        for w in self.canvas_continua_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 3.5))
        fig.patch.set_facecolor("#ffffff")

        # Densidad uniforme
        x = np.linspace(a - (b - a) * 0.2, b + (b - a) * 0.2, 500)
        y = np.where((x >= a) & (x <= b), densidad, 0.0)

        ax.plot(x, y, color="#2980b9")
        ax.axhline(0, color="black", linewidth=1)

        # Rectángulo sombreado entre c_ef y d_ef
        if c_ef < d_ef:
            xs = np.array([c_ef, d_ef])
            ys = np.array([densidad, densidad])
            ax.fill_between(xs, 0, ys, color="#a5d6a7", alpha=0.7,
                            label=f"Área P({c_ef:.2f}≤X≤{d_ef:.2f})")

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title("Función de Densidad de Probabilidad - Uniforme(a,b)")
        ax.set_ylim(bottom=0, top=densidad * 1.4)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.legend(loc="upper right")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_continua_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = VariablesAleatoriasInteractivoApp(root)
    root.mainloop()