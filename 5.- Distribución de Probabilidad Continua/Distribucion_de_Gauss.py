import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
from scipy.stats import norm


class AplicacionDistribucionNormal:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Distribución Normal - Campana de Gauss")

        # Pantalla completa
        self.raiz.state('zoomed')

        # Fuentes
        self.fuente_grande = ('Arial', 12)
        self.fuente_mediana = ('Arial', 10)
        self.fuente_titulo = ('Arial', 14, 'bold')
        self.fuente_botones = ('Arial', 10)

        # Variables para los parámetros
        self.media = tk.DoubleVar(value=0)
        self.desviacion = tk.DoubleVar(value=1)
        self.probabilidad = tk.DoubleVar(value=0.95)
        self.limite_inferior = tk.DoubleVar(value=-1)
        self.limite_superior = tk.DoubleVar(value=1)

        # NUEVAS variables para intervalo entre z1 y z2
        self.usar_intervalo_z = tk.BooleanVar(value=False)
        self.z1 = tk.DoubleVar(value=-1.0)
        self.z2 = tk.DoubleVar(value=1.0)

        self.crear_interfaz()
        self.actualizar_grafica()

        # Atajos de teclado
        self.raiz.bind('<Escape>', lambda e: self.raiz.state('normal'))
        self.raiz.bind('<F11>', lambda e: self.raiz.state('zoomed'))

    def crear_interfaz(self):
        estilo = ttk.Style()
        estilo.configure('TLabel', font=self.fuente_mediana)
        estilo.configure('TButton', font=self.fuente_botones)
        estilo.configure('TLabelframe', font=self.fuente_titulo)
        estilo.configure('TLabelframe.Label', font=self.fuente_titulo)
        estilo.configure('TEntry', font=self.fuente_mediana)

        # Marco principal
        marco_principal = ttk.Frame(self.raiz, padding="10")
        marco_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Marco de controles
        marco_controles = ttk.LabelFrame(
            marco_principal, text="PARÁMETROS DE LA DISTRIBUCIÓN", padding="10"
        )
        marco_controles.pack(fill=tk.X, pady=(0, 15))

        # MEDIA
        frame_media = ttk.Frame(marco_controles)
        frame_media.pack(fill=tk.X, pady=8)

        ttk.Label(frame_media, text="Media (μ):").pack(side=tk.LEFT, padx=(0, 15))
        self.deslizador_media = ttk.Scale(
            frame_media,
            from_=-5,
            to=5,
            variable=self.media,
            orient=tk.HORIZONTAL,
            command=self.actualizar_desde_deslizador,
            length=400
        )
        self.deslizador_media.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        self.entrada_media = ttk.Entry(
            frame_media, textvariable=self.media, width=12, font=self.fuente_mediana
        )
        self.entrada_media.pack(side=tk.LEFT, padx=(0, 10))

        # DESVIACIÓN ESTÁNDAR
        frame_desviacion = ttk.Frame(marco_controles)
        frame_desviacion.pack(fill=tk.X, pady=8)

        ttk.Label(frame_desviacion, text="Desviación Estándar (σ):").pack(side=tk.LEFT, padx=(0, 15))
        self.deslizador_desviacion = ttk.Scale(
            frame_desviacion,
            from_=0.1,
            to=3,
            variable=self.desviacion,
            orient=tk.HORIZONTAL,
            command=self.actualizar_desde_deslizador,
            length=400
        )
        self.deslizador_desviacion.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        self.entrada_desviacion = ttk.Entry(
            frame_desviacion, textvariable=self.desviacion, width=12, font=self.fuente_mediana
        )
        self.entrada_desviacion.pack(side=tk.LEFT, padx=(0, 10))

        # MARCO PROBABILIDADES
        marco_probabilidad = ttk.LabelFrame(
            marco_principal, text="CÁLCULOS DE PROBABILIDAD", padding="10"
        )
        marco_probabilidad.pack(fill=tk.X, pady=(0, 15))

        # Fila 1: rango (limite inferior / superior)
        frame_rango = ttk.Frame(marco_probabilidad)
        frame_rango.pack(fill=tk.X, pady=10)

        ttk.Label(frame_rango, text="Límite Inferior:").pack(side=tk.LEFT, padx=(0, 10))
        self.entrada_lim_inf = ttk.Entry(
            frame_rango, textvariable=self.limite_inferior, width=12, font=self.fuente_mediana
        )
        self.entrada_lim_inf.pack(side=tk.LEFT, padx=(0, 30))

        ttk.Label(frame_rango, text="Límite Superior:").pack(side=tk.LEFT, padx=(0, 10))
        self.entrada_lim_sup = ttk.Entry(
            frame_rango, textvariable=self.limite_superior, width=12, font=self.fuente_mediana
        )
        self.entrada_lim_sup.pack(side=tk.LEFT, padx=(0, 30))

        ttk.Button(
            frame_rango,
            text="CALCULAR PROBABILIDAD",
            command=self.calcular_probabilidad_rango
        ).pack(side=tk.LEFT, padx=(20, 0))

        # Fila 2: probabilidad acumulada P(X ≤ z)
        frame_acumulada = ttk.Frame(marco_probabilidad)
        frame_acumulada.pack(fill=tk.X, pady=10)

        ttk.Label(frame_acumulada, text="Valor a la izquierda de Z:").pack(side=tk.LEFT, padx=(0, 10))
        self.valor_z = ttk.Entry(frame_acumulada, width=12, font=self.fuente_mediana)
        self.valor_z.pack(side=tk.LEFT, padx=(0, 30))

        ttk.Button(
            frame_acumulada,
            text="PROBABILIDAD ACUMULADA (P(X ≤ z))",
            command=self.calcular_probabilidad_acumulada
        ).pack(side=tk.LEFT, padx=(0, 10))

        # Fila 3 (NUEVA): intervalo entre z1 y z2
        frame_intervalo = ttk.Frame(marco_probabilidad)
        frame_intervalo.pack(fill=tk.X, pady=10)

        self.chk_intervalo = ttk.Checkbutton(
            frame_intervalo,
            text="Usar intervalo entre z₁ y z₂",
            variable=self.usar_intervalo_z
        )
        self.chk_intervalo.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(frame_intervalo, text="z₁:").pack(side=tk.LEFT, padx=(0, 5))
        self.entrada_z1 = ttk.Entry(
            frame_intervalo, textvariable=self.z1, width=10, font=self.fuente_mediana
        )
        self.entrada_z1.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(frame_intervalo, text="z₂:").pack(side=tk.LEFT, padx=(0, 5))
        self.entrada_z2 = ttk.Entry(
            frame_intervalo, textvariable=self.z2, width=10, font=self.fuente_mediana
        )
        self.entrada_z2.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Button(
            frame_intervalo,
            text="PROBABILIDAD ENTRE z₁ Y z₂",
            command=self.calcular_probabilidad_entre_z
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Botones de acciones rápidas
        marco_acciones = ttk.Frame(marco_principal)
        marco_acciones.pack(fill=tk.X, pady=(0, 15))

        frame_botones_izq = ttk.Frame(marco_acciones)
        frame_botones_izq.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Button(
            frame_botones_izq,
            text="DISTRIBUCIÓN ESTÁNDAR (μ=0, σ=1)",
            command=self.establecer_estandar
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            frame_botones_izq,
            text="ÁREA 1 DESVIACIÓN ESTÁNDAR",
            command=self.area_una_desviacion
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            frame_botones_izq,
            text="ÁREA 2 DESVIACIONES ESTÁNDAR",
            command=self.area_dos_desviaciones
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            marco_acciones,
            text="SALIR (ESC)",
            command=self.raiz.destroy
        ).pack(side=tk.RIGHT)

        # Marco para la gráfica
        marco_grafica = ttk.Frame(marco_principal)
        marco_grafica.pack(fill=tk.BOTH, expand=True)

        # Configurar matplotlib
        plt.rcParams.update({
            'font.size': 12,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'legend.fontsize': 10,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'figure.titlesize': 14
        })

        # Crear figura y ejes
        self.figura = plt.Figure(figsize=(12, 6), dpi=100)
        self.eje = self.figura.add_subplot(111)
        self.figura.patch.set_facecolor('#f0f0f0')

        self.canvas = FigureCanvasTkAgg(self.figura, marco_grafica)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Actualización en tiempo real
        self.configurar_eventos_entrada()

    def configurar_eventos_entrada(self):
        """Eventos para las entradas de texto"""
        entradas = [
            (self.entrada_media, self.media),
            (self.entrada_desviacion, self.desviacion),
            (self.entrada_lim_inf, self.limite_inferior),
            (self.entrada_lim_sup, self.limite_superior),
        ]

        for entrada, variable in entradas:
            entrada.bind(
                '<KeyRelease>',
                lambda e, v=variable: self.actualizar_desde_entrada(v)
            )

    def actualizar_desde_deslizador(self, event=None):
        """Actualizar la gráfica cuando se mueven los deslizadores"""
        self.actualizar_grafica()

    def actualizar_desde_entrada(self, variable):
        """Actualizar la gráfica cuando se escriben valores"""
        try:
            float(variable.get())
            if hasattr(self, '_after_id'):
                self.raiz.after_cancel(self._after_id)
            self._after_id = self.raiz.after(500, self.actualizar_grafica)
        except ValueError:
            pass  # Ignorar mientras el valor no sea numérico completo

    def actualizar_grafica(self):
        """Actualizar la gráfica de la distribución normal"""
        try:
            self.eje.clear()

            media = self.media.get()
            desviacion = self.desviacion.get()

            # Generar puntos para la curva
            x = np.linspace(media - 4 * desviacion, media + 4 * desviacion, 1000)
            y = norm.pdf(x, media, desviacion)

            # Curva principal
            self.eje.plot(
                x, y, 'b-', linewidth=3,
                label=f'N(μ = {media:.2f}, σ = {desviacion:.2f})'
            )

            # Área entre límites actuales
            limite_inf = self.limite_inferior.get()
            limite_sup = self.limite_superior.get()

            if limite_inf < limite_sup:
                mascara = (x >= limite_inf) & (x <= limite_sup)
                self.eje.fill_between(
                    x[mascara], y[mascara],
                    alpha=0.4, color='red',
                    label=f'Área: {limite_inf:.2f} a {limite_sup:.2f}'
                )

                prob = norm.cdf(limite_sup, media, desviacion) - norm.cdf(
                    limite_inf, media, desviacion
                )
                self.eje.text(
                    0.02, 0.83,
                    f'P = {prob:.4f}\n({prob*100:.2f}%)',
                    transform=self.eje.transAxes,
                    fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.3",
                              facecolor="yellow", alpha=0.7)
                )

            # Etiquetas
            self.eje.set_xlabel('Valores', fontsize=10, fontweight='bold')
            self.eje.set_ylabel('Densidad de Probabilidad', fontsize=14, fontweight='bold')
            self.eje.set_title(
                'DISTRIBUCIÓN NORMAL - CAMPANA DE GAUSS',
                fontsize=12, fontweight='bold', pad=20
            )

            self.eje.legend(fontsize=12, loc='upper right', framealpha=0.9)
            self.eje.grid(True, alpha=0.3, linestyle='--')
            self.eje.set_ylim(bottom=0)

            self.canvas.draw()

        except Exception as e:
            print(f"Error al actualizar gráfica: {e}")

    def calcular_probabilidad_rango(self):
        """Calcular la probabilidad entre dos valores"""
        try:
            media = self.media.get()
            desviacion = self.desviacion.get()
            limite_inf = self.limite_inferior.get()
            limite_sup = self.limite_superior.get()

            if limite_inf >= limite_sup:
                messagebox.showerror(
                    "Error",
                    "El límite inferior debe ser menor al límite superior"
                )
                return

            prob = norm.cdf(limite_sup, media, desviacion) - norm.cdf(
                limite_inf, media, desviacion
            )

            messagebox.showinfo(
                "Resultado",
                f"P({limite_inf:.4f} ≤ X ≤ {limite_sup:.4f}) = {prob:.6f}\n"
                f"({prob*100:.4f}% del área total)"
            )

            self.actualizar_grafica()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese valores numéricos válidos"
            )

    def calcular_probabilidad_acumulada(self):
        """Calcular la probabilidad acumulada hasta un valor z"""
        try:
            texto = self.valor_z.get().strip()
            if not texto:
                messagebox.showerror("Error", "Por favor ingrese un valor z")
                return

            z = float(texto)
            media = self.media.get()
            desviacion = self.desviacion.get()

            prob = norm.cdf(z, media, desviacion)

            messagebox.showinfo(
                "Resultado",
                f"P(X ≤ {z:.4f}) = {prob:.6f}\n"
                f"({prob*100:.4f}% de los valores son ≤ {z:.4f})"
            )

            # Actualizar límites para mostrar esta área
            self.limite_inferior.set(media - 4 * desviacion)
            self.limite_superior.set(z)
            self.actualizar_grafica()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese un valor z numérico válido"
            )

    def calcular_probabilidad_entre_z(self):
        """Calcular P(z1 ≤ X ≤ z2) y sombrear esa área"""
        try:
            if not self.usar_intervalo_z.get():
                messagebox.showerror(
                    "Opción desactivada",
                    "Marque la casilla 'Usar intervalo entre z₁ y z₂' para activar esta opción."
                )
                return

            z1 = float(self.entrada_z1.get().strip())
            z2 = float(self.entrada_z2.get().strip())

            if z1 >= z2:
                messagebox.showerror(
                    "Error",
                    "Debe cumplirse z₁ < z₂."
                )
                return

            media = self.media.get()
            desviacion = self.desviacion.get()

            prob = norm.cdf(z2, media, desviacion) - norm.cdf(z1, media, desviacion)

            messagebox.showinfo(
                "Resultado",
                f"P({z1:.4f} ≤ X ≤ {z2:.4f}) = {prob:.6f}\n"
                f"({prob*100:.4f}% del área total)"
            )

            # Actualizar límites para mostrar esa área en rojo
            self.limite_inferior.set(z1)
            self.limite_superior.set(z2)
            self.actualizar_grafica()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Por favor ingrese valores numéricos válidos para z₁ y z₂"
            )

    def establecer_estandar(self):
        """Establecer la distribución normal estándar"""
        self.media.set(0)
        self.desviacion.set(1)
        self.limite_inferior.set(-1.96)
        self.limite_superior.set(1.96)
        self.actualizar_grafica()
        messagebox.showinfo(
            "Distribución Estándar",
            "Configurada distribución normal estándar: μ=0, σ=1"
        )

    def area_una_desviacion(self):
        """Mostrar el área dentro de una desviación estándar"""
        media = self.media.get()
        desviacion = self.desviacion.get()
        self.limite_inferior.set(media - desviacion)
        self.limite_superior.set(media + desviacion)
        self.actualizar_grafica()

        prob = norm.cdf(media + desviacion, media, desviacion) - norm.cdf(
            media - desviacion, media, desviacion
        )
        messagebox.showinfo(
            "Regla Empírica",
            f"Área dentro de μ±σ: {prob:.6f}\n"
            f"Aproximadamente 68.27% de los datos\n"
            f"Límites: [{media-desviacion:.2f}, {media+desviacion:.2f}]"
        )

    def area_dos_desviaciones(self):
        """Mostrar el área dentro de dos desviaciones estándar"""
        media = self.media.get()
        desviacion = self.desviacion.get()
        self.limite_inferior.set(media - 2 * desviacion)
        self.limite_superior.set(media + 2 * desviacion)
        self.actualizar_grafica()

        prob = norm.cdf(media + 2 * desviacion, media, desviacion) - norm.cdf(
            media - 2 * desviacion, media, desviacion
        )
        messagebox.showinfo(
            "Regla Empírica",
            f"Área dentro de μ±2σ: {prob:.6f}\n"
            f"Aproximadamente 95.45% de los datos\n"
            f"Límites: [{media - 2 * desviacion:.2f}, {media + 2 * desviacion:.2f}]"
        )


def main():
    raiz = tk.Tk()
    app = AplicacionDistribucionNormal(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()