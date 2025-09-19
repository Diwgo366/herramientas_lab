import os
import numpy as np
import json
import subprocess
import sys

def iniciar_documento_latex():
    return [
        r"\documentclass{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[spanish]{babel}",
        r"\usepackage{amsmath}",
        r"\usepackage{geometry}",
        r"\usepackage{caption}",
        r"\usepackage{float}",
        r"\usepackage{pgfplots}",
        r"\pgfplotsset{compat=1.18}",
        r"\geometry{left=2.54cm, top=2.54cm}",
        r"\setlength{\tabcolsep}{10pt}",
        r"\renewcommand{\arraystretch}{1.5}",
        r"\begin{document}",
        r"\begin{center}",
        r"\Large{\textbf{Tratamiento de Datos y Ajuste de Curvas}}",
        r"\end{center}"
    ]

def agregar_tabla_latex(datos, idx_x, idx_y, tipo_grafica=None):
    contenido = []
    contenido.append(r"\begin{figure}[H]")
    contenido.append(r"\centering")
    x_vals = np.array([fila+1 if idx_x == -1 else datos[fila, idx_x] for fila in range(datos.shape[0])])
    y_vals = datos[:, idx_y]
    if tipo_grafica and tipo_grafica.lower() == "exponencial":
        encabezado = r"$x_i$ & $y_i$ & $\log x_i$ & $\log y_i$ & $\log x_i \log y_i$ & $(\log x_i)^2$"
        contenido.append(r"\begin{tabular}{cccccc}")
        contenido.append(encabezado + r" \\ \hline")
        suma_x = suma_y = suma_logx = suma_logy = suma_logxlogy = suma_logx2 = 0
        for x, y in zip(x_vals, y_vals):
            logx = np.log10(x)
            logy = np.log10(y)
            logxlogy = logx * logy
            logx2 = logx ** 2
            suma_x += x
            suma_y += y
            suma_logx += logx
            suma_logy += logy
            suma_logxlogy += logxlogy
            suma_logx2 += logx2
            contenido.append(f"{x:.4f} & {y:.4f} & {logx:.10f} & {logy:.10f} & {logxlogy:.10f} & {logx2:.10f} \\\\")
        contenido.append(r"\hline")
        contenido.append(r"$\sum x_i$ & $\sum y_i$ & $\sum \log x_i$ & $\sum \log y_i$ & $\sum \log x_i \log y_i$ & $\sum (\log x_i)^2$ \\")
        contenido.append("%.4f & %.4f & %.10f & %.10f & %.10f & %.10f \\\\" % (
            suma_x, suma_y, suma_logx, suma_logy, suma_logxlogy, suma_logx2))
        contenido.append(r"\end{tabular}")
    else:
        encabezado = r"$x_i$ & $y_i$ & $x_i y_i$ & $x_i^2$"
        contenido.append(r"\begin{tabular}{cccc}")
        contenido.append(encabezado + r" \\ \hline")
        suma_x = suma_y = suma_xy = suma_x2 = 0
        for x, y in zip(x_vals, y_vals):
            xy = x * y
            x2 = x ** 2
            suma_x += x
            suma_y += y
            suma_xy += xy
            suma_x2 += x2
            contenido.append(f"{x:.4f} & {y:.4f} & {xy:.4f} & {x2:.4f} \\\\")
        contenido.append(r"\hline")
        contenido.append(r"$\sum x_i$ & $\sum y_i$ & $\sum x_i y_i$ & $\sum x_i^2$ \\")
        contenido.append("%.4f & %.4f & %.4f & %.4f \\\\" % (
            suma_x, suma_y, suma_xy, suma_x2))
        contenido.append(r"\end{tabular}")
    contenido.append(r"\vspace{0.5cm}")
    contenido.append(r"\end{figure}")
    return contenido

