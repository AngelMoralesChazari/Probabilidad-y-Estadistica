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

        # Intentar maximizar la ventana (no falla si no está disponible)
        try:
            self.raiz.state('zoomed')
        except Exception:
            pass

        # Fuentes
        self.fuente_grande = ('Arial', 12)
        self.fuente_mediana = ('Arial', 10)
        self.fuente_titulo = ('Arial', 14, 'bold')
        self.fuente_botones = ('Arial', 10)

        # Valores por defecto solicitados: μ=0, σ=1, límites -1 y 1
        self.media = tk.DoubleVar(value=0.0)
        self.desviacion = tk.DoubleVar(value=1.0)
        self.probabilidad = tk.DoubleVar(value=0.95)
        self.limite_inferior = tk.DoubleVar(value=-1.0)
        self.limite_superior = tk.DoubleVar(value=1.0)

        # Variables para intervalo entre z1 y z2 (opcional)
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
            from_=-50,
            to=50,
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
            to=50,
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

        # Fila 1: rango (límite inferior / superior)
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

        # Fila 2: probabilidad acumulada P(X ≤ x) y P(X ≥ x)
        frame_acumulada = ttk.Frame(marco_probabilidad)
        frame_acumulada.pack(fill=tk.X, pady=10)

        ttk.Label(frame_acumulada, text="Valor X (para P(X ≤ x) o P(X ≥ x)):").pack(side=tk.LEFT, padx=(0, 10))
        self.valor_z = ttk.Entry(frame_acumulada, width=12, font=self.fuente_mediana)
        self.valor_z.pack(side=tk.LEFT, padx=(0, 30))

        ttk.Button(
            frame_acumulada,
            text="PROBABILIDAD ACUMULADA (P(X ≤ x))",
            command=self.calcular_probabilidad_acumulada
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            frame_acumulada,
            text="PROBABILIDAD COLA DERECHA (P(X ≥ x))",
            command=self.calcular_probabilidad_mayor
        ).pack(side=tk.LEFT, padx=(5, 10))

        # Fila 3: intervalo entre z1 y z2 (opcional)
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

        # Eventos
        self.configurar_eventos_entrada()

    # ---------- Helpers y eventos ----------
    def safe_get(self, var, default=None):
        """Leer de forma segura una tk.Variable o Entry vinculada.
           Devuelve default si el campo está vacío o no es numérico."""
        try:
            raw = var.get()
        except Exception:
            return default
        try:
            return float(raw)
        except (ValueError, TypeError):
            return default

    def configurar_eventos_entrada(self):
        entradas = [
            (self.entrada_media, self.media),
            (self.entrada_desviacion, self.desviacion),
            (self.entrada_lim_inf, self.limite_inferior),
            (self.entrada_lim_sup, self.limite_superior),
            (self.entrada_z1, self.z1),
            (self.entrada_z2, self.z2),
        ]
        for entrada, variable in entradas:
            entrada.bind('<KeyRelease>', lambda e, v=variable: self.actualizar_desde_entrada(v))

    def actualizar_desde_deslizador(self, event=None):
        self.actualizar_grafica()

    def actualizar_desde_entrada(self, variable):
        val = self.safe_get(variable, default=None)
        if val is None:
            return
        if hasattr(self, '_after_id'):
            try:
                self.raiz.after_cancel(self._after_id)
            except Exception:
                pass
        self._after_id = self.raiz.after(300, self.actualizar_grafica)

    # ---------- Gráfica ----------
    def actualizar_grafica(self):
        try:
            self.eje.clear()

            media = self.safe_get(self.media)
            desviacion = self.safe_get(self.desviacion)

            if media is None or desviacion is None or desviacion <= 0:
                self.eje.text(0.5, 0.5, "Introduzca μ y σ válidos", ha='center', transform=self.eje.transAxes)
                self.canvas.draw()
                return

            x = np.linspace(media - 4 * desviacion, media + 4 * desviacion, 1000)
            y = norm.pdf(x, loc=media, scale=desviacion)

            self.eje.plot(x, y, 'b-', linewidth=3, label=f'N(μ = {media:.2f}, σ = {desviacion:.2f})')

            limite_inf = self.safe_get(self.limite_inferior, default=None)
            limite_sup = self.safe_get(self.limite_superior, default=None)

            # Solo sombrear si límite inferior < límite superior
            if limite_inf is not None and limite_sup is not None and limite_inf < limite_sup:
                mascara = (x >= limite_inf) & (x <= limite_sup)
                if np.any(mascara):
                    self.eje.fill_between(x[mascara], y[mascara], alpha=0.4, color='red',
                                          label=f'Área: {limite_inf:.2f} a {limite_sup:.2f}')

                prob = norm.cdf(limite_sup, loc=media, scale=desviacion) - norm.cdf(limite_inf, loc=media, scale=desviacion)
                self.eje.text(0.02, 0.83, f'P = {prob:.4f}\n({prob*100:.2f}%)', transform=self.eje.transAxes,
                              fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.8))

            self.eje.set_xlabel('Valores', fontsize=10, fontweight='bold')
            self.eje.set_ylabel('Densidad de Probabilidad', fontsize=14, fontweight='bold')
            self.eje.set_title('DISTRIBUCIÓN NORMAL - CAMPANA DE GAUSS', fontsize=12, fontweight='bold', pad=20)

            self.eje.legend(fontsize=12, loc='upper right', framealpha=0.9)
            self.eje.grid(True, alpha=0.3, linestyle='--')
            self.eje.set_ylim(bottom=0)

            self.canvas.draw()

        except Exception as e:
            print(f"Error al actualizar gráfica: {e}")

    # ---------- Cálculos de probabilidad ----------
    def calcular_probabilidad_rango(self):
        media = self.safe_get(self.media)
        desviacion = self.safe_get(self.desviacion)
        limite_inf = self.safe_get(self.limite_inferior)
        limite_sup = self.safe_get(self.limite_superior)

        if None in (media, desviacion, limite_inf, limite_sup):
            messagebox.showerror("Error", "Por favor ingrese todos los valores numéricos.")
            return

        if desviacion <= 0:
            messagebox.showerror("Error", "La desviación estándar debe ser mayor que 0.")
            return

        if limite_inf >= limite_sup:
            messagebox.showerror("Error", "El límite inferior debe ser menor al límite superior.")
            return

        z1 = (limite_inf - media) / desviacion
        z2 = (limite_sup - media) / desviacion
        phi_z1 = norm.cdf(z1)
        phi_z2 = norm.cdf(z2)
        prob = phi_z2 - phi_z1

        texto = (
            f"PARÁMETROS:\n"
            f"  μ = {media:.4f}, σ = {desviacion:.4f}\n\n"
            f"INTERVALO: {limite_inf:.4f} ≤ X ≤ {limite_sup:.4f}\n\n"
            f"Estandarización:\n"
            f"  z1 = (a - μ)/σ = ({limite_inf:.4f} - {media:.4f}) / {desviacion:.4f} = {z1:.4f}\n"
            f"  z2 = (b - μ)/σ = ({limite_sup:.4f} - {media:.4f}) / {desviacion:.4f} = {z2:.4f}\n\n"
            f"Valores de la CDF estándar:\n"
            f"  Φ(z1) = Φ({z1:.4f}) = {phi_z1:.6f}\n"
            f"  Φ(z2) = Φ({z2:.4f}) = {phi_z2:.6f}\n\n"
            f"Probabilidad:\n"
            f"  P({limite_inf:.4f} ≤ X ≤ {limite_sup:.4f}) = Φ(z2) - Φ(z1) = {phi_z2:.6f} - {phi_z1:.6f} = {prob:.6f}\n"
            f"  → {prob*100:.4f}%"
        )

        messagebox.showinfo("Resultado (con estandarización)", texto)
        self.limite_inferior.set(limite_inf)
        self.limite_superior.set(limite_sup)
        self.actualizar_grafica()

    def calcular_probabilidad_acumulada(self):
        texto = self.valor_z.get().strip()
        if not texto:
            messagebox.showerror("Error", "Por favor ingrese un valor X")
            return
        try:
            x_val = float(texto)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido para X")
            return

        media = self.safe_get(self.media)
        desviacion = self.safe_get(self.desviacion)
        if None in (media, desviacion) or desviacion <= 0:
            messagebox.showerror("Error", "Ingrese μ y σ válidos")
            return

        z = (x_val - media) / desviacion
        phi = norm.cdf(z)
        texto_res = (
            f"Valor X = {x_val:.4f}\n"
            f"Estandarizado: z = (X - μ)/σ = ({x_val:.4f} - {media:.4f})/{desviacion:.4f} = {z:.4f}\n"
            f"Φ(z) = Φ({z:.4f}) = {phi:.6f}\n"
            f"P(X ≤ {x_val:.4f}) = {phi:.6f}  → {phi*100:.4f}%"
        )
        messagebox.showinfo("Probabilidad acumulada (con z)", texto_res)

        # Sombrear cola izquierda hasta X
        self.limite_inferior.set(media - 4 * desviacion)
        self.limite_superior.set(x_val)
        self.actualizar_grafica()

    def calcular_probabilidad_mayor(self):
        texto = self.valor_z.get().strip()
        if not texto:
            messagebox.showerror("Error", "Por favor ingrese un valor X")
            return
        try:
            x_val = float(texto)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido para X")
            return

        media = self.safe_get(self.media)
        desviacion = self.safe_get(self.desviacion)
        if None in (media, desviacion) or desviacion <= 0:
            messagebox.showerror("Error", "Ingrese μ y σ válidos")
            return

        z = (x_val - media) / desviacion
        phi = norm.cdf(z)
        prob = 1.0 - phi  # P(X >= x)

        texto_res = (
            f"Valor X = {x_val:.4f}\n"
            f"Estandarizado: z = (X - μ)/σ = ({x_val:.4f} - {media:.4f})/{desviacion:.4f} = {z:.4f}\n"
            f"Φ(z) = Φ({z:.4f}) = {phi:.6f}\n\n"
            f"P(X ≥ {x_val:.4f}) = 1 - Φ(z) = {prob:.6f}  → {prob*100:.4f}%"
        )
        messagebox.showinfo("Probabilidad cola derecha (con z)", texto_res)

        # Sombrear la cola derecha desde X hasta media+4σ
        self.limite_inferior.set(x_val)
        self.limite_superior.set(media + 4 * desviacion)
        self.actualizar_grafica()

    def calcular_probabilidad_entre_z(self):
        try:
            if not self.usar_intervalo_z.get():
                messagebox.showerror("Opción desactivada", "Marque la casilla 'Usar intervalo entre z₁ y z₂' para activar esta opción.")
                return

            z1_raw = self.entrada_z1.get().strip()
            z2_raw = self.entrada_z2.get().strip()
            if z1_raw == "" or z2_raw == "":
                messagebox.showerror("Error", "Ingrese valores para z₁ y z₂")
                return

            z1_val = float(z1_raw)
            z2_val = float(z2_raw)

            if z1_val >= z2_val:
                messagebox.showerror("Error", "Debe cumplirse z₁ < z₂.")
                return

            media = self.safe_get(self.media)
            desviacion = self.safe_get(self.desviacion)
            if None in (media, desviacion) or desviacion <= 0:
                messagebox.showerror("Error", "Ingrese μ y σ válidos")
                return

            prob = norm.cdf(z2_val, loc=media, scale=desviacion) - norm.cdf(z1_val, loc=media, scale=desviacion)

            texto = (
                f"INTERVALO: {z1_val:.4f} ≤ X ≤ {z2_val:.4f}\n\n"
                f"P = {prob:.6f} → {prob*100:.4f}%\n\n"
                f"(Si quieres que z₁,y z₂ sean z-estandarizados, dime y lo adapto.)"
            )
            messagebox.showinfo("Resultado", texto)

            self.limite_inferior.set(z1_val)
            self.limite_superior.set(z2_val)
            self.actualizar_grafica()

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos para z₁ y z₂")

    # ---------- Acciones rápidas ----------
    def establecer_estandar(self):
        self.media.set(0.0)
        self.desviacion.set(1.0)
        self.limite_inferior.set(-1.0)
        self.limite_superior.set(1.0)
        self.actualizar_grafica()
        messagebox.showinfo("Distribución Estándar", "Configurada distribución normal estándar: μ=0, σ=1")

    def area_una_desviacion(self):
        media = self.safe_get(self.media)
        desviacion = self.safe_get(self.desviacion)
        if media is None or desviacion is None:
            messagebox.showerror("Error", "Ingrese μ y σ válidos")
            return

        self.limite_inferior.set(media - desviacion)
        self.limite_superior.set(media + desviacion)
        self.actualizar_grafica()

        prob = norm.cdf(media + desviacion, media, desviacion) - norm.cdf(media - desviacion, media, desviacion)
        messagebox.showinfo("Regla Empírica", f"Área dentro de μ±σ: {prob:.6f}\nAproximadamente 68.27% de los datos\nLímites: [{media-desviacion:.2f}, {media+desviacion:.2f}]")

    def area_dos_desviaciones(self):
        media = self.safe_get(self.media)
        desviacion = self.safe_get(self.desviacion)
        if media is None or desviacion is None:
            messagebox.showerror("Error", "Ingrese μ y σ válidos")
            return

        self.limite_inferior.set(media - 2 * desviacion)
        self.limite_superior.set(media + 2 * desviacion)
        self.actualizar_grafica()

        prob = norm.cdf(media + 2 * desviacion, media, desviacion) - norm.cdf(media - 2 * desviacion, media, desviacion)
        messagebox.showinfo("Regla Empírica", f"Área dentro de μ±2σ: {prob:.6f}\nAproximadamente 95.45% de los datos\nLímites: [{media - 2 * desviacion:.2f}, {media + 2 * desviacion:.2f}]")

def main():
    raiz = tk.Tk()
    app = AplicacionDistribucionNormal(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()