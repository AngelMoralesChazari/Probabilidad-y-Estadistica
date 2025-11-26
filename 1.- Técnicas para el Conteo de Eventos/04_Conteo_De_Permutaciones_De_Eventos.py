import tkinter as tk
from tkinter import ttk, messagebox
import math
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PermutacionesRepeticionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔁 Conteo de Permutaciones con Repetición")
        self.root.geometry("950x650")
        self.root.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        title_label = tk.Label(
            main_frame,
            text="🔁 Permutaciones de Eventos con Repetición",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=5)

        desc_label = tk.Label(
            main_frame,
            text="Cuenta las distintas maneras de ordenar elementos cuando algunos se repiten (por ejemplo, letras de una palabra).",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 10))

        # ---- Entrada: palabra ----
        input_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        input_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            input_frame,
            text="Ingresa una palabra o secuencia de símbolos:",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side="left", padx=(10, 5), pady=10)

        self.entry_palabra = tk.Entry(input_frame, font=("Arial", 11), width=25)
        self.entry_palabra.insert(0, "MAMA")
        self.entry_palabra.pack(side="left", padx=5)

        btn_calc = tk.Button(
            input_frame,
            text="Calcular permutaciones",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_desde_palabra
        )
        btn_calc.pack(side="left", padx=15)

        btn_ejemplo = tk.Button(
            input_frame,
            text="Ejemplo: BANANA",
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

        self.label_resultado = tk.Label(
            left_frame,
            text="Permutaciones distintas: -",
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
            height=10,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_pasos.pack(fill="x", padx=10, pady=5)

        # Tabla de frecuencias
        tk.Label(
            left_frame,
            text="📋 Frecuencia de cada símbolo:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        table_frame = tk.Frame(left_frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("simbolo", "frecuencia"),
            show="headings",
            height=6
        )
        self.tree.heading("simbolo", text="Símbolo")
        self.tree.heading("frecuencia", text="Frecuencia")
        self.tree.column("simbolo", width=100, anchor="center")
        self.tree.column("frecuencia", width=100, anchor="center")

        scrollbar_table = tk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_table.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")

        # Derecha - gráfica
        right_frame = tk.Frame(results_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📈 Frecuencia de símbolos:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Info teórica abajo ----
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Permutaciones con repetición:\n"
            "Si tenemos un total de n elementos, donde "
            "n₁ son iguales de un tipo, n₂ son iguales de otro tipo, "
            "..., hasta nᵣ, entonces el número de permutaciones distintas es:\n"
            "n! / (n₁! · n₂! · ... · nᵣ!)\n"
            "Ejemplo: BANANA → 6 letras en total (3 A, 2 N, 1 B). "
            "Permutaciones = 6! / (3! · 2! · 1!)"
        )

        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left",
            anchor="w",       # alinea el texto a la izquierda dentro del label
            wraplength=850    # ancho máximo en píxeles para hacer saltos de línea
        )
        info_label.pack(fill="x", padx=10, pady=8)

    def cargar_ejemplo(self):
        self.entry_palabra.delete(0, tk.END)
        self.entry_palabra.insert(0, "BANANA")
        self.calcular_desde_palabra()

    def calcular_desde_palabra(self):
        texto = self.entry_palabra.get().strip()

        if not texto:
            messagebox.showerror("Error", "Por favor ingresa una palabra o secuencia de símbolos.")
            return

        # Para facilidad visual, usamos mayúsculas
        texto = texto.upper()

        # Contar frecuencias
        conteo = Counter(texto)
        n = len(texto)

        # Evitar casos ridículamente largos
        if n > 20:
            messagebox.showwarning(
                "Advertencia",
                "La longitud es mayor que 20; se limitará a los primeros 20 símbolos para el cálculo."
            )
            texto = texto[:20]
            conteo = Counter(texto)
            n = len(texto)
            self.entry_palabra.delete(0, tk.END)
            self.entry_palabra.insert(0, texto)

        # Listas ordenadas por símbolo
        simbolos = sorted(conteo.keys())
        frecuencias = [conteo[s] for s in simbolos]

        # Cálculo del número de permutaciones
        n_fact = math.factorial(n)
        denominador = 1
        for ni in frecuencias:
            denominador *= math.factorial(ni)
        permutaciones = n_fact // denominador

        # Mostrar resultado principal
        self.label_resultado.config(
            text=f"Permutaciones distintas: {permutaciones:,}".replace(",", " ")
        )

        # Mostrar pasos
        self.text_pasos.delete("1.0", tk.END)

        pasos = []
        pasos.append(f"Texto analizado: {texto}")
        pasos.append(f"Longitud total n = {n}")
        pasos.append("")
        pasos.append("Frecuencias:")
        for s, f in zip(simbolos, frecuencias):
            pasos.append(f"  {s}: {f}")
        pasos.append("")
        pasos.append("Fórmula:")
        pasos.append("  n! / (n₁! · n₂! · ... · nᵣ!)")
        pasos.append("")
        pasos.append(f"n! = {n}! = {n_fact:,}".replace(",", " "))

        denom_str_partes = []
        for s, f in zip(simbolos, frecuencias):
            pasos.append(f"{f}! (por {s}) = {math.factorial(f):,}".replace(",", " "))
            denom_str_partes.append(f"{f}!")
        denom_str = " · ".join(denom_str_partes)
        pasos.append("")
        pasos.append(f"Denominador = {denom_str}")
        pasos.append(f"Valor del denominador = {denominador:,}".replace(",", " "))
        pasos.append("")
        pasos.append(
            f"Permutaciones = {n}! / ({denom_str}) = {n_fact:,} / {denominador:,} = {permutaciones:,}".replace(",", " ")
        )

        pasos.append("")
        pasos.append("Interpretación:")
        pasos.append(
            "Si todas las letras fueran distintas, habría n! formas de acomodarlas.\n"
            "Pero cuando algunas se repiten, varias de esas acomodaciones son indistinguibles.\n"
            "Por eso dividimos entre los factoriales de las frecuencias."
        )

        self.text_pasos.insert(tk.END, "\n".join(pasos))

        # Llenar tabla
        self.tree.delete(*self.tree.get_children())
        for s, f in zip(simbolos, frecuencias):
            self.tree.insert("", "end", values=(s, f))

        # Crear gráfica
        self.crear_grafica(simbolos, frecuencias)

    def crear_grafica(self, simbolos, frecuencias):
        # Limpiar gráfica anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        x = range(len(simbolos))
        ax.bar(x, frecuencias, color="#9b59b6", alpha=0.8, edgecolor="#5e3370")

        ax.set_xticks(list(x))
        ax.set_xticklabels(simbolos, fontsize=10)
        ax.set_xlabel("Símbolos", fontsize=10, fontweight="bold")
        ax.set_ylabel("Frecuencia", fontsize=10, fontweight="bold")
        ax.set_title("Frecuencia de cada símbolo", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        ax.set_facecolor("#f8f9fa")

        for i, f in enumerate(frecuencias):
            ax.text(i, f, str(f), ha="center", va="bottom", fontsize=9)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.entry_palabra.delete(0, tk.END)
        self.entry_palabra.insert(0, "MAMA")
        self.label_resultado.config(text="Permutaciones distintas: -")
        self.text_pasos.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PermutacionesRepeticionApp(root)
    root.mainloop()