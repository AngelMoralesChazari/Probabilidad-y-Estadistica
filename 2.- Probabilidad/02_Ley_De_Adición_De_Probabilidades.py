import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LeyAdicionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ley de Adición de Probabilidades")
        self.root.geometry("900x650")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        tk.Label(
            main_frame,
            text="Ley de Adición de Probabilidades",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            main_frame,
            text="Para dos sucesos A y B:  P(A ∪ B) = P(A) + P(B) − P(A ∩ B)",
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
        self.entry_PA.insert(0, "0.4")
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
        self.entry_PAB.insert(0, "0.2")
        self.entry_PAB.grid(row=1, column=1, padx=5, pady=8)

        # Casilla: mutuamente excluyentes
        self.var_excluyentes = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(
            input_frame,
            text="A y B son mutuamente excluyentes (P(A ∩ B) = 0)",
            font=("Arial", 10),
            bg="#ffffff",
            anchor="w",
            variable=self.var_excluyentes,
            command=self.toggle_excluyentes
        )
        chk.grid(row=1, column=2, columnspan=2, padx=10, pady=8, sticky="w")

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
            text="Ejemplo solapados",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_solapados
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo excluyentes",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_excluyentes
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
            text="📝 Resultados:",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=(10, 5))

        self.text_resultados = tk.Text(
            left_frame,
            height=10,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_resultados.pack(fill="both", expand=True, padx=10, pady=5)

        # Derecha: gráfico
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📊 Visualización de probabilidades:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---------- Info teórica ----------
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Ley de adición:\n"
            "   - Caso general:   P(A ∪ B) = P(A) + P(B) − P(A ∩ B)\n"
            "   - Si A y B son mutuamente excluyentes (no se solapan): P(A ∩ B) = 0,\n"
            "     entonces P(A ∪ B) = P(A) + P(B).\n"
            "   - Siempre debe cumplirse 0 ≤ P(·) ≤ 1 y P(A ∪ B) ≤ 1."
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

    def toggle_excluyentes(self):
        """Si se marcan excluyentes, fijar P(A∩B)=0 y deshabilitar entrada."""
        if self.var_excluyentes.get():
            self.entry_PAB.delete(0, tk.END)
            self.entry_PAB.insert(0, "0")
            self.entry_PAB.config(state="disabled")
        else:
            self.entry_PAB.config(state="normal")

    def leer_prob(self, entry, nombre):
        """Lee un valor de probabilidad de un Entry y valida [0,1]."""
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

        # Comprobaciones lógicas básicas
        if PAB > PA or PAB > PB:
            messagebox.showerror(
                "Error lógico",
                "P(A ∩ B) no puede ser mayor que P(A) ni que P(B)."
            )
            return

        PU = PA + PB - PAB  # P(A ∪ B)

        if PU < 0 or PU > 1 + 1e-8:
            messagebox.showerror(
                "Error lógico",
                "El resultado P(A ∪ B) está fuera del rango [0,1]. "
                "Revisa los valores introducidos."
            )
            return

        # Redondear un poco
        PU = max(0, min(1, PU))

        # Partes exclusivas e intersección
        solo_A = PA - PAB
        solo_B = PB - PAB

        # Mostrar texto
        self.text_resultados.delete("1.0", tk.END)
        lineas = []
        lineas.append(f"P(A)      = {PA:.4f}")
        lineas.append(f"P(B)      = {PB:.4f}")
        lineas.append(f"P(A ∩ B)  = {PAB:.4f}")
        lineas.append("")
        lineas.append("Ley de adición general:")
        lineas.append("P(A ∪ B) = P(A) + P(B) − P(A ∩ B)")
        lineas.append(
            f"          = {PA:.4f} + {PB:.4f} − {PAB:.4f} = {PU:.4f}"
        )
        lineas.append("")
        lineas.append(f"Parte solo en A      (A \\ B) = {solo_A:.4f}")
        lineas.append(f"Parte solo en B      (B \\ A) = {solo_B:.4f}")
        lineas.append(f"Parte en ambos       (A ∩ B)  = {PAB:.4f}")
        lineas.append(f"Unión total          (A ∪ B)  = {PU:.4f}")
        if self.var_excluyentes.get():
            lineas.append("")
            lineas.append("Como A y B son mutuamente excluyentes, P(A ∩ B) = 0,")
            lineas.append("por lo que P(A ∪ B) = P(A) + P(B).")

        self.text_resultados.insert(tk.END, "\n".join(lineas))

        # Dibujar gráfico de barras
        self.dibujar_barras(PA, PB, PAB, PU)

    def dibujar_barras(self, PA, PB, PAB, PU):
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        etiquetas = ["P(A)", "P(B)", "P(A∩B)", "P(A∪B)"]
        valores = [PA, PB, PAB, PU]
        colores = ["#3498db", "#e74c3c", "#9b59b6", "#27ae60"]

        ax.bar(etiquetas, valores, color=colores)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Probabilidad")
        ax.set_title("Probabilidades de A, B, intersección y unión")

        for i, v in enumerate(valores):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=10)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def ejemplo_solapados(self):
        """Ejemplo con intersección positiva."""
        self.var_excluyentes.set(False)
        self.entry_PAB.config(state="normal")

        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)

        self.entry_PA.insert(0, "0.6")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.3")
        self.calcular()

    def ejemplo_excluyentes(self):
        """Ejemplo con sucesos mutuamente excluyentes."""
        self.var_excluyentes.set(True)
        self.toggle_excluyentes()

        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)

        self.entry_PA.insert(0, "0.3")
        self.entry_PB.insert(0, "0.4")
        # PAB se pone en 0 por toggle_excluyentes
        self.calcular()

    def limpiar(self):
        self.var_excluyentes.set(False)
        self.entry_PAB.config(state="normal")

        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)

        self.entry_PA.insert(0, "0.4")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.2")

        self.text_resultados.delete("1.0", tk.END)
        for w in self.canvas_frame.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LeyAdicionApp(root)
    root.mainloop()