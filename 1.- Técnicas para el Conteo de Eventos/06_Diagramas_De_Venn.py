import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle, Rectangle


class Venn2App:
    def __init__(self, root):
        self.root = root
        self.root.title("🔵 Diagramas de Venn - 2 Conjuntos")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        title_label = tk.Label(
            main_frame,
            text="🔵 Diagrama de Venn con 2 conjuntos (A y B)",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=5)

        desc_label = tk.Label(
            main_frame,
            text="Ingresa las cardinalidades para visualizar cómo se reparten los elementos en A, B y su intersección.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 10))

        # ---- Entradas ----
        input_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=5, pady=5)

        # |U|
        tk.Label(
            input_frame,
            text="Tamaño del universo |U| (opcional):",
            font=("Arial", 10),
            bg="#ffffff"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry_U = tk.Entry(input_frame, font=("Arial", 10), width=8)
        self.entry_U.grid(row=0, column=1, padx=5, pady=5)

        # |A|
        tk.Label(
            input_frame,
            text="|A|:",
            font=("Arial", 10),
            bg="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.entry_A = tk.Entry(input_frame, font=("Arial", 10), width=8)
        self.entry_A.insert(0, "30")
        self.entry_A.grid(row=1, column=1, padx=5, pady=5)

        # |B|
        tk.Label(
            input_frame,
            text="|B|:",
            font=("Arial", 10),
            bg="#ffffff"
        ).grid(row=1, column=2, padx=(20, 5), pady=5, sticky="w")

        self.entry_B = tk.Entry(input_frame, font=("Arial", 10), width=8)
        self.entry_B.insert(0, "25")
        self.entry_B.grid(row=1, column=3, padx=5, pady=5)

        # |A ∩ B|
        tk.Label(
            input_frame,
            text="|A ∩ B|:",
            font=("Arial", 10),
            bg="#ffffff"
        ).grid(row=1, column=4, padx=(20, 5), pady=5, sticky="w")

        self.entry_AB = tk.Entry(input_frame, font=("Arial", 10), width=8)
        self.entry_AB.insert(0, "10")
        self.entry_AB.grid(row=1, column=5, padx=5, pady=5)

        # Botones
        btn_calc = tk.Button(
            input_frame,
            text="Calcular regiones",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular
        )
        btn_calc.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        btn_ejemplo = tk.Button(
            input_frame,
            text="Ejemplo típico",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.cargar_ejemplo
        )
        btn_ejemplo.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        btn_limpiar = tk.Button(
            input_frame,
            text="Limpiar",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar
        )
        btn_limpiar.grid(row=2, column=4, columnspan=2, padx=10, pady=10, sticky="e")

        # ---- Resultados: izquierda tabla/texto, derecha diagrama ----
        results_frame = tk.Frame(main_frame, bg="#f0f0f0")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Izquierda
        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.label_resumen = tk.Label(
            left_frame,
            text="Regiones del diagrama:",
            font=("Arial", 13, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        self.label_resumen.pack(pady=(10, 5))

        # Tabla
        table_frame = tk.Frame(left_frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("region", "descripcion", "valor"),
            show="headings",
            height=6
        )
        self.tree.heading("region", text="Región")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("valor", text="Valor")

        self.tree.column("region", width=80, anchor="center")
        self.tree.column("descripcion", width=220, anchor="w")
        self.tree.column("valor", width=80, anchor="center")

        scrollbar_table = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_table.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")

        # Texto explicativo
        tk.Label(
            left_frame,
            text="📝 Explicación:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.text_explicacion = tk.Text(
            left_frame,
            height=7,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_explicacion.pack(fill="x", padx=10, pady=5)

        # Derecha - diagrama
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📊 Diagrama de Venn (A y B):",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Info teórica abajo ----
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Diagrama de Venn con 2 conjuntos:\n"
            "Un elemento puede estar solo en A, solo en B, en ambos (A ∩ B) o en ninguno.\n"
            "Regiones:\n"
            "  - Solo A    = |A| - |A ∩ B|\n"
            "  - Solo B    = |B| - |A ∩ B|\n"
            "  - A ∩ B     = intersección\n"
            "  - Fuera de A,B (si se da |U|) = |U| - (Solo A + Solo B + A ∩ B)."
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

    def cargar_ejemplo(self):
        self.entry_U.delete(0, tk.END)
        self.entry_A.delete(0, tk.END)
        self.entry_B.delete(0, tk.END)
        self.entry_AB.delete(0, tk.END)

        self.entry_U.insert(0, "50")
        self.entry_A.insert(0, "30")
        self.entry_B.insert(0, "25")
        self.entry_AB.insert(0, "10")
        self.calcular()

    def calcular(self):
        # Leer valores
        try:
            A = int(self.entry_A.get())
            B = int(self.entry_B.get())
            AB = int(self.entry_AB.get())

            if A < 0 or B < 0 or AB < 0:
                raise ValueError

            if AB > A or AB > B:
                messagebox.showerror("Error", "|A ∩ B| no puede ser mayor que |A| ni que |B|.")
                return

            # Universo puede ser vacío (opcional)
            U_texto = self.entry_U.get().strip()
            U = None
            if U_texto:
                U = int(U_texto)
                if U < 0:
                    raise ValueError

        except ValueError:
            messagebox.showerror("Error", "Verifica que todos los valores sean enteros válidos.")
            return

        # Cálculo de regiones
        solo_A = A - AB
        solo_B = B - AB

        fuera = None
        if U is not None:
            usados = solo_A + solo_B + AB
            if usados > U:
                messagebox.showerror(
                    "Error",
                    "La suma de las regiones dentro de A y B es mayor que |U|."
                )
                return
            fuera = U - usados

        # Llenar tabla
        self.tree.delete(*self.tree.get_children())
        self.tree.insert("", "end", values=("Solo A", "Elementos solo en A", solo_A))
        self.tree.insert("", "end", values=("Solo B", "Elementos solo en B", solo_B))
        self.tree.insert("", "end", values=("A ∩ B", "Elementos en ambos", AB))
        if fuera is not None:
            self.tree.insert("", "end", values=("Fuera", "Elementos en U, pero no en A ni B", fuera))

        # Explicación
        self.text_explicacion.delete("1.0", tk.END)
        explic = []
        explic.append(f"|A| = {A}, |B| = {B}, |A ∩ B| = {AB}")
        if U is not None:
            explic.append(f"|U| = {U}")
        explic.append("")
        explic.append(f"Solo A = |A| - |A ∩ B| = {A} - {AB} = {solo_A}")
        explic.append(f"Solo B = |B| - |A ∩ B| = {B} - {AB} = {solo_B}")
        explic.append(f"A ∩ B = {AB}")
        if fuera is not None:
            explic.append("")
            explic.append(
                f"Fuera de A y B = |U| - (Solo A + Solo B + A ∩ B) = "
                f"{U} - ({solo_A} + {solo_B} + {AB}) = {fuera}"
            )

        self.text_explicacion.insert(tk.END, "\n".join(explic))

        # Dibujar diagrama
        self.dibujar_venn(solo_A, solo_B, AB, fuera)

    def dibujar_venn(self, solo_A, solo_B, AB, fuera):
        # Limpiar canvas anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")
        ax.set_aspect("equal")
        ax.axis("off")

        # Ajustar límites para que quepan bien los círculos
        ax.set_xlim(-3, 3)
        ax.set_ylim(-2, 2)

        # Fondo (universo)
        rect = Rectangle((-2.8, -1.8), 5.6, 3.6,
                         linewidth=1.5, edgecolor="#34495e", facecolor="#ecf0f1")
        ax.add_patch(rect)

        if fuera is not None:
            ax.text(-2.7, 1.6, f"U (fuera: {fuera})",
                    fontsize=9, ha="left", va="center")

        # Círculos A y B (más pequeños y mejor separados)
        radio = 1.0
        circle_A = Circle((-0.9, 0), radio, color="#3498db", alpha=0.5)
        circle_B = Circle((0.9, 0), radio, color="#e74c3c", alpha=0.5)
        ax.add_patch(circle_A)
        ax.add_patch(circle_B)

        # Etiquetas A y B
        ax.text(-0.9, 1.25, "A", fontsize=12, ha="center",
                va="center", color="#2c3e50")
        ax.text(0.9, 1.25, "B", fontsize=12, ha="center",
                va="center", color="#2c3e50")

        # Números en las regiones
        ax.text(-1.4, 0, str(solo_A), fontsize=13,
                ha="center", va="center")
        ax.text(1.4, 0, str(solo_B), fontsize=13,
                ha="center", va="center")
        ax.text(0, 0, str(AB), fontsize=13,
                ha="center", va="center", fontweight="bold")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.entry_U.delete(0, tk.END)
        self.entry_A.delete(0, tk.END)
        self.entry_B.delete(0, tk.END)
        self.entry_AB.delete(0, tk.END)

        self.entry_A.insert(0, "30")
        self.entry_B.insert(0, "25")
        self.entry_AB.insert(0, "10")

        self.tree.delete(*self.tree.get_children())
        self.text_explicacion.delete("1.0", tk.END)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Venn2App(root)
    root.mainloop()