import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class MedidasTendenciaCentralDiscretasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medidas de Tendencia Central en Distribuciones Discretas")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            main_frame,
            text="Medidas de Tendencia Central en Distribuciones Discretas",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            main_frame,
            text="Ingresa una distribución discreta X (valores y probabilidades) para obtener media, mediana y moda.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e",
            wraplength=1000
        ).pack(pady=(0, 10))

        # Panel superior: entradas y botones
        top_frame = tk.Frame(main_frame, bg="#f0f0f0")
        top_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(
            top_frame,
            text="Valores de X (separados por comas):",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.entry_x_vals = tk.Entry(top_frame, font=("Arial", 11), width=40)
        self.entry_x_vals.grid(row=0, column=1, padx=5, pady=5)
        self.entry_x_vals.insert(0, "0,1,2,3")  # ejemplo

        tk.Label(
            top_frame,
            text="Probabilidades P(X=x) (separadas por comas):",
            font=("Arial", 11),
            bg="#f0f0f0"
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.entry_probs = tk.Entry(top_frame, font=("Arial", 11), width=40)
        self.entry_probs.grid(row=1, column=1, padx=5, pady=5)
        self.entry_probs.insert(0, "0.1,0.3,0.4,0.2")  # ejemplo

        # Botones
        btn_frame = tk.Frame(top_frame, bg="#f0f0f0")
        btn_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Calcular",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Ejemplo 1",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_1
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Ejemplo 2 (bimodal)",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_2
        ).pack(pady=3, fill="x")

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar
        ).pack(pady=3, fill="x")

        # Panel medio: resultados y gráfico
        middle_frame = tk.Frame(main_frame, bg="#f0f0f0")
        middle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Izquierda: tabla y texto
        left_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Tabla de la distribución:",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.tree = ttk.Treeview(
            left_frame,
            columns=("x", "p", "acum"),
            show="headings",
            height=8
        )
        self.tree.heading("x", text="x")
        self.tree.heading("p", text="P(X=x)")
        self.tree.heading("acum", text="F(x)=P(X≤x)")

        self.tree.column("x", width=60, anchor="center")
        self.tree.column("p", width=80, anchor="center")
        self.tree.column("acum", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Medidas de tendencia central:",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=(5, 0))

        self.text_resultados = tk.Text(left_frame, height=10, font=("Courier", 10), wrap="word")
        self.text_resultados.pack(fill="both", expand=True, padx=5, pady=5)

        # Derecha: gráfico
        right_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="Gráfico de la distribución discreta",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Panel inferior: explicación breve
        bottom_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        bottom_frame.pack(fill="x", padx=10, pady=(5, 0))

        expl = (
            "ℹ️ Recordatorio:\n"
            "   • Media (esperanza): E[X] = Σ x·P(X=x)\n"
            "   • Mediana: valor m tal que P(X ≤ m) ≥ 0.5 y P(X ≥ m) ≥ 0.5\n"
            "   • Moda: valor(es) x con P(X=x) máxima.\n"
            "   Esta app trabaja con distribuciones discretas definidas por valores X y sus probabilidades."
        )
        tk.Label(
            bottom_frame,
            text=expl,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left",
            anchor="w",
            wraplength=1050
        ).pack(fill="x", padx=10, pady=8)

    # ===================== LÓGICA =====================

    def ejemplo_1(self):
        """Distribución sencilla, unimodal."""
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.entry_x_vals.insert(0, "0,1,2,3")
        self.entry_probs.insert(0, "0.1,0.3,0.4,0.2")
        self.calcular()

    def ejemplo_2(self):
        """Distribución bimodal (dos modas)."""
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.entry_x_vals.insert(0, "1,2,3,4,5")
        self.entry_probs.insert(0, "0.2,0.3,0.1,0.3,0.1")
        self.calcular()

    def limpiar(self):
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        self.text_resultados.delete("1.0", tk.END)
        for w in self.canvas_frame.winfo_children():
            w.destroy()

    def calcular(self):
        # Leer y validar datos
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

        # Normalizar (opcional) o solo advertir
        aviso = ""
        if abs(suma_p - 1) > 1e-6:
            # Normalizamos para que la suma sea 1, pero avisamos al usuario
            p_vals = [p / suma_p for p in p_vals]
            aviso = f"Advertencia: las probabilidades sumaban {suma_p:.4f}. Se han reescalado para que sumen 1.\n\n"

        # Ordenar por x (por si vienen desordenados)
        pares = sorted(zip(x_vals, p_vals), key=lambda t: t[0])
        x_vals = [t[0] for t in pares]
        p_vals = [t[1] for t in pares]

        # Media
        media = sum(x * p for x, p in zip(x_vals, p_vals))

        # Distribución acumulada
        acum = []
        total = 0.0
        for p in p_vals:
            total += p
            acum.append(total)

        # Mediana (para VA discreta)
        # Buscamos el primer x tal que F(x) >= 0.5
        mediana = None
        for x, F in zip(x_vals, acum):
            if F >= 0.5 - 1e-8:  # tolerancia numérica
                mediana = x
                break

        # Moda(s): los x con probabilidad máxima
        max_p = max(p_vals)
        modas = [x for x, p in zip(x_vals, p_vals) if abs(p - max_p) < 1e-12]

        # Llenar tabla
        self.tree.delete(*self.tree.get_children())
        for x, p, F in zip(x_vals, p_vals, acum):
            self.tree.insert(
                "", "end",
                values=(f"{x:.3f}", f"{p:.4f}", f"{F:.4f}")
            )

        # Mostrar resultados
        self.text_resultados.delete("1.0", tk.END)
        txt = ""
        if aviso:
            txt += aviso
        txt += "Media (esperanza):\n"
        txt += "   μ = Σ x·P(X=x)\n"
        txt += f"     = {media:.4f}\n\n"
        txt += "Mediana (discreta):\n"
        txt += "   m = primer valor x con F(x) = P(X≤x) ≥ 0.5\n"
        txt += f"   m = {mediana:.4f}\n\n" if mediana is not None else "   No se pudo determinar la mediana.\n\n"
        txt += "Moda(s):\n"
        txt += "   Valor(es) de x con P(X=x) máxima.\n"
        txt += f"   Pmáx = {max_p:.4f}\n"
        txt += "   Modas: " + ", ".join(f"{m:.3f}" for m in modas) + "\n"
        self.text_resultados.insert(tk.END, txt)

        # Gráfico
        self.dibujar_grafico(x_vals, p_vals, media, mediana, modas)

    def dibujar_grafico(self, x_vals, p_vals, media, mediana, modas):
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 4))
        fig.patch.set_facecolor("#ffffff")

        # Barras
        ax.bar(x_vals, p_vals, color="#3498db", width=0.6, label="P(X=x)")

        # Línea vertical para la media
        ax.axvline(media, color="#e74c3c", linestyle="--", linewidth=2, label=f"Media ≈ {media:.2f}")

        # Línea vertical para la mediana
        ax.axvline(mediana, color="#2ecc71", linestyle="-.", linewidth=2, label=f"Mediana ≈ {mediana:.2f}")

        # Resaltar modas
        for m in modas:
            ax.annotate(
                "Moda",
                xy=(m, max(p_vals)),
                xytext=(0, 10),
                textcoords="offset points",
                ha="center",
                color="#9b59b6",
                fontsize=9,
                fontweight="bold"
            )

        ax.set_xlabel("x")
        ax.set_ylabel("P(X=x)")
        ax.set_title("Distribución discreta y medidas de tendencia central")
        ax.set_ylim(0, max(p_vals) * 1.3)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.legend(loc="upper right")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = MedidasTendenciaCentralDiscretasApp(root)
    root.mainloop()