def agregar_grafica_latex(datos, idx_x, idx_ys, tipo_grafica, config, solo_grafica=False):
    contenido = []
    mostrar_leyenda = config.get("mostrar_leyenda", True)
    leyenda_str = (
        "legend style={at={(1.05,1)},anchor=north west,legend columns=1}" if mostrar_leyenda else "legend style={draw=none},legend entries={}"
    )
    nombre_xs = config.get("nombre_x", [])
    label_grafica = config.get("label_grafica", "")
    nombre_eje_x = config.get("nombre_eje_x", "")
    nombre_eje_y = config.get("nombre_eje_y", "")

    if not solo_grafica:
        contenido.append(r"\begin{figure}[H]")
        contenido.append(r"\centering")
    
    contenido.append(r"\begin{tikzpicture}")
    axis_options = (
        r"grid=both, grid style={%s!60!%s}, axis background/.style={fill=%s}, width=12cm, height=8cm," % (
            config.get("linea", "orange"),
            config.get("fondo", "white"),
            config.get("fondo", "white")
            ) +
        f"xlabel={{{nombre_eje_x}}}," +
        f"ylabel={{{nombre_eje_y}}}," + (f"title={{{label_grafica}}}," if solo_grafica else "") +
        f"{leyenda_str}"
    )
    contenido.append(r"\begin{axis}[" + axis_options + "]")
    colores = config.get("colores_x", ["red", "blue", "green", "orange", "purple"])
    for i, idx_y in enumerate(idx_ys):
        color = colores[i % len(colores)]
        nombre_y = nombre_xs[i] if i < len(nombre_xs) and nombre_xs[i] else f"Y{i+1}"
        x = np.arange(1, datos.shape[0]+1) if idx_x == -1 else datos[:, idx_x]
        y = datos[:, idx_y]
        contenido.append(r"\addplot+[only marks, mark=*, mark options={{fill=%s,draw=%s}}] coordinates {" % (color, color))
        for par in np.column_stack((x, y)):
            contenido.append(f"({par[0]},{par[1]})")
        contenido.append("};")
        if mostrar_leyenda:
            contenido.append(r"\addlegendentry{%s}" % (nombre_y))
        if tipo_grafica.lower() == "lineal":
            p = len(x)
            suma_x = np.sum(x)
            suma_y = np.sum(y)
            suma_xy = np.sum(x * y)
            suma_x2 = np.sum(x ** 2)
            denominador = (p * suma_x2 - suma_x ** 2.0)
            if denominador != 0 and config.get("mostrar_ajuste", True):
                m = (p * suma_xy - suma_x * suma_y) / denominador
                b = (suma_x2 * suma_y - suma_x * suma_xy) / denominador
                contenido.append(
                    r"\addplot[smooth, color=%s, thick, %s, domain=%.4f:%.4f] {%.6f*x + %.6f};" % (
                        config.get("color_ajuste", "black"),
                        config.get("tipo_linea", ""),
                        np.min(x), np.max(x),
                        m, b
                    )
                )
                if mostrar_leyenda:
                    contenido.append(r"\addlegendentry{$y=%.4fx + %.4f$}" % (m, b))
        elif tipo_grafica.lower() == "exponencial":
            p = len(x)
            log_x = np.log10(x)
            log_y = np.log10(y)
            suma_log_x = np.sum(log_x)
            suma_log_y = np.sum(log_y)
            suma_log_x_log_y = np.sum(log_x * log_y)
            suma_log_x2 = np.sum(log_x ** 2)
            denominador = (p * suma_log_x2 - suma_log_x ** 2.0)
            if denominador != 0 and config.get("mostrar_ajuste", True):
                m = (p * suma_log_x_log_y - suma_log_x * suma_log_y) / denominador
                b = (suma_log_x2 * suma_log_y - suma_log_x * suma_log_x_log_y) / denominador
                contenido.append(
                    r"\addplot[smooth, color=%s, thick, %s, domain=%.4f:%.4f] {10^(%.6f) * x^(%.6f)};" % (
                        config.get("color_ajuste", "black"),
                        config.get("tipo_linea", ""),
                        np.min(x), np.max(x),
                        b, m
                    )
                )
                if mostrar_leyenda:
                    contenido.append(r"\addlegendentry{$y=10^{%.4f}x^{%.4f}$}" % (b, m))
    contenido.append(r"\end{axis}")
    contenido.append(r"\end{tikzpicture}")
    if not solo_grafica:
        if label_grafica:
            contenido.append(r"\caption{%s}" % label_grafica)
        contenido.append(r"\label{fig:}")
        contenido.append(r"\end{figure}")
    return contenido

