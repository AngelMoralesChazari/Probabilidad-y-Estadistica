import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MedidasDispersionDiscretasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medidas de Dispersión en Distribuciones Discretas")
        self.root.geometry("1150x750")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(
            main_frame,
            text="Medidas de Dispersión en Distribuciones Discretas",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            main_frame,
            text="Ingresa una distribución discreta X (valores y probabilidades) para calcular varianza, desviación estándar, rango e IQR.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e",
            wraplength=1050
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
            text="Ejemplo 2 (más dispersa)",
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

        # Panel medio: tabla + resultados + gráfico
        middle_frame = tk.Frame(main_frame, bg="#f0f0f0")
        middle_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Izquierda: tabla
        left_frame = tk.Frame(middle_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="Tabla de la distribución y contribución a la varianza:",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.tree = ttk.Treeview(
            left_frame,
            columns=("x", "p", "acum", "(x-μ)^2", "(x-μ)^2·p"),
            show="headings",
            height=8
        )
        self.tree.heading("x", text="x")
        self.tree.heading("p", text="P(X=x)")
        self.tree.heading("acum", text="F(x)")
        self.tree.heading("(x-μ)^2", text="(x-μ)² (desp.)")
        self.tree.heading("(x-μ)^2·p", text="(x-μ)²·P(X=x)")

        self.tree.column("x", width=60, anchor="center")
        self.tree.column("p", width=80, anchor="center")
        self.tree.column("acum", width=80, anchor="center")
        self.tree.column("(x-μ)^2", width=110, anchor="center")
        self.tree.column("(x-μ)^2·p", width=130, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        # Resultados numéricos
        tk.Label(
            left_frame,
            text="Medidas de dispersión:",
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
            "   • Varianza: Var(X) = Σ (x - μ)² · P(X=x)\n"
            "   • Desviación estándar: σ = √Var(X)\n"
            "   • Rango: max(X) − min(X)\n"
            "   • Rango intercuartílico (IQR): Q3 − Q1, donde Q1 y Q3 se obtienen de la F(x) = P(X≤x).\n"
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
        """Distribución más compacta."""
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.entry_x_vals.insert(0, "0,1,2,3")
        self.entry_probs.insert(0, "0.1,0.3,0.4,0.2")
        self.calcular()

    def ejemplo_2(self):
        """Distribución más dispersa (valores más alejados)."""
        self.entry_x_vals.delete(0, tk.END)
        self.entry_probs.delete(0, tk.END)
        self.entry_x_vals.insert(0, "0,3,6,9")
        self.entry_probs.insert(0, "0.2,0.3,0.3,0.2")
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
            p_vals = [p / suma_p for p in p_vals]
            aviso = f"Advertencia: las probabilidades sumaban {suma_p:.4f}. Se han reescalado para que sumen 1.\n\n"

        # Ordenar por x
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

        # Varianza
        varianza = sum((x - media) ** 2 * p for x, p in zip(x_vals, p_vals))
        desv = varianza ** 0.5

        # Rango
        rango = x_vals[-1] - x_vals[0]

        # Cuartiles Q1 y Q3 (basados en F(x))
        Q1 = self.calcular_cuartil(x_vals, acum, 0.25)
        Q3 = self.calcular_cuartil(x_vals, acum, 0.75)
        IQR = Q3 - Q1

        # Completar tabla
        self.tree.delete(*self.tree.get_children())
        for x, p, F in zip(x_vals, p_vals, acum):
            # (x-μ)² lo mostramos solo como referencia numérica
            # y (x-μ)²·p como contribución a la varianza
            des_sq = (x - media) ** 2
            contrib = des_sq * p
            self.tree.insert(
                "", "end",
                values=(
                    f"{x:.3f}",
                    f"{p:.4f}",
                    f"{F:.4f}",
                    f"{des_sq:.4f}",
                    f"{contrib:.4f}"
                )
            )

        # Texto de resultados
        self.text_resultados.delete("1.0", tk.END)
        txt = ""
        if aviso:
            txt += aviso
        txt += "Media (μ):\n"
        txt += "   μ = Σ x·P(X=x)\n"
        txt += f"     = {media:.4f}\n\n"
        txt += "Varianza:\n"
        txt += "   Var(X) = Σ (x - μ)² · P(X=x)\n"
        txt += f"          = {varianza:.4f}\n\n"
        txt += "Desviación estándar:\n"
        txt += "   σ = √Var(X)\n"
        txt += f"     = {desv:.4f}\n\n"
        txt += "Rango:\n"
        txt += f"   max(X) - min(X) = {x_vals[-1]:.4f} - {x_vals[0]:.4f} = {rango:.4f}\n\n"
        txt += "Cuartiles aproximados (discretos):\n"
        txt += "   Q1: primer x con F(x) ≥ 0.25\n"
        txt += "   Q3: primer x con F(x) ≥ 0.75\n"
        txt += f"   Q1 ≈ {Q1:.4f}\n"
        txt += f"   Q3 ≈ {Q3:.4f}\n"
        txt += f"   IQR = Q3 - Q1 = {IQR:.4f}\n"
        self.text_resultados.insert(tk.END, txt)

        # Gráfico
        self.dibujar_grafico(x_vals, p_vals, media, Q1, Q3)

    def calcular_cuartil(self, x_vals, acum, q):
        """Devuelve el primer x tal que F(x) >= q."""
        for x, F in zip(x_vals, acum):
            if F >= q - 1e-8:
                return x
        return x_vals[-1]

    def dibujar_grafico(self, x_vals, p_vals, media, Q1, Q3):
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        import numpy as np
        fig, ax = plt.subplots(figsize=(5.5, 4))
        fig.patch.set_facecolor("#ffffff")

        # Barras
        ax.bar(x_vals, p_vals, color="#3498db", width=0.6, label="P(X=x)")

        # Sombrear rango intercuartílico (IQR)
        xs_iqr = [x for x in x_vals if Q1 <= x <= Q3]
        ys_iqr = [p for x, p in zip(x_vals, p_vals) if Q1 <= x <= Q3]
        if xs_iqr:
            ax.bar(xs_iqr, ys_iqr, color="#a5d6a7", width=0.6, label="Valores entre Q1 y Q3")

        # Línea vertical para la media
        ax.axvline(media, color="#e74c3c", linestyle="--", linewidth=2, label=f"Media ≈ {media:.2f}")

        # Marcar Q1 y Q3
        ax.axvline(Q1, color="#2ecc71", linestyle="-.", linewidth=1.8, label=f"Q1 ≈ {Q1:.2f}")
        ax.axvline(Q3, color="#9b59b6", linestyle="-.", linewidth=1.8, label=f"Q3 ≈ {Q3:.2f}")

        ax.set_xlabel("x")
        ax.set_ylabel("P(X=x)")
        ax.set_title("Distribución discreta y medidas de dispersión")
        ax.set_ylim(0, max(p_vals) * 1.3)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        ax.legend(loc="upper right")

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = MedidasDispersionDiscretasApp(root)
    root.mainloop()