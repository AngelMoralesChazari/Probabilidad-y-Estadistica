import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PrincipioConteoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Principio Fundamental de Conteo")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Estilo ttk
        style = ttk.Style()
        style.theme_use("clam")

        # Frame principal
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Título
        title_label = tk.Label(
            main_frame,
            text="🧮 Principio Fundamental de Conteo",
            font=("Arial", 20, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=5)

        # Descripción corta
        desc_label = tk.Label(
            main_frame,
            text="Multiplica el número de opciones de cada etapa para obtener el número total de resultados posibles.",
            font=("Arial", 11),
            bg="#f0f0f0",
            fg="#34495e"
        )
        desc_label.pack(pady=(0, 10))

        # ---- Sección configuración número de eventos ----
        config_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        config_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(
            config_frame,
            text="Número de eventos (etapas):",
            font=("Arial", 11),
            bg="#ffffff"
        ).pack(side="left", padx=10, pady=10)

        self.spin_eventos = tk.Spinbox(
            config_frame,
            from_=2,
            to=10,
            width=5,
            font=("Arial", 11),
            command=self.crear_campos_eventos
        )
        self.spin_eventos.pack(side="left", padx=5)

        btn_actualizar = tk.Button(
            config_frame,
            text="Actualizar eventos",
            font=("Arial", 10, "bold"),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            command=self.crear_campos_eventos
        )
        btn_actualizar.pack(side="left", padx=10)

        btn_calcular = tk.Button(
            config_frame,
            text="Calcular total",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            command=self.calcular_total
        )
        btn_calcular.pack(side="left", padx=10)

        btn_limpiar = tk.Button(
            config_frame,
            text="Limpiar",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            cursor="hand2",
            command=self.limpiar
        )
        btn_limpiar.pack(side="left", padx=10)

        # ---- Sección de entrada de opciones por evento ----
        self.eventos_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="raised")
        self.eventos_frame.pack(fill="x", padx=5, pady=5)

        self.campos_eventos = []
        self.crear_campos_eventos()  # inicial

        # ---- Sección de resultados (izquierda texto/tabla, derecha gráfica) ----
        resultados_frame = tk.Frame(main_frame, bg="#f0f0f0")
        resultados_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Izquierda
        left_frame = tk.Frame(resultados_frame, bg="#ffffff", bd=2, relief="raised")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Resultado total
        self.label_total = tk.Label(
            left_frame,
            text="Total de resultados posibles: -",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        self.label_total.pack(pady=(10, 5))

        # Proceso paso a paso
        tk.Label(
            left_frame,
            text="📝 Cálculo paso a paso:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(5, 0))

        self.text_proceso = tk.Text(
            left_frame,
            height=8,
            font=("Courier", 10),
            wrap="word"
        )
        self.text_proceso.pack(fill="x", padx=10, pady=5)

        # Tabla de eventos
        tk.Label(
            left_frame,
            text="📋 Tabla de eventos y opciones:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(10, 0))

        table_frame = tk.Frame(left_frame, bg="#ffffff")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("evento", "descripcion", "opciones"),
            show="headings",
            height=6
        )
        self.tree.heading("evento", text="Evento")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("opciones", text="Opciones")
        self.tree.column("evento", width=70, anchor="center")
        self.tree.column("descripcion", width=200, anchor="w")
        self.tree.column("opciones", width=100, anchor="center")

        scrollbar_table = tk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar_table.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_table.pack(side="right", fill="y")

        # ---- Derecha: gráfica ----
        right_frame = tk.Frame(resultados_frame, bg="#ffffff", bd=2, relief="raised")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        tk.Label(
            right_frame,
            text="📈 Representación gráfica:",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=5)

        self.canvas_frame = tk.Frame(right_frame, bg="#ffffff")
        self.canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # ---- Info teórica abajo ----
        info_frame = tk.Frame(main_frame, bg="#e8f4f8", bd=1, relief="solid")
        info_frame.pack(fill="x", padx=5, pady=(5, 0))

        info_text = (
            "ℹ️ Principio Fundamental de Conteo:\n"
            "Si un experimento se realiza en k etapas, donde:\n"
            "  - La etapa 1 tiene n₁ posibles resultados\n"
            "  - La etapa 2 tiene n₂ posibles resultados\n"
            "  - ...\n"
            "  - La etapa k tiene nₖ posibles resultados\n"
            "y cada combinación de elecciones es posible, entonces el número total de resultados es:\n"
            "  Total = n₁ × n₂ × ... × nₖ"
        )

        tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#e8f4f8",
            fg="#34495e",
            justify="left"
        ).pack(padx=10, pady=8)

    def crear_campos_eventos(self):
        # Eliminar campos anteriores
        for widget in self.eventos_frame.winfo_children():
            widget.destroy()
        self.campos_eventos.clear()

        tk.Label(
            self.eventos_frame,
            text="Ingresa el número de opciones para cada evento (etapa):",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(anchor="w", padx=10, pady=(8, 5))

        try:
            num_eventos = int(self.spin_eventos.get())
        except ValueError:
            num_eventos = 2
            self.spin_eventos.delete(0, tk.END)
            self.spin_eventos.insert(0, "2")

        # Crear filas para cada evento
        for i in range(1, num_eventos + 1):
            fila = tk.Frame(self.eventos_frame, bg="#ffffff")
            fila.pack(fill="x", padx=15, pady=2)

            tk.Label(
                fila,
                text=f"Evento {i}:",
                font=("Arial", 10),
                bg="#ffffff",
                width=10,
                anchor="w"
            ).pack(side="left")

            entry_desc = tk.Entry(fila, font=("Arial", 10), width=30)
            entry_desc.insert(0, f"Descripción del evento {i}")
            entry_desc.pack(side="left", padx=5)

            tk.Label(
                fila,
                text="Opciones:",
                font=("Arial", 10),
                bg="#ffffff"
            ).pack(side="left", padx=(10, 2))

            entry_opc = tk.Entry(fila, font=("Arial", 10), width=8)
            entry_opc.insert(0, "2")
            entry_opc.pack(side="left", padx=2)

            self.campos_eventos.append((entry_desc, entry_opc))

    def calcular_total(self):
        opciones = []
        descripciones = []

        # Leer valores
        for i, (entry_desc, entry_opc) in enumerate(self.campos_eventos, start=1):
            desc = entry_desc.get().strip()
            if not desc:
                desc = f"Evento {i}"
            try:
                n = int(entry_opc.get())
                if n <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"El número de opciones del evento {i} debe ser un entero positivo."
                )
                return

            descripciones.append(desc)
            opciones.append(n)

        # Calcular total (producto)
        total = 1
        for n in opciones:
            total *= n

        # Actualizar texto total
        self.label_total.config(
            text=f"Total de resultados posibles: {total:,}".replace(",", " ")
        )

        # Texto proceso
        self.text_proceso.delete("1.0", tk.END)
        proceso = "Total = "
        proceso += " × ".join(str(n) for n in opciones)
        proceso += f"\n\nCálculo:\n"

        parcial = 1
        for i, n in enumerate(opciones, start=1):
            parcial *= n
            proceso += f"Después del evento {i}: {parcial:,}".replace(",", " ") + "\n"

        explicacion = (
            "\nInterpretación:\n"
            "Cada combinación posible se obtiene eligiendo una opción de cada evento.\n"
            "El total corresponde al número de combinaciones distintas que pueden formarse."
        )

        self.text_proceso.insert(tk.END, proceso + explicacion)

        # Llenar tabla
        self.tree.delete(*self.tree.get_children())
        for i, (desc, n) in enumerate(zip(descripciones, opciones), start=1):
            self.tree.insert(
                "",
                "end",
                values=(f"Evento {i}", desc, n)
            )

        # Crear gráfica
        self.crear_grafica(opciones)

    def crear_grafica(self, opciones):
        # Limpiar gráfica anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor("#ffffff")

        x = np.arange(1, len(opciones) + 1)
        ax.bar(x, opciones, color="#3498db", alpha=0.8, edgecolor="#1f618d")

        ax.set_xticks(x)
        ax.set_xticklabels([f"E{i}" for i in x])
        ax.set_xlabel("Eventos (Etapas)", fontsize=10, fontweight="bold")
        ax.set_ylabel("Número de opciones", fontsize=10, fontweight="bold")
        ax.set_title("Opciones por evento", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
        ax.set_facecolor("#f8f9fa")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        # Reiniciar entradas de eventos
        self.crear_campos_eventos()

        # Limpiar resultados
        self.label_total.config(text="Total de resultados posibles: -")
        self.text_proceso.delete("1.0", tk.END)
        self.tree.delete(*self.tree.get_children())

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PrincipioConteoApp(root)
    root.mainloop()