# -*- coding: utf-8 -*-
"""
Simulacion y Analisis Matematico de Consumo Energetico en Vivienda Inteligente
Ubicacion: San Luis Potosi, S.L.P.
Entregables 1 y 2 - Calculo Diferencial e Integral
"""

import numpy as np
import matplotlib.pyplot as plt

# Configuracion de estilo para graficos tecnicos
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#cccccc'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.6

# -------------------------------------------------------------
# 1. PARAMETROS BASE DEL MODELO Y VIVIENDA
# -------------------------------------------------------------
T_CONFORT_BASE = 22.0  # Grados Celsius
P_BASE = 0.40          # kW (Potencia basal continua)
A_COEFF = 0.010        # kW/(°C^2) (Coeficiente de demanda termica)

# Definicion de funciones matematicas del modelo
def potencia(T, t_confort=T_CONFORT_BASE, a=A_COEFF, p_base=P_BASE):
    """Modelo cuadratico de consumo de potencia P(T) en kW."""
    return a * (T - t_confort)**2 + p_base

def derivada_potencia(T, t_confort=T_CONFORT_BASE, a=A_COEFF):
    """Razon de cambio de la potencia respecto a la temperatura dP/dT en kW/°C."""
    return 2.0 * a * (T - t_confort)

def segunda_derivada(a=A_COEFF):
    """Segunda derivada d^2P/dT^2 en kW/(°C^2)."""
    return 2.0 * a

# -------------------------------------------------------------
# 2. ESCENARIOS CLIMATICOS DIARIOS (San Luis Potosi)
# -------------------------------------------------------------
escenarios = {
    'Frio': {
        'nombre': 'Dia Frio (Invierno - Enero)',
        'T_min': 4.0,
        'T_max': 20.0,
        'T_media': 12.0,
        'Amplitud': 8.0,
        'color': '#1f77b4',
        'T_confort_opt': 20.0  # Ajuste de termostato para ahorro
    },
    'Templado': {
        'nombre': 'Dia Templado (Transicion - Marzo/Oct)',
        'T_min': 12.0,
        'T_max': 26.0,
        'T_media': 19.0,
        'Amplitud': 7.0,
        'color': '#2ca02c',
        'T_confort_opt': 22.0  # Mantener zona neutra
    },
    'Calido': {
        'nombre': 'Dia Calido (Verano - Mayo/Junio)',
        'T_min': 16.0,
        'T_max': 34.0,
        'T_media': 25.0,
        'Amplitud': 9.0,
        'color': '#d62728',
        'T_confort_opt': 24.0  # Ajuste de termostato para ahorro
    }
}

def temperatura_temporal(t, T_media, Amplitud):
    """
    Perfil horario de temperatura en 24 horas.
    Minimo a las t = 6:00 h, maximo a las t = 18:00 h.
    """
    return T_media - Amplitud * np.cos(np.pi * (t - 6.0) / 12.0)

def energia_analitica(T_media, Amplitud, t_confort=T_CONFORT_BASE, a=A_COEFF, p_base=P_BASE):
    """
    Calculo analitico exacto de la integral definida de 0 a 24 horas:
    E = 24 * [ P_base + a * ( (T_media - T_confort)^2 + 0.5 * Amplitud^2 ) ]
    """
    delta_t = T_media - t_confort
    p_promedio = p_base + a * (delta_t**2 + 0.5 * Amplitud**2)
    return 24.0 * p_promedio

def energia_numerica(t_vals, p_vals):
    """Integracion numerica por regla compuesta del trapecio."""
    if hasattr(np, 'trapezoid'):
        return np.trapezoid(p_vals, t_vals)
    return np.trapz(p_vals, t_vals)

# -------------------------------------------------------------
# 3. GENERACION DE GRAFICAS TECNICAS
# -------------------------------------------------------------
print("--- EJECUTANDO CALCULOS Y GENERACION DE GRAFICAS ---")

