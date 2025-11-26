import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class OrdenacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔄 Conteo de Ordenaciones de Eventos (Permutaciones)")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        title_label = tk.Label(
            main_frame,
            text="🔄 Conteo de Ordenaciones de Eventos",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=5)

        desc_label = tk.Label(
            main_frame,
            text="Se cuentan las distintas maneras de ordenar k elementos tomados de un conjunto de n elementos distintos.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 10))

        # ---- Entrada de datos (n y k) ----
        input_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=5, pady=5)

        # n
        tk.Label(
            input_frame,
            text="Número total de elementos (n):",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side="left", padx=(10, 5), pady=10)

        self.entry_n = tk.Entry(input_frame, font=("Arial", 11), width=8)
        self.entry_n.insert(0, "5")
        self.entry_n.pack(side="left", padx=5)

        # k
        tk.Label(
            input_frame,
            text="Elementos en la ordenación (k):",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side="left", padx=(20, 5))

        self.entry_k = tk.Entry(input_frame, font=("Arial", 11), width=8)
        self.entry_k.insert(0, "5")
        self.entry_k.pack(side="left", padx=5)

        btn_calc = tk.Button(
            input_frame,
            text="Calcular",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular
        )
        btn_calc.pack(side="left", padx=15)

        btn_auto_k = tk.Button(
            input_frame,
            text="Usar k = n",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.usar_k_igual_n
        )
        btn_auto_k.pack(side="left", padx=5)

        btn_limpiar = tk.Button(
            input_frame,
            text="Limpiar",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar
        )
        btn_limpiar.pack(side="left", padx=10)

        # ---- Resultados: izquierda (texto/tabla) y derecha (gráfica) ----
        results_frame = tk.Frame(main_frame, bg="#f0f0f0")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Izquierda
        left_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.label_resultado = tk.Label(
            left_frame,
            text="P(n, k) = -",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        self.label_resultado.pack(pady=(10, 5))

        # Cálculo paso a paso
        tk.Label(
            left_frame,
            text="📝 Cálculo paso a paso:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.text_pasos = tk.Text(
            left_frame,
            height=9,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_pasos.pack(fill="x", padx=10, pady=5)

        # Tabla resumen
        tk.Label(
            left_frame,
            text="📋 Resumen de valores:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        table_frame = tk.Frame(left_frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("n", "k", "n_fact", "n_k_fact", "p_nk"),
            show="headings",
            height=5
        )
        self.tree.heading("n", text="n")
        self.tree.heading("k", text="k")
        self.tree.heading("n_fact", text="n!")
        self.tree.heading("n_k_fact", text="(n-k)!")
        self.tree.heading("p_nk", text="P(n, k)")

        self.tree.column("n", width=50, anchor="center")
        self.tree.column("k", width=50, anchor="center")
        self.tree.column("n_fact", width=140, anchor="center")
        self.tree.column("n_k_fact", width=140, anchor="center")
        self.tree.column("p_nk", width=160, anchor="center")

        scrollbar_table = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_table.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")

        # Derecha - gráfica
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📈 Comparación de valores factoriales y P(n, k):",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Info teórica ----
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Ordenaciones y permutaciones:\n"
            "Si tenemos n elementos distintos y queremos ordenarlos tomando k de ellos (sin repetición),\n"
            "el número de ordenaciones posibles es la permutación:\n"
            "    P(n, k) = n × (n-1) × (n-2) × ... × (n-k+1) = n! / (n-k)!\n"
            "En el caso particular donde k = n, simplemente contamos todas las formas de ordenar los n elementos:\n"
            "    P(n, n) = n!"
        )

        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left"
        ).pack(padx=10, pady=8)

    def usar_k_igual_n(self):
        """Copia el valor de n dentro de k."""
        try:
            n = int(self.entry_n.get())
            if n <= 0:
                raise ValueError
            self.entry_k.delete(0, tk.END)
            self.entry_k.insert(0, str(n))
        except ValueError:
            messagebox.showerror("Error", "n debe ser un entero positivo antes de usar k = n.")

    def calcular(self):
        # Leer n y k
        try:
            n = int(self.entry_n.get())
            k = int(self.entry_k.get())

            if n <= 0 or k <= 0:
                raise ValueError

            if k > n:
                messagebox.showerror("Error", "k no puede ser mayor que n (no puedes ordenar más elementos de los que tienes).")
                return

            if n > 20:
                messagebox.showwarning(
                    "Advertencia",
                    "n es grande; se limitará el cálculo a n = 20 para evitar números demasiado grandes."
                )
                n = 20
                if k > n:
                    k = n
                self.entry_n.delete(0, tk.END)
                self.entry_n.insert(0, str(n))
                self.entry_k.delete(0, tk.END)
                self.entry_k.insert(0, str(k))

        except ValueError:
            messagebox.showerror("Error", "n y k deben ser enteros positivos.")
            return

        # Cálculos factoriales
        n_fact = math.factorial(n)
        n_k_fact = math.factorial(n - k)
        p_nk = n_fact // n_k_fact

        # Resultado principal
        self.label_resultado.config(
            text=f"P({n}, {k}) = {p_nk:,}".replace(",", " ")
        )

        # Texto paso a paso
        self.text_pasos.delete("1.0", tk.END)

        pasos = []
        # Forma producto directo
        terminos = [str(n - i) for i in range(k)]  # n, n-1, ..., n-k+1
        producto_str = " × ".join(terminos)

        pasos.append(f"P({n}, {k}) = {producto_str}")
        pasos.append("")
        pasos.append(f"Usando factoriales:")
        pasos.append(f"P({n}, {k}) = n! / (n - k)! = {n}! / ({n-k})!")
        pasos.append(f"{n}! = {n_fact:,}".replace(",", " "))
        pasos.append(f"({n-k})! = {n_k_fact:,}".replace(",", " "))
        pasos.append(f"P({n}, {k}) = {n_fact:,} / {n_k_fact:,} = {p_nk:,}".replace(",", " "))

        pasos.append("")
        pasos.append("Interpretación:")
        pasos.append(
            "Primero eliges qué elemento va en la primera posición (n opciones),\n"
            "luego en la segunda (n-1 opciones), y así sucesivamente hasta completar k posiciones."
        )

        self.text_pasos.insert(tk.END, "\n".join(pasos))

        # Tabla
        self.tree.delete(*self.tree.get_children())
        self.tree.insert(
            "",
            "end",
            values=(
                n,
                k,
                f"{n_fact:,}".replace(",", " "),
                f"{n_k_fact:,}".replace(",", " "),
                f"{p_nk:,}".replace(",", " ")
            )
        )

        # Gráfica
        self.crear_grafica(n_fact, n_k_fact, p_nk)

    def crear_grafica(self, n_fact, n_k_fact, p_nk):
        # Limpiar cualquier gráfica anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        categorias = ["n!", "(n-k)!", "P(n,k)"]
        valores = [n_fact, n_k_fact, p_nk]
        colores = ["#3498db", "#9b59b6", "#e67e22"]

        ax.bar(categorias, valores, color=colores, alpha=0.85, edgecolor="#2c3e50")

        ax.set_ylabel("Valor", fontsize=10, fontweight="bold")
        ax.set_title("Comparación de n!, (n-k)! y P(n,k)", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        ax.set_facecolor("#f8f9fa")

        # Mostrar los valores encima de las barras (si no son demasiado grandes)
        for i, v in enumerate(valores):
            ax.text(
                i,
                v,
                f"{v}",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0
            )

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.entry_n.delete(0, tk.END)
        self.entry_k.delete(0, tk.END)
        self.entry_n.insert(0, "5")
        self.entry_k.insert(0, "5")

        self.label_resultado.config(text="P(n, k) = -")
        self.text_pasos.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrdenacionesApp(root)
    root.mainloop()