def agregar_formulas_latex(datos, idx_x, idx_y, tipo_grafica):
    contenido = []
    contenido.append(r"\section*{Ecuaciones}")
    if idx_x == -1:
        x = np.arange(1, datos.shape[0]+1)
    else:
        x = datos[:, idx_x]
    y = datos[:, idx_y]
    if tipo_grafica.lower() == "lineal":
        p = len(x)
        suma_x = np.sum(x)
        suma_y = np.sum(y)
        suma_xy = np.sum(x * y)
        suma_x2 = np.sum(x ** 2)
        denominador = (p * suma_x2 - suma_x ** 2.0)
        if denominador != 0:
            m = (p * suma_xy - suma_x * suma_y) / denominador
            b = (suma_x2 * suma_y - suma_x * suma_xy) / denominador
            contenido.append(r"\begin{center}")
            contenido.append(r"\textbf{Ecuación general:} \\[0.2cm]")
            contenido.append(r"\fbox{$y = m x + b$}")
            contenido.append(r"\end{center}")
            contenido.append(r"\begin{center}")
            contenido.append(r"\begin{tabular}{p{0.48\textwidth} p{0.48\textwidth}}")
            m_col = [
                r"\textbf{Desarrollo de $m$}",
                r"\begin{equation*}",
                r"m = \frac{p \sum x_i y_i - \sum x_i \sum y_i}{p \sum x_i^2 - (\sum x_i)^2}",
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"m = \frac{%d \cdot %.4f - %.4f \cdot %.4f}{%d \cdot %.4f - (%.4f)^2}" % (
                    p, suma_xy, suma_x, suma_y, p, suma_x2, suma_x
                ),
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"m = \frac{%.4f}{%.4f} = %.4f" % (
                    (p * suma_xy - suma_x * suma_y),
                    denominador,
                    m
                ),
                r"\end{equation*}",
            ]
            b_col = [
                r"\textbf{Desarrollo de $b$}",
                r"\begin{equation*}",
                r"b = \frac{\sum x_i^2 \sum y_i - \sum x_i \sum x_i y_i}{p \sum x_i^2 - (\sum x_i)^2}",
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"b = \frac{%.4f \cdot %.4f - %.4f \cdot %.4f}{%d \cdot %.4f - (%.4f)^2}" % (
                    suma_x2, suma_y, suma_x, suma_xy, p, suma_x2, suma_x
                ),
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"b = \frac{%.4f}{%.4f} = %.4f" % (
                    (suma_x2 * suma_y - suma_x * suma_xy),
                    denominador,
                    b
                ),
                r"\end{equation*}",
            ]
            contenido.append(" ".join(m_col) + " & " + " ".join(b_col) + r" \\")
            contenido.append(r"\end{tabular}")
            contenido.append(r"\end{center}")
            contenido.append(r"\begin{center}")
            if b < 0:
                contenido.append(r"\fbox{$y = %.4fx %.4f$}" % (m, b))
            else:
                contenido.append(r"\fbox{$y = %.4fx + %.4f$}" % (m, b))
            contenido.append(r"\end{center}")
    elif tipo_grafica.lower() == "exponencial":
        p = len(x)
        log_x = np.log10(x)
        log_y = np.log10(y)
        suma_log_x = np.sum(log_x)
        suma_log_y = np.sum(log_y)
        suma_log_x_log_y = np.sum(log_x * log_y)
        suma_log_x2 = np.sum(log_x ** 2)
        denominador = (p * suma_log_x2 - suma_log_x ** 2.0)
        if denominador != 0:
            m = (p * suma_log_x_log_y - suma_log_x * suma_log_y) / denominador
            b = (suma_log_x2 * suma_log_y - suma_log_x * suma_log_x_log_y) / denominador
            contenido.append(r"\begin{center}")
            contenido.append(r"\textbf{Ecuación general:} \\[0.2cm]")
            contenido.append(r"\fbox{$y = 10^{b} x^{m}$}")
            contenido.append(r"\end{center}")
            contenido.append(r"\begin{center}")
            contenido.append(r"\begin{tabular}{p{0.48\textwidth} p{0.48\textwidth}}")
            # Columna m
            m_col = [
                r"\textbf{Desarrollo de $m$}",
                r"\begin{equation*}",
                r"m = \frac{p \sum \log{x_i} \log{y_i} - \sum \log{x_i} \sum \log{y_i}}{p \sum \log{x_i}^2 - (\sum \log{x_i})^2}",
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"m = \frac{%d \cdot %.4f - %.4f \cdot %.4f}{%d \cdot %.4f - (%.4f)^2}" % (
                    p, suma_log_x_log_y, suma_log_x, suma_log_y, p, suma_log_x2, suma_log_x
                ),
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"m = \frac{%.4f}{%.4f} = %.4f" % (
                    (p * suma_log_x_log_y - suma_log_x * suma_log_y),
                    (p * suma_log_x2 - suma_log_x ** 2.0),
                    m
                ),
                r"\end{equation*}",
            ]
            # Columna b
            b_col = [
                r"\textbf{Desarrollo de $b$}",
                r"\begin{equation*}",
                r"b = \frac{\sum \log{x_i}^2 \sum \log{y_i} - \sum \log{x_i} \sum \log{x_i} \log{y_i}}{p \sum \log{x_i}^2 - (\sum \log{x_i})^2}",
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"b = \frac{%.4f \cdot %.4f - %.4f \cdot %.4f}{%d \cdot %.4f - (%.4f)^2}" % (
                    suma_log_x2, suma_log_y, suma_log_x, suma_log_x_log_y, p, suma_log_x2, suma_log_x
                ),
                r"\end{equation*}",
                r"\vspace{0.3cm}",
                r"\begin{equation*}",
                r"b = \frac{%.4f}{%.4f} = %.4f" % (
                    (suma_log_x2 * suma_log_y - suma_log_x * suma_log_x_log_y),
                    denominador,
                    b
                ),
                r"\end{equation*}",
            ]
            contenido.append(" ".join(b_col) + " & " + " ".join(m_col) + r" \\")
            contenido.append(r"\end{tabular}")
            contenido.append(r"\end{center}")
            # Ecuación resultante centrada
            contenido.append(r"\begin{center}")
            contenido.append(r"\fbox{$y = 10^{%.4f} x^{%.4f}$}" % (b, m))
            contenido.append(r"\end{center}")
    return contenido

