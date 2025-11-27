import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LeyMultiplicacionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ley de Multiplicación de Probabilidades")
        self.root.geometry("1000x680")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        tk.Label(
            main_frame,
            text="Ley de Multiplicación de Probabilidades",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        ).pack(pady=5)

        tk.Label(
            main_frame,
            text="P(A ∩ B) = P(B)·P(A|B) = P(A)·P(B|A)   (si A y B independientes:  P(A ∩ B) = P(A)·P(B))",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e",
            wraplength=900
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

        # P(A | B)
        tk.Label(
            input_frame,
            text="P(A | B):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=2, padx=10, pady=8, sticky="w")

        self.entry_PA_B = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_PA_B.insert(0, "")
        self.entry_PA_B.grid(row=1, column=3, padx=5, pady=8)

        # P(B | A)
        tk.Label(
            input_frame,
            text="P(B | A):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=4, padx=10, pady=8, sticky="w")

        self.entry_PB_A = tk.Entry(input_frame, font=("Arial", 11), width=10)
        self.entry_PB_A.insert(0, "")
        self.entry_PB_A.grid(row=1, column=5, padx=5, pady=8)

        # Independencia
        self.var_indep = tk.BooleanVar(value=False)
        chk_indep = tk.Checkbutton(
            input_frame,
            text="A y B son independientes (P(A ∩ B) = P(A)·P(B))",
            font=("Arial", 10),
            bg="#ffffff",
            anchor="w",
            variable=self.var_indep,
            command=self.toggle_independencia
        )
        chk_indep.grid(row=2, column=0, columnspan=6, padx=10, pady=8, sticky="w")

        # Botones
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

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
            text="Ejemplo general",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_general
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Ejemplo independiente",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_indep
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
            "ℹ️ Ley de multiplicación:\n"
            "   - General:  P(A ∩ B) = P(B)·P(A|B) = P(A)·P(B|A).\n"
            "   - Si A y B son independientes: P(A ∩ B) = P(A)·P(B), "
            "y se cumple P(A|B) = P(A),  P(B|A) = P(B).\n"
            "   - Útil para calcular probabilidades conjuntas a partir de probabilidades simples y condicionales."
        )

        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left",
            anchor="w",
            wraplength=950
        ).pack(fill="x", padx=10, pady=8)

    # ---------- Lógica ----------

    def leer_prob_opcional(self, entry):
        """Devuelve None si está vacío, o el valor float si es válido en [0,1]."""
        txt = entry.get().strip()
        if txt == "":
            return None
        try:
            val = float(txt)
            if not (0 <= val <= 1):
                raise ValueError
            return val
        except ValueError:
            raise ValueError("Valores deben estar entre 0 y 1 o dejarse en blanco.")

    def leer_prob_obligatoria(self, entry, nombre):
        """Lee un valor de probabilidad obligatorio en [0,1]."""
        try:
            val = float(entry.get())
            if not (0 <= val <= 1):
                raise ValueError
            return val
        except ValueError:
            raise ValueError(f"{nombre} debe ser un número entre 0 y 1.")

    def toggle_independencia(self):
        """Si son independientes, fijar P(A∩B) = P(A)·P(B) (cuando se calcule)."""
        # No deshabilitamos nada aquí, solo dejamos una marca lógica.
        # El cálculo se ajusta en self.calcular().
        pass

    def calcular(self):
        # Leer P(A) y P(B) obligatorios
        try:
            PA = self.leer_prob_obligatoria(self.entry_PA, "P(A)")
            PB = self.leer_prob_obligatoria(self.entry_PB, "P(B)")
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        # Leer otros (opcionales o definidos según independencia)
        try:
            PAB_input = self.leer_prob_opcional(self.entry_PAB)
            PA_B_input = self.leer_prob_opcional(self.entry_PA_B)
            PB_A_input = self.leer_prob_opcional(self.entry_PB_A)
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
            return

        # Si independencia marcada, priorizar P(A∩B) = P(A)·P(B)
        if self.var_indep.get():
            PAB = PA * PB
            # Condicionales se deducen
            PA_B = PA if PB > 0 else None
            PB_A = PB if PA > 0 else None
        else:
            # Caso general: usamos lo que el alumno haya dado para completar
            PAB = PAB_input
            PA_B = PA_B_input
            PB_A = PB_A_input

            # Necesitamos al menos DOS piezas entre {PAB, PA|B, PB|A}
            num_datos = sum(v is not None for v in [PAB, PA_B, PB_A])
            if num_datos < 1:
                messagebox.showerror(
                    "Faltan datos",
                    "Debe proporcionar al menos uno de estos: P(A ∩ B), P(A|B) o P(B|A).\n"
                    "También puede marcar la casilla de independencia."
                )
                return

            # Completar faltantes con la ley de multiplicación
            # Usamos relaciones:
            # PAB = PB * P(A|B)
            # PAB = PA * P(B|A)

            # 1) Si tenemos PAB y P(A|B) falta PB → PB = PAB / P(A|B)
            # 2) Si tenemos PAB y P(B|A) falta PA → PA = PAB / P(B|A)
            # 3) Si tenemos P(A|B) y no PAB → PAB = PB * P(A|B)
            # 4) Si tenemos P(B|A) y no PAB → PAB = PA * P(B|A)

            # NOTA: como PA y PB ya vienen dados por el usuario, no los modificamos,
            #       solo ajustamos PAB, P(A|B), P(B|A) con consistencia.

            if PAB is None and PA_B is not None:
                PAB = PB * PA_B  # PAB = PB * P(A|B)
            if PAB is None and PB_A is not None:
                PAB = PA * PB_A  # PAB = PA * P(B|A)

            if PAB is not None and PA_B is None and PB > 0:
                PA_B = PAB / PB
            if PAB is not None and PB_A is None and PA > 0:
                PB_A = PAB / PA

        # Comprobaciones lógicas
        if PAB is None:
            messagebox.showerror(
                "Datos insuficientes",
                "No fue posible determinar P(A ∩ B). Revise los datos ingresados."
            )
            return

        if PAB > PA + 1e-8 or PAB > PB + 1e-8:
            messagebox.showerror(
                "Error lógico",
                "P(A ∩ B) no puede ser mayor que P(A) ni que P(B)."
            )
            return

        # Recorte por precisión numérica
        PAB = max(0, min(1, PAB))
        if PA_B is not None:
            PA_B = max(0, min(1, PA_B))
        if PB_A is not None:
            PB_A = max(0, min(1, PB_A))

        # Revisar independencia real aproximada
        independiente_real = abs(PAB - PA * PB) < 1e-6

        # Mostrar texto
        self.text_resultados.delete("1.0", tk.END)
        lineas = []
        lineas.append(f"P(A)      = {PA:.4f}")
        lineas.append(f"P(B)      = {PB:.4f}")
        lineas.append(f"P(A ∩ B)  = {PAB:.4f}")
        lineas.append("")
        if PA_B is not None:
            lineas.append("P(A | B) = P(A ∩ B) / P(B)")
            lineas.append(f"         = {PAB:.4f} / {PB:.4f} = {PA_B:.4f}")
        else:
            lineas.append("P(A | B) no definida (P(B) = 0).")
        lineas.append("")
        if PB_A is not None:
            lineas.append("P(B | A) = P(A ∩ B) / P(A)")
            lineas.append(f"         = {PAB:.4f} / {PA:.4f} = {PB_A:.4f}")
        else:
            lineas.append("P(B | A) no definida (P(A) = 0).")
        lineas.append("")
        lineas.append("Revisión de independencia:")
        lineas.append(f"   P(A)·P(B) = {PA*PB:.4f}")
        lineas.append(f"   P(A ∩ B)  = {PAB:.4f}")
        if independiente_real:
            lineas.append("   ⇒ A y B son (aprox.) INDEPENDIENTES.")
        else:
            lineas.append("   ⇒ A y B NO son independientes.")

        if self.var_indep.get():
            lineas.append("")
            lineas.append("Se marcó la casilla de independencia, por lo que se ha usado:")
            lineas.append("   P(A ∩ B) = P(A)·P(B)")
            lineas.append("   P(A | B) = P(A),   P(B | A) = P(B).")

        self.text_resultados.insert(tk.END, "\n".join(lineas))

        # Dibujar gráfico
        self.dibujar_barras(PA, PB, PAB, PA_B, PB_A)

    def dibujar_barras(self, PA, PB, PAB, PA_B, PB_A):
        for w in self.canvas_frame.winfo_children():
            w.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 4))
        fig.patch.set_facecolor("#ffffff")

        etiquetas = ["P(A)", "P(B)", "P(A∩B)"]
        valores = [PA, PB, PAB]
        colores = ["#3498db", "#e74c3c", "#9b59b6"]

        if PA_B is not None:
            etiquetas.append("P(A|B)")
            valores.append(PA_B)
            colores.append("#27ae60")
        if PB_A is not None:
            etiquetas.append("P(B|A)")
            valores.append(PB_A)
            colores.append("#f1c40f")

        ax.bar(etiquetas, valores, color=colores)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Probabilidad")
        ax.set_title("Probabilidades simples, conjuntas y condicionales")

        for i, v in enumerate(valores):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=9)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------- Ejemplos y limpiar ----------

    def ejemplo_general(self):
        """
        Ejemplo general (no necesariamente independiente):
        P(A) = 0.6, P(B) = 0.5, P(A ∩ B) = 0.3
        """
        self.var_indep.set(False)

        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)
        self.entry_PA_B.delete(0, tk.END)
        self.entry_PB_A.delete(0, tk.END)

        self.entry_PA.insert(0, "0.6")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.3")
        self.calcular()

    def ejemplo_indep(self):
        """
        Ejemplo con independencia:
        P(A) = 0.4, P(B) = 0.5  ⇒  P(A ∩ B) = 0.2
        """
        self.var_indep.set(True)

        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)
        self.entry_PA_B.delete(0, tk.END)
        self.entry_PB_A.delete(0, tk.END)

        self.entry_PA.insert(0, "0.4")
        self.entry_PB.insert(0, "0.5")
        # P(A ∩ B) se ajustará automáticamente a 0.4*0.5 en calcular()
        self.calcular()

    def limpiar(self):
        self.var_indep.set(False)

        self.entry_PA.delete(0, tk.END)
        self.entry_PB.delete(0, tk.END)
        self.entry_PAB.delete(0, tk.END)
        self.entry_PA_B.delete(0, tk.END)
        self.entry_PB_A.delete(0, tk.END)

        self.entry_PA.insert(0, "0.6")
        self.entry_PB.insert(0, "0.5")
        self.entry_PAB.insert(0, "0.3")

        self.text_resultados.delete("1.0", tk.END)
        for w in self.canvas_frame.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LeyMultiplicacionApp(root)
    root.mainloop()