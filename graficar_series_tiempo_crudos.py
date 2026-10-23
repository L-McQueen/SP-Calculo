# -*- coding: utf-8 -*-
"""
Generacion de graficas separadas con datos horarios crudos (t = 0 a 24 h):
1. Temperatura exterior respecto al tiempo T(t).
2. Consumo energetico instantaneo respecto al tiempo P(t).
Ubicacion: San Luis Potosi, S.L.P.
"""

import numpy as np
import matplotlib.pyplot as plt

# Configuracion de estilo tecnico
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.9
plt.rcParams['grid.color'] = '#dddddd'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

# Horas discretas crudas (0 a 24 h)
horas_crudas = np.arange(0, 25, 1) # 25 puntos horarios exactos
t_fino = np.linspace(0, 24, 400)

# Parametros del modelo
T_CONFORT = 22.0
P_BASE = 0.40
A_COEFF = 0.010

def temp_modelo(t, T_media, Amplitud):
    return T_media - Amplitud * np.cos(np.pi * (t - 6.0) / 12.0)

def pot_modelo(T):
    return A_COEFF * (T - T_CONFORT)**2 + P_BASE

# Escenarios de San Luis Potosi
escenarios = {
    'Frio': {
        'nombre': 'Dia Frio (Invierno)',
        'T_media': 12.0,
        'Amplitud': 8.0,
        'color': '#1565c0',
        'marker': 'o'
    },
    'Templado': {
        'nombre': 'Dia Templado (Primavera/Otono)',
        'T_media': 19.0,
        'Amplitud': 7.0,
        'color': '#2e7d32',
        'marker': 's'
    },
    'Calido': {
        'nombre': 'Dia Calido (Verano/Estiaje)',
        'T_media': 25.0,
        'Amplitud': 9.0,
        'color': '#c62828',
        'marker': '^'
    }
}

# =====================================================================
# GRAFICA 1: TEMPERATURA RESPECTO AL TIEMPO (DATOS CRUDOS Y CURVA)
# =====================================================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

for key, esc in escenarios.items():
    # Puntos crudos hora por hora
    T_crudos = temp_modelo(horas_crudas, esc['T_media'], esc['Amplitud'])
    # Curva continua
    T_curva = temp_modelo(t_fino, esc['T_media'], esc['Amplitud'])
    
    # Dibujar linea continua suave
    ax1.plot(t_fino, T_curva, color=esc['color'], linewidth=1.8, alpha=0.7, linestyle='-')
    # Dibujar puntos de datos crudos
    ax1.plot(horas_crudas, T_crudos, color=esc['color'], marker=esc['marker'], markersize=6.5,
             linewidth=0, label=f"{esc['nombre']} (Datos horarios crudos)")

# Linea de confort
ax1.axhline(T_CONFORT, color='#616161', linestyle=':', linewidth=1.5, label=f'Temperatura de confort interior ({T_CONFORT} °C)')

# Anotaciones de puntos criticos horarios
ax1.axvline(6.0, color='#9e9e9e', linestyle='--', linewidth=0.9)
ax1.text(6.1, 33.0, '06:00 h (Minima diurna)', fontsize=8.5, color='#424242', style='italic')

ax1.axvline(18.0, color='#9e9e9e', linestyle='--', linewidth=0.9)
ax1.text(18.1, 33.0, '18:00 h (Maxima diurna)', fontsize=8.5, color='#424242', style='italic')

ax1.set_title('Temperatura Exterior Respecto al Tiempo T(t) - San Luis Potosi\n(Registro horario crudo paso a paso)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Tiempo t (horas del dia)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Temperatura T (°C)', fontsize=11, fontweight='bold')
ax1.set_xlim(-0.5, 24.5)
ax1.set_ylim(2.0, 36.0)
ax1.set_xticks(horas_crudas)
ax1.grid(True)
ax1.legend(loc='upper left', framealpha=0.95, fontsize=9)

plt.tight_layout()
plt.savefig('grafica_temperatura_tiempo_crudo.png', dpi=300)
plt.close(fig1)
print("Guardada exitosamente: grafica_temperatura_tiempo_crudo.png")

# =====================================================================
# GRAFICA 2: CONSUMO ENERGETICO (POTENCIA) RESPECTO AL TIEMPO
# =====================================================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

for key, esc in escenarios.items():
    T_crudos = temp_modelo(horas_crudas, esc['T_media'], esc['Amplitud'])
    P_crudos = pot_modelo(T_crudos)
    
    T_curva = temp_modelo(t_fino, esc['T_media'], esc['Amplitud'])
    P_curva = pot_modelo(T_curva)
    
    # Curva suave
    ax2.plot(t_fino, P_curva, color=esc['color'], linewidth=1.8, alpha=0.7, linestyle='-')
    # Puntos crudos horarios
    ax2.plot(horas_crudas, P_crudos, color=esc['color'], marker=esc['marker'], markersize=6.5,
             linewidth=0, label=f"Consumo {esc['nombre']} (Datos horarios crudos)")

# Linea de potencia basal
ax2.axhline(P_BASE, color='#2e7d32', linestyle=':', linewidth=1.5, label=f'Potencia basal minima P_base = {P_BASE} kW')

ax2.set_title('Consumo Energetico Instantaneo Respecto al Tiempo P(t) - San Luis Potosi\n(Demanda de potencia horaria cruda)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Tiempo t (horas del dia)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Potencia Electrica Demandada P (kW)', fontsize=11, fontweight='bold')
ax2.set_xlim(-0.5, 24.5)
ax2.set_ylim(0.2, 3.9)
ax2.set_xticks(horas_crudas)
ax2.grid(True)
ax2.legend(loc='upper right', framealpha=0.95, fontsize=9)

plt.tight_layout()
plt.savefig('grafica_consumo_tiempo_crudo.png', dpi=300)
plt.close(fig2)
print("Guardada exitosamente: grafica_consumo_tiempo_crudo.png")

# Imprimir tabla de datos crudos en consola para revision
print("\n--- TABLA DE DATOS CRUDOS HORARIOS (T y P) ---")
print(f"{'Hora (t)':<9} | {'T_Frio (°C)':<12} | {'P_Frio (kW)':<12} | {'T_Temp (°C)':<12} | {'P_Temp (kW)':<12} | {'T_Cald (°C)':<12} | {'P_Cald (kW)':<12}")
print("-" * 88)
for h in [0, 3, 6, 9, 12, 15, 18, 21, 24]:
    tf = temp_modelo(h, 12.0, 8.0)
    pf = pot_modelo(tf)
    tt = temp_modelo(h, 19.0, 7.0)
    pt = pot_modelo(tt)
    tc = temp_modelo(h, 25.0, 9.0)
    pc = pot_modelo(tc)
    print(f"{h:>4} h    | {tf:>8.2f} °C   | {pf:>8.3f} kW   | {tt:>8.2f} °C   | {pt:>8.3f} kW   | {tc:>8.2f} °C   | {pc:>8.3f} kW")