# GRAFICA 1: Modelo Cuadratico P(T) y Derivada dP/dT
T_range = np.linspace(0.0, 38.0, 400)
P_range = potencia(T_range)
dP_range = derivada_potencia(T_range)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

# Curva P(T)
ax1.plot(T_range, P_range, color='#0d47a1', linewidth=2.5, label='P(T) = 0.010*(T - 22)^2 + 0.40')
ax1.axvline(22.0, color='#b71c1c', linestyle=':', linewidth=1.5, label='Punto critico (T = 22 °C, P = 0.40 kW)')
ax1.scatter([22.0], [0.40], color='#b71c1c', s=70, zorder=5)
ax1.axvspan(0, 22, color='#e3f2fd', alpha=0.4, label='Zona de Calefaccion (dP/dT < 0)')
ax1.axvspan(22, 38, color='#ffebee', alpha=0.4, label='Zona de Climatizacion (dP/dT > 0)')
ax1.set_ylabel('Potencia Electrica P (kW)', fontsize=11, fontweight='bold')
ax1.set_title('Modelo Matematico de Consumo de Potencia vs Temperatura Exterior', fontsize=12, fontweight='bold')
ax1.grid(True)
ax1.legend(loc='upper center', framealpha=0.9)

# Curva dP/dT
ax2.plot(T_range, dP_range, color='#e65100', linewidth=2.2, label="dP/dT = 0.020*(T - 22) [kW/°C]")
ax2.axhline(0.0, color='black', linestyle='-', linewidth=0.8)
ax2.axvline(22.0, color='#b71c1c', linestyle=':', linewidth=1.5)
ax2.scatter([22.0], [0.0], color='#b71c1c', s=70, zorder=5, label='Raiz dP/dT = 0 (Minimo consumo)')
ax2.set_xlabel('Temperatura Exterior T (°C)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Razon de Cambio dP/dT (kW/°C)', fontsize=11, fontweight='bold')
ax2.set_title('Primera Derivada: Razon de Cambio Marginal del Consumo', fontsize=12, fontweight='bold')
ax2.grid(True)
ax2.legend(loc='upper left', framealpha=0.9)

plt.tight_layout()
plt.savefig('grafica_1_modelo_y_derivada.png', dpi=300)
plt.close()
print("Guardada: grafica_1_modelo_y_derivada.png")

# GRAFICA 2: Perfiles Diarios de Temperatura T(t) (San Luis Potosi)
t_hours = np.linspace(0.0, 24.0, 500)

plt.figure(figsize=(9, 5))
for key, esc in escenarios.items():
    T_esc = temperatura_temporal(t_hours, esc['T_media'], esc['Amplitud'])
    plt.plot(t_hours, T_esc, color=esc['color'], linewidth=2.2,
             label=f"{esc['nombre']} (Min: {esc['T_min']}°C, Max: {esc['T_max']}°C)")

plt.axhline(22.0, color='#666666', linestyle='--', linewidth=1.2, label='Temperatura de confort base (22 °C)')
plt.title('Ciclo Termico Diario Representativo T(t) - San Luis Potosi', fontsize=12, fontweight='bold')
plt.xlabel('Hora del Dia (h)', fontsize=11, fontweight='bold')
plt.ylabel('Temperatura Exterior T (°C)', fontsize=11, fontweight='bold')
plt.xticks(np.arange(0, 25, 2))
plt.grid(True)
plt.legend(loc='lower center', framealpha=0.9)
plt.tight_layout()
plt.savefig('grafica_2_perfiles_temperatura.png', dpi=300)
plt.close()
print("Guardada: grafica_2_perfiles_temperatura.png")

# GRAFICA 3: Potencia Instantanea P(t) en 24 Horas
plt.figure(figsize=(9, 5.5))
for key, esc in escenarios.items():
    T_esc = temperatura_temporal(t_hours, esc['T_media'], esc['Amplitud'])
    P_esc = potencia(T_esc)
    plt.plot(t_hours, P_esc, color=esc['color'], linewidth=2.2, label=f"Demanda {key}: {esc['nombre']}")

