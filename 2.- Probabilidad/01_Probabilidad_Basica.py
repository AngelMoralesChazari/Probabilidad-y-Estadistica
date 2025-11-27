import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import gcd


class ProbabilidadBasicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Probabilidad Básica - Definición Clásica")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        title_label = tk.Label(
            main_frame,
            text="📊 Probabilidad Básica",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=5)

        desc_label = tk.Label(
            main_frame,
            text="Calcula la probabilidad de un evento A usando la fórmula clásica: P(A) = casos favorables / casos posibles",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 10))

        # ---- Entradas ----
        input_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=5, pady=5)

        # Casos posibles
        tk.Label(
            input_frame,
            text="Casos posibles (espacio muestral):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_posibles = tk.Entry(input_frame, font=("Arial", 11), width=15)
        self.entry_posibles.insert(0, "52")
        self.entry_posibles.grid(row=0, column=1, padx=10, pady=10)

        # Casos favorables
        tk.Label(
            input_frame,
            text="Casos favorables (evento A):",
            font=("Arial", 11),
            bg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_favorables = tk.Entry(input_frame, font=("Arial", 11), width=15)
        self.entry_favorables.insert(0, "13")
        self.entry_favorables.grid(row=1, column=1, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(input_frame, bg="#ffffff")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

        btn_calc = tk.Button(
            btn_frame,
            text="Calcular Probabilidad",
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular
        )
        btn_calc.pack(side="left", padx=5)

        btn_ejemplo = tk.Button(
            btn_frame,
            text="Ejemplo: Dado",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_dado
        )
        btn_ejemplo.pack(side="left", padx=5)

        btn_ejemplo2 = tk.Button(
            btn_frame,
            text="Ejemplo: Baraja",
            font=("Arial", 11, "bold"),
            bg="#9b59b6",
            fg="white",
            cursor="hand2",
            command=self.ejemplo_baraja
        )
        btn_ejemplo2.pack(side="left", padx=5)

        btn_limpiar = tk.Button(
            btn_frame,
            text="Limpiar",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar
        )
        btn_limpiar.pack(side="left", padx=5)

        # ---- Resultados ----
        results_frame = tk.Frame(main_frame, bg="#f0f0f0")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Izquierda: texto y tabla
        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            left_frame,
            text="📝 Resultados:",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        ).pack(pady=(10, 5))

        # Tabla
        table_frame = tk.Frame(left_frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("concepto", "valor"),
            show="headings",
            height=5
        )
        self.tree.heading("concepto", text="Concepto")
        self.tree.heading("valor", text="Valor")

        self.tree.column("concepto", width=250, anchor="w")
        self.tree.column("valor", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Explicación
        tk.Label(
            left_frame,
            text="📖 Explicación paso a paso:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        self.text_explicacion = tk.Text(
            left_frame,
            height=8,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_explicacion.pack(fill="both", expand=True, padx=10, pady=5)

        # Derecha: gráfico
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📊 Gráfica:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Info teórica ----
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Probabilidad Clásica (Laplace): "
            "P(A) = (casos favorables) / (casos posibles). "
            "Supone que todos los resultados son igualmente probables. "
            "El valor siempre está entre 0 (imposible) y 1 (seguro). "
            "Ejemplo: probabilidad de sacar un as de una baraja = 4/52 = 1/13 ≈ 7.69%."
        )

        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left",
            anchor="w",
            wraplength=850
        )
        info_label.pack(fill="x", padx=10, pady=8)

    def ejemplo_dado(self):
        """Ejemplo: probabilidad de sacar un número par en un dado"""
        self.entry_posibles.delete(0, tk.END)
        self.entry_favorables.delete(0, tk.END)
        self.entry_posibles.insert(0, "6")
        self.entry_favorables.insert(0, "3")
        self.calcular()

    def ejemplo_baraja(self):
        """Ejemplo: probabilidad de sacar un corazón de una baraja"""
        self.entry_posibles.delete(0, tk.END)
        self.entry_favorables.delete(0, tk.END)
        self.entry_posibles.insert(0, "52")
        self.entry_favorables.insert(0, "13")
        self.calcular()

    def calcular(self):
        try:
            posibles = int(self.entry_posibles.get())
            favorables = int(self.entry_favorables.get())

            if posibles <= 0 or favorables < 0:
                raise ValueError

            if favorables > posibles:
                messagebox.showerror(
                    "Error",
                    "Los casos favorables no pueden ser mayores que los casos posibles."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese valores enteros válidos."
            )
            return

        # Calcular probabilidad
        prob_decimal = favorables / posibles
        prob_porcentaje = prob_decimal * 100

        # Simplificar fracción
        divisor = gcd(favorables, posibles)
        frac_num = favorables // divisor
        frac_den = posibles // divisor

        # Complemento
        no_favorables = posibles - favorables
        prob_complemento = no_favorables / posibles

        # Llenar tabla
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=("Casos posibles", posibles))
        self.tree.insert("", "end", values=("Casos favorables", favorables))
        self.tree.insert("", "end", values=(f"P(A) = {frac_num}/{frac_den}", f"{prob_decimal:.6f}"))
        self.tree.insert("", "end", values=("P(A) en porcentaje", f"{prob_porcentaje:.2f}%"))
        self.tree.insert("", "end", values=("P(A') - Complemento", f"{prob_complemento:.6f}"))

        # Explicación
        self.text_explicacion.delete("1.0", tk.END)
        explic = []
        explic.append(f"Espacio muestral: {posibles} casos posibles")
        explic.append(f"Evento A: {favorables} casos favorables")
        explic.append("")
        explic.append(f"P(A) = {favorables} / {posibles}")
        if divisor > 1:
            explic.append(f"     = {frac_num} / {frac_den}  (simplificado)")
        explic.append(f"     = {prob_decimal:.6f}")
        explic.append(f"     = {prob_porcentaje:.2f}%")
        explic.append("")
        explic.append(f"Complemento P(A') = 1 - P(A) = {prob_complemento:.6f}")
        explic.append(f"                  = {no_favorables}/{posibles}")

        self.text_explicacion.insert(tk.END, "\n".join(explic))

        # Dibujar gráfico
        self.dibujar_grafico(favorables, no_favorables, prob_porcentaje)

    def dibujar_grafico(self, favorables, no_favorables, prob_porcentaje):
        # Limpiar canvas anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        labels = [f'Favorables\n({favorables})', f'No favorables\n({no_favorables})']
        sizes = [favorables, no_favorables]
        colors = ['#27ae60', '#e74c3c']
        explode = (0.1, 0)

        ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            textprops={'fontsize': 11}
        )
        ax.set_title(f"P(A) = {prob_porcentaje:.2f}%", fontsize=13, fontweight='bold')

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.entry_posibles.delete(0, tk.END)
        self.entry_favorables.delete(0, tk.END)
        self.entry_posibles.insert(0, "52")
        self.entry_favorables.insert(0, "13")

        self.tree.delete(*self.tree.get_children())
        self.text_explicacion.delete("1.0", tk.END)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProbabilidadBasicaApp(root)
    root.mainloop()