def finalizar_documento_latex():
    return [r"\end{document}"]

def crear_archivo_tek(tipo_grafica, eje_x, ejes_y, base_dir, compilar):
    carpeta = os.path.join(base_dir, "temporales")
    resultados_dir = os.path.join(base_dir, "resultados")
    datos_path = os.path.join(carpeta, "datos.dat")
    config_path = os.path.join(carpeta, "configuracion_grafica.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    datos = np.loadtxt(datos_path, delimiter="\t")
    idx_x = -1 if eje_x == "X0" else int(eje_x[1:]) - 1
    idx_ys = [int(y[1:]) - 1 for y in ejes_y]
    nombre_xs = config.get("nombre_x", [])
    contenido = iniciar_documento_latex()
    for i, idx_y in enumerate(idx_ys):
        nombre_y = nombre_xs[i] if i < len(nombre_xs) and nombre_xs[i] else f"Y{i+1}"
        if tipo_grafica.lower() == "lineal":
            contenido.append(r"\section*{Ajuste Lineal para %s}" % nombre_y)
        elif tipo_grafica.lower() == "exponencial":
            contenido.append(r"\section*{Ajuste Exponencial para %s}" % nombre_y)
        contenido += agregar_tabla_latex(datos, idx_x, idx_y, tipo_grafica)
        contenido += agregar_formulas_latex(datos, idx_x, idx_y, tipo_grafica)
    contenido += agregar_grafica_latex(datos, idx_x, idx_ys, tipo_grafica, config, False)
    contenido += finalizar_documento_latex()
    os.makedirs(carpeta, exist_ok=True)
    ruta_tex = os.path.join(carpeta, "analisis.tex")
    with open(ruta_tex, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))
    if compilar:
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "analisis.tex"],
                cwd=carpeta,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            pdf_path = os.path.join(carpeta, "analisis.pdf")
            os.makedirs(resultados_dir, exist_ok=True)
            pdf_destino = os.path.join(resultados_dir, "analisis.pdf")
            try:
                if os.path.exists(pdf_destino):
                    os.remove(pdf_destino)
                os.replace(pdf_path, pdf_destino)
            except Exception as e:
                print("No se pudo mover el PDF a la carpeta Resultados:", e)
                pdf_destino = pdf_path
            # Abrir el PDF automáticamente
            try:
                if sys.platform.startswith("win"):
                    os.startfile(pdf_destino)
                elif sys.platform.startswith("darwin"):
                    subprocess.run(["open", pdf_destino])
                else:
                    subprocess.run(["xdg-open", pdf_destino])
            except Exception:
                pass
            # Limpiar archivos auxiliares
            for ext in [".aux", ".log", ".out", ".toc"]:
                aux_file = os.path.join(carpeta, f"analisis{ext}")
                if os.path.exists(aux_file):
                    try:
                        os.remove(aux_file)
                    except Exception:
                        pass
            return pdf_destino
        except Exception as e:
            print("Error al compilar o abrir el PDF:", e)
            return ruta_tex
    else:
        ruta_txt = os.path.join(resultados_dir, "analisis.txt")
        os.makedirs(resultados_dir, exist_ok=True)
        with open(ruta_txt, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))
        try:
            if sys.platform.startswith("win"):
                os.startfile(ruta_txt)
            elif sys.platform.startswith("darwin"):
                subprocess.run(["open", ruta_txt])
            else:
                subprocess.run(["xdg-open", ruta_txt])
        except Exception as e:
            print("No se pudo abrir el archivo TXT:", e)
        return ruta_txt