plt.axhline(P_BASE, color='#333333', linestyle=':', linewidth=1.2, label=f'Potencia basal P_base = {P_BASE} kW')
plt.title('Curva de Potencia Instantanea P(t) = P(T(t)) a lo Largo de 24 Horas', fontsize=12, fontweight='bold')
plt.xlabel('Hora del Dia (h)', fontsize=11, fontweight='bold')
plt.ylabel('Potencia Electrica Demandada P (kW)', fontsize=11, fontweight='bold')
plt.xticks(np.arange(0, 25, 2))
plt.grid(True)
plt.legend(loc='upper right', framealpha=0.9)
plt.tight_layout()
plt.savefig('grafica_3_potencia_temporal.png', dpi=300)
plt.close()
print("Guardada: grafica_3_potencia_temporal.png")

# GRAFICA 4: Comparacion de Consumo Acumulado Base vs Optimizado
resultados = {}
for key, esc in escenarios.items():
    # Base
    e_base_analitica = energia_analitica(esc['T_media'], esc['Amplitud'], t_confort=T_CONFORT_BASE)
    T_esc = temperatura_temporal(t_hours, esc['T_media'], esc['Amplitud'])
    P_base_t = potencia(T_esc, t_confort=T_CONFORT_BASE)
    e_base_num = energia_numerica(t_hours, P_base_t)
    
    # Optimizado
    e_opt_analitica = energia_analitica(esc['T_media'], esc['Amplitud'], t_confort=esc['T_confort_opt'])
    P_opt_t = potencia(T_esc, t_confort=esc['T_confort_opt'])
    e_opt_num = energia_numerica(t_hours, P_opt_t)
    
    ahorro_kwh = e_base_analitica - e_opt_analitica
    pct_ahorro = (ahorro_kwh / e_base_analitica) * 100.0
    
    resultados[key] = {
        'nombre': esc['nombre'],
        'e_base': e_base_analitica,
        'e_base_num': e_base_num,
        'e_opt': e_opt_analitica,
        'e_opt_num': e_opt_num,
        'ahorro_kwh': ahorro_kwh,
        'pct_ahorro': pct_ahorro,
        'T_confort_opt': esc['T_confort_opt']
    }
    
    print(f"\n[{key.upper()}]")
    print(f"  Energia Base: {e_base_analitica:.3f} kWh (Numerica: {e_base_num:.3f} kWh)")
    print(f"  Energia Optimizada (T_confort={esc['T_confort_opt']}°C): {e_opt_analitica:.3f} kWh (Numerica: {e_opt_num:.3f} kWh)")
    print(f"  Ahorro: {ahorro_kwh:.3f} kWh ({pct_ahorro:.2f}%)")

# Grafico de barras comparativo
labels = ['Dia Frio\n(Invierno)', 'Dia Templado\n(Transicion)', 'Dia Calido\n(Verano)']
base_vals = [resultados['Frio']['e_base'], resultados['Templado']['e_base'], resultados['Calido']['e_base']]
opt_vals = [resultados['Frio']['e_opt'], resultados['Templado']['e_opt'], resultados['Calido']['e_opt']]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(8.5, 5))
rects1 = ax.bar(x - width/2, base_vals, width, label='Consumo Base (T_confort = 22 °C)', color='#5c6bc0')
rects2 = ax.bar(x + width/2, opt_vals, width, label='Consumo Optimizado (Consigna Adaptativa)', color='#26a69a')

ax.set_ylabel('Energia Total Acumulada (kWh/dia)', fontsize=11, fontweight='bold')
ax.set_title('Consumo Energetico Acumulado Diario: Base vs Optimizado', fontsize=12, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10, fontweight='bold')
ax.legend(framealpha=0.9)
ax.grid(axis='y')

# Etiquetas de valores sobre las barras
for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} kWh',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} kWh',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('grafica_4_comparacion_ahorro.png', dpi=300)
plt.close()
print("Guardada: grafica_4_comparacion_ahorro.png")
print("--- CALCULOS Y GRAFICAS COMPLETADOS CON EXITO ---")
