import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ProbabilidadCondicionalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Probabilidad Condicional")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        tk.Label(
            main_frame,
            text="Probabilidad Condicional",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            main_frame,
            text="P(A | B) = P(A ∩ B) / P(B)   y   P(B | A) = P(A ∩ B) / P(A), con P(A), P(B) > 0",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        ).pack(pady=(0, 10))

        # ---------- Entradas ----------
        input_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=5, pady=5)

        # P(A)
        tk.Label(
            input_frame,
            text="P(A):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.entry_PA = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_PA.insert(0, "0.6")
        self.entry_PA.grid(row=0, column=1, padx=5, pady=8)

        # P(B)
        tk.Label(
            input_frame,
            text="P(B):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=2, padx=10, pady=8, sticky="w")

        self.entry_PB = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_PB.insert(0, "0.5")
        self.entry_PB.grid(row=0, column=3, padx=5, pady=8)

        # P(A ∩ B)
        tk.Label(
            input_frame,
            text="P(A ∩ B):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.entry_PAB = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_PAB.insert(0, "0.3")
        self.entry_PAB.grid(row=1, column=1, padx=5, pady=8)

        # Botones
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        tk.Button(
            btn_frame,
            text="Calcular",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo 1",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo1
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo 2",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.ejemplo2
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar
        ).pack(side="left", padx=5)

        # ---------- Resultados ----------
        results_frame = tk.Frame(main_frame, bg="#f0f0f0")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Izquierda: texto
        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="📝 Resultados y explicación:",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=(10, 5))

        self.text_resultados = tk.Text(
            left_frame,
            height=15,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_resultados.pack(fill="both", expand=True, padx=10, pady=5)

        # Derecha: gráfico
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📊 Visualización:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------- Info teórica ----------
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Probabilidad condicional:\n"
            "   P(A | B) = P(A ∩ B) / P(B), siempre que P(B) > 0.\n"
            "   Interpreta P(A | B) como la probabilidad de A restringida al caso en que B ha ocurrido.\n"
            "   Análogamente, P(B | A) = P(A ∩ B) / P(A), si P(A) > 0.\n"
            "   Muy relacionada con los diagramas de Venn y con la noción de eventos independientes."
        )

        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(fill="x", padx=10, pady=8)

    # ---------- Lógica ----------

    def leer_prob(self, entry, nombre):
        try:
            val = float(entry.get())
            if not (0 <= val <= 1):
                raise ValueError
            return val
        except ValueError:
            raise ValueError(f"{nombre} debe ser un número entre 0 y 1.")

    def calcular(self):
        # Leer y validar
        try:
            PA = self.leer_prob(self.entry_PA, "P(A)")
            PB = self.leer_prob(self.entry_PB, "P(B)")
            PAB = self.leer_prob(self.entry_PAB, "P(A ∩ B)")
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        # Comprobaciones lógicas
        if PAB > PA or PAB > PB:
            messagebox.showerror(
                "Error lógico",
                "P(A ∩ B) no puede ser mayor que P(A) ni que P(B)."
            )
            return

        if PA == 0 and PB == 0:
            messagebox.showerror(
                "Error",
                "P(A) y P(B) no pueden ser ambas cero."
            )
            return

        # Condicionales
        PA_dado_B = None
        PB_dado_A = None

        if PB > 0:
            PA_dado_B = PAB / PB
        if PA > 0:
            PB_dado_A = PAB / PA

        # Independencia
        independiente = abs(PAB - PA * PB) < 1e-6

        # Mostrar texto
        self.text_resultados.delete("1.0", tk.END)
        lineas = []
        lineas.append(f"P(A)      = {PA:.4f}")
        lineas.append(f"P(B)      = {PB:.4f}")
        lineas.append(f"P(A ∩ B)  = {PAB:.4f}")
        lineas.append("")
        if PA_dado_B is not None:
            lineas.append("P(A | B) = P(A ∩ B) / P(B)")
            lineas.append(
                f"         = {PAB:.4f} / {PB:.4f} = {PA_dado_B:.4f}"
            )
        else:
            lineas.append("P(A | B) no está definida porque P(B) = 0.")
        lineas.append("")
        if PB_dado_A is not None:
            lineas.append("P(B | A) = P(A ∩ B) / P(A)")
            lineas.append(
                f"         = {PAB:.4f} / {PA:.4f} = {PB_dado_A:.4f}"
            )
        else:
            lineas.append("P(B | A) no está definida porque P(A) = 0.")
        lineas.append("")
        if independiente:
            lineas.append("A y B son (aproximadamente) INDEPENDIENTES, porque:")
            lineas.append(f"   P(A ∩ B) ≈ P(A) · P(B) = {PA*PB:.4f}")
        else:
            lineas.append("A y B NO son independientes, porque:")
            lineas.append(f"   P(A ∩ B) = {PAB:.4f}  y  P(A)·P(B) = {PA*PB:.4f}")

        self.text_resultados.insert(tk.END, "\n".join(lineas))

        # Dibujar barras
        self.dibujar_barras(PA, PB, PAB, PA_dado_B, PB_dado_A)

    def dibujar_barras(self, PA, PB, PAB, PA_dado_B, PB_dado_A):
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        etiquetas = ["P(A)", "P(B)", "P(A∩B)"]
        valores = [PA, PB, PAB]
        colores = ["#3498db", "#e74c3c", "#9b59b6"]

        if PA_dado_B is not None:
            etiquetas.append("P(A|B)")
            valores.append(PA_dado_B)
            colores.append("#27ae60")
        if PB_dado_A is not None:
            etiquetas.append("P(B|A)")
            valores.append(PB_dado_A)
            colores.append("#f1c40f")

        ax.bar(etiquetas, valores, color=colores)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Probabilidad")
        ax.set_title("P(A), P(B), P(A∩B), P(A|B), P(B|A)")

        for i, v in enumerate(valores):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=9)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- Ejemplos y limpiar ----------

    def ejemplo1(self):
        """
        Ejemplo típico:
        P(A) = 0.6, P(B) = 0.5, P(A ∩ B) = 0.3
        """
        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)

        self.entry_PA.insert(0, "0.6")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.3")
        self.calcular()

    def ejemplo2(self):
        """
        Ejemplo con independencia:
        P(A) = 0.4, P(B) = 0.5, P(A ∩ B) = 0.2  (≈ 0.4 * 0.5)
        """
        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)

        self.entry_PA.insert(0, "0.4")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.2")
        self.calcular()

    def limpiar(self):
        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)

        self.entry_PA.insert(0, "0.6")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.3")

        self.text_resultados.delete("1.0", tk.END)
        for w in self.canvas_frame.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProbabilidadCondicionalApp(root)
    root.mainloop()