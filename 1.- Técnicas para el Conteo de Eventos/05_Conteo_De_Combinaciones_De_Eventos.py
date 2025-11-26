import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CombinacionesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Conteo de Combinaciones de Eventos")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        title_label = tk.Label(
            main_frame,
            text="🧩 Combinaciones: Elegir sin importar el orden",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=5)

        desc_label = tk.Label(
            main_frame,
            text="Cuenta cuántas formas hay de ELEGIR k elementos de un conjunto de n, cuando el orden NO importa.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 10))

        # ---- Entrada: n y k ----
        input_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            input_frame,
            text="Número total de elementos (n):",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side="left", padx=(10, 5), pady=10)

        self.entry_n = tk.Entry(input_frame, font=("Arial", 11), width=8)
        self.entry_n.insert(0, "5")
        self.entry_n.pack(side="left", padx=5)

        tk.Label(
            input_frame,
            text="Elementos a elegir (k):",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side="left", padx=(20, 5))

        self.entry_k = tk.Entry(input_frame, font=("Arial", 11), width=8)
        self.entry_k.insert(0, "3")
        self.entry_k.pack(side="left", padx=5)

        btn_calc = tk.Button(
            input_frame,
            text="Calcular combinaciones",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular
        )
        btn_calc.pack(side="left", padx=15)

        btn_ejemplo = tk.Button(
            input_frame,
            text="Ejemplo: n=5, k=3",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.cargar_ejemplo
        )
        btn_ejemplo.pack(side="left", padx=5)

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

        self.label_cnk = tk.Label(
            left_frame,
            text="C(n, k) = -",
            font=("Arial", 16, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        self.label_cnk.pack(pady=(10, 5))

        self.label_pnk = tk.Label(
            left_frame,
            text="P(n, k) = -   (para comparar con permutaciones)",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#e67e22"
        )
        self.label_pnk.pack(pady=(0, 10))

        # Cálculo paso a paso
        tk.Label(
            left_frame,
            text="📝 Cálculo paso a paso:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.text_pasos = tk.Text(
            left_frame,
            height=11,
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
            columns=("n", "k", "n_fact", "k_fact", "n_k_fact", "c_nk", "p_nk"),
            show="headings",
            height=5
        )
        self.tree.heading("n", text="n")
        self.tree.heading("k", text="k")
        self.tree.heading("n_fact", text="n!")
        self.tree.heading("k_fact", text="k!")
        self.tree.heading("n_k_fact", text="(n-k)!")
        self.tree.heading("c_nk", text="C(n,k)")
        self.tree.heading("p_nk", text="P(n,k)")

        self.tree.column("n", width=40, anchor="center")
        self.tree.column("k", width=40, anchor="center")
        self.tree.column("n_fact", width=110, anchor="center")
        self.tree.column("k_fact", width=110, anchor="center")
        self.tree.column("n_k_fact", width=110, anchor="center")
        self.tree.column("c_nk", width=110, anchor="center")
        self.tree.column("p_nk", width=110, anchor="center")

        scrollbar_table = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_table.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")

        # Derecha - gráfica
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📈 Comparación combinaciones vs permutaciones:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Info teórica abajo ----
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Combinaciones (sin orden):\n"
            "Si tenemos n elementos distintos y queremos ELEGIR k de ellos, sin importar el orden, usamos:\n"
            "  C(n, k) = n! / (k! · (n - k)!)\n"
            "Ejemplo: n = 5 estudiantes y elegimos k = 3 para formar un equipo.\n"
            "  C(5, 3) = 5! / (3! · 2!) = 10 formas de elegir el equipo.\n"
            "Si contáramos PERMUTACIONES P(5, 3), estaríamos contando también el orden dentro del equipo."
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
        self.entry_n.delete(0, tk.END)
        self.entry_k.delete(0, tk.END)
        self.entry_n.insert(0, "5")
        self.entry_k.insert(0, "3")
        self.calcular()

    def calcular(self):
        # Leer n y k
        try:
            n = int(self.entry_n.get())
            k = int(self.entry_k.get())

            if n <= 0 or k < 0:
                raise ValueError

            if k > n:
                messagebox.showerror("Error", "k no puede ser mayor que n.")
                return

            if n > 25:
                messagebox.showwarning(
                    "Advertencia",
                    "n es grande; se limitará el cálculo a n = 25 para evitar números demasiado grandes."
                )
                n = 25
                if k > n:
                    k = n
                self.entry_n.delete(0, tk.END)
                self.entry_n.insert(0, str(n))
                self.entry_k.delete(0, tk.END)
                self.entry_k.insert(0, str(k))

        except ValueError:
            messagebox.showerror("Error", "n debe ser entero positivo y k entero no negativo.")
            return

        # Factoriales
        n_fact = math.factorial(n)
        k_fact = math.factorial(k)
        n_k_fact = math.factorial(n - k)

        # Combinaciones y permutaciones
        c_nk = n_fact // (k_fact * n_k_fact)
        p_nk = n_fact // n_k_fact  # P(n,k)

        # Mostrar resultados principales
        self.label_cnk.config(text=f"C({n}, {k}) = {c_nk:,}".replace(",", " "))
        self.label_pnk.config(text=f"P({n}, {k}) = {p_nk:,}   (permutaciones)".replace(",", " "))

        # Texto paso a paso
        self.text_pasos.delete("1.0", tk.END)

        pasos = []
        pasos.append(f"n = {n}, k = {k}")
        pasos.append("")
        pasos.append("Fórmula de combinaciones:")
        pasos.append("  C(n, k) = n! / (k! · (n - k)!)")
        pasos.append("")
        pasos.append(f"n!     = {n}! = {n_fact:,}".replace(",", " "))
        pasos.append(f"k!     = {k}! = {k_fact:,}".replace(",", " "))
        pasos.append(f"(n-k)! = ({n-k})! = {n_k_fact:,}".replace(",", " "))
        pasos.append("")
        pasos.append(
            f"C({n}, {k}) = {n_fact:,} / ({k_fact:,} · {n_k_fact:,}) = {c_nk:,}".replace(",", " ")
        )
        pasos.append("")
        pasos.append("Relación con permutaciones:")
        pasos.append("  P(n, k) = n! / (n - k)!")
        pasos.append(
            f"P({n}, {k}) = {n_fact:,} / {n_k_fact:,} = {p_nk:,}".replace(",", " ")
        )
        pasos.append("")
        pasos.append("Interpretación:")
        pasos.append(
            "P(n, k) cuenta ordenaciones distintas de k elementos elegidos de n.\n"
            "C(n, k) cuenta solo los GRUPOS distintos (equipos, subconjuntos), sin importar el orden interno.\n"
            "Por eso C(n, k) es más pequeño: cada grupo se cuenta muchas veces en P(n,k),\n"
            "una vez por cada forma de ordenar sus k elementos (k! veces)."
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
                f"{k_fact:,}".replace(",", " "),
                f"{n_k_fact:,}".replace(",", " "),
                f"{c_nk:,}".replace(",", " "),
                f"{p_nk:,}".replace(",", " ")
            )
        )

        # Gráfica
        self.crear_grafica(c_nk, p_nk)

    def crear_grafica(self, c_nk, p_nk):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        categorias = ["C(n,k)", "P(n,k)"]
        valores = [c_nk, p_nk]
        colores = ["#2ecc71", "#e67e22"]

        ax.bar(categorias, valores, color=colores, alpha=0.85, edgecolor="#2c3e50")

        ax.set_ylabel("Valor", fontsize=10, fontweight="bold")
        ax.set_title("Combinaciones vs Permutaciones", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        ax.set_facecolor("#f8f9fa")

        for i, v in enumerate(valores):
            ax.text(i, v, f"{v}", ha="center", va="bottom", fontsize=9)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.entry_n.delete(0, tk.END)
        self.entry_k.delete(0, tk.END)
        self.entry_n.insert(0, "5")
        self.entry_k.insert(0, "3")

        self.label_cnk.config(text="C(n, k) = -")
        self.label_pnk.config(text="P(n, k) = -   (para comparar con permutaciones)")
        self.text_pasos.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CombinacionesApp(root)
    root.mainloop()