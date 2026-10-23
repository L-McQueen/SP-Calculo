# -*- coding: utf-8 -*-
"""
Grafica de Puntos Evaluados de Temperatura vs Consumo Energetico
Muestra cuanto difiere cada punto evaluado respecto al minimo de confort (22 °C, 0.40 kW)
y la variacion del consumo en San Luis Potosi.
"""

import numpy as np
import matplotlib.pyplot as plt

# Configuracion de estilo
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#cccccc'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.6

# Modelo matematico base
def potencia(T):
    return 0.010 * (T - 22.0)**2 + 0.40

# Puntos clave evaluados: Mensuales historicos y extremos de diseno (San Luis Potosi)
puntos = [
    {'label': 'Minimo Invierno', 'T': 4.0, 'tipo': 'extremo', 'color': '#0d47a1'},
    {'label': 'Ene (16.5°C)', 'T': 16.5, 'tipo': 'mes', 'color': '#1976d2'},
    {'label': 'Dic (17.3°C)', 'T': 17.3, 'tipo': 'mes', 'color': '#1e88e5'},
    {'label': 'Feb (18.4°C)', 'T': 18.4, 'tipo': 'mes', 'color': '#42a5f5'},
    {'label': 'Nov (19.4°C)', 'T': 19.4, 'tipo': 'mes', 'color': '#64b5f6'},
    {'label': 'Mar (21.1°C)', 'T': 21.1, 'tipo': 'mes', 'color': '#81c784'},
    {'label': 'Oct / Confort (22.0°C)', 'T': 22.0, 'tipo': 'base', 'color': '#2e7d32'},
    {'label': 'Abr (23.8°C)', 'T': 23.8, 'tipo': 'mes', 'color': '#ffb74d'},
    {'label': 'Jul (24.8°C)', 'T': 24.8, 'tipo': 'mes', 'color': '#ffa726'},
    {'label': 'Ago (25.1°C)', 'T': 25.1, 'tipo': 'mes', 'color': '#ff9800'},
    {'label': 'May/Jun (25.8°C)', 'T': 25.8, 'tipo': 'mes', 'color': '#fb8c00'},
    {'label': 'Maximo Verano', 'T': 34.0, 'tipo': 'extremo', 'color': '#b71c1c'}
]

T_curve = np.linspace(0.0, 36.0, 500)
P_curve = potencia(T_curve)

# Crear figura con 2 subplots:
# Superior: Curva P(T) con los puntos evaluados y lineas de diferencia
# Inferior: Grafico de barras con la diferencia Delta P = P(T) - P_base
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 10), gridspec_kw={'height_ratios': [1.2, 0.8]})

# --- SUBPLOT 1: Curva P(T) con Puntos ---
ax1.plot(T_curve, P_curve, color='#37474f', linewidth=2.5, label='Modelo P(T) = 0.010*(T - 22)^2 + 0.40')
ax1.axhline(0.40, color='#2e7d32', linestyle=':', linewidth=1.5, label='Potencia Basal Minima (0.40 kW a 22 °C)')
ax1.axvline(22.0, color='#2e7d32', linestyle=':', linewidth=1.2)

# Sombreados de régimen
ax1.axvspan(0, 22, color='#e3f2fd', alpha=0.35, label='Zona de Calefaccion (T < 22 °C)')
ax1.axvspan(22, 36, color='#ffebee', alpha=0.35, label='Zona de Refrigeracion (T > 22 °C)')

# Dibujar puntos y diferencias
for p in puntos:
    T_val = p['T']
    P_val = potencia(T_val)
    delta_P = P_val - 0.40
    
    # Marcador
    marker_size = 90 if p['tipo'] != 'base' else 140
    ax1.scatter([T_val], [P_val], color=p['color'], s=marker_size, zorder=6, edgecolors='black', linewidth=0.8)
    
    # Linea vertical de diferencia respecto a la base (0.40 kW)
    if delta_P > 0.02:
        ax1.plot([T_val, T_val], [0.40, P_val], color=p['color'], linestyle='--', linewidth=1.2, alpha=0.7)
    
    # Texto con valor
    offset_y = 0.12 if T_val not in [16.5, 18.4, 24.8] else -0.22
    if p['tipo'] == 'extremo':
        ax1.annotate(f"{p['label']}\nT={T_val}°C\nP={P_val:.2f} kW\n(+{delta_P:.2f} kW)",
                     xy=(T_val, P_val), xytext=(T_val + (-4.5 if T_val < 20 else 1.2), P_val - 0.2),
                     fontsize=8.5, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=p['color'], alpha=0.9))
    elif p['tipo'] == 'base':
        ax1.annotate(f"Minimo Base\nT=22°C, P=0.40 kW\n(Delta = 0 kW)",
                     xy=(T_val, P_val), xytext=(T_val - 3.5, P_val + 0.35),
                     fontsize=9, fontweight='bold', color='#1b5e20',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2e7d32'),
                     arrowprops=dict(arrowstyle='->', color='#2e7d32', lw=1.2))

ax1.set_title('Evaluacion de Puntos en la Curva de Consumo Energetico P(T) - San Luis Potosi', fontsize=12, fontweight='bold')
ax1.set_ylabel('Potencia Demandada P (kW)', fontsize=11, fontweight='bold')
ax1.set_xlim(-1, 37)
ax1.set_ylim(0.2, 4.0)
ax1.grid(True)
ax1.legend(loc='upper center', fontsize=9, framealpha=0.95, ncol=2)

# --- SUBPLOT 2: Grafico de Barras de Diferencia Delta P ---
nombres_barras = [p['label'] for p in puntos]
deltas_barras = [potencia(p['T']) - 0.40 for p in puntos]
colores_barras = [p['color'] for p in puntos]

x_pos = np.arange(len(nombres_barras))
bars = ax2.bar(x_pos, deltas_barras, color=colores_barras, edgecolor='#333333', linewidth=0.8, alpha=0.9)

ax2.set_title('¿Cuanto difiere cada punto respecto al consumo base? (Delta P = P(T) - 0.40 kW)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Incremento de Potencia Delta P (kW)', fontsize=10, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(nombres_barras, rotation=35, ha='right', fontsize=8.5, fontweight='bold')
ax2.grid(axis='y')

# Etiquetas sobre las barras
for bar in bars:
    h = bar.get_height()
    if h > 0.005:
        ax2.annotate(f'+{h:.2f} kW',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, fontweight='bold')
    else:
        ax2.annotate('0.00 (Base)',
                     xy=(bar.get_x() + bar.get_width() / 2, 0),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=8, color='#2e7d32', fontweight='bold')

plt.tight_layout()
plt.savefig('grafica_5_puntos_evaluados.png', dpi=300)
plt.close()

# Imprimir tabla detallada en consola
print(f"{'Punto / Mes':<25} | {'Temp T (°C)':<11} | {'Potencia P (kW)':<15} | {'Difiere de Base (Delta P)':<25} | {'Incremento (%)':<15}")
print("-" * 100)
for p in puntos:
    T_val = p['T']
    P_val = potencia(T_val)
    delta = P_val - 0.40
    pct = (delta / 0.40) * 100.0
    print(f"{p['label']:<25} | {T_val:>8.1f} °C | {P_val:>12.3f} kW | {f'+{delta:.3f} kW':>22} | {f'+{pct:.1f} %':>12}")

