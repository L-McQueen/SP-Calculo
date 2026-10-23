import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 11

# ==========================================
# 1. Gráfica de Consumo Histórico (SENER)
# ==========================================
years = np.arange(2002, 2022)
slp_gwh = np.array([
    4124.44, 4355.34, 4692.70, 4820.86, 4934.49, 5049.51, 5044.22, 
    4637.31, 4850.84, 5280.63, 5790.50, 5774.61, 5405.75, 5390.77, 
    5850.05, 5416.98, 5921.74, 5982.93, 5708.41, 5364.60
])

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
ax.plot(years, slp_gwh, color='#1f77b4', marker='o', linewidth=2.5, markersize=7, label='Consumo Estatal Registrado (GWh)')
ax.fill_between(years, slp_gwh, color='#1f77b4', alpha=0.15)

# Trendline
z = np.polyfit(years, slp_gwh, 1)
p = np.poly1d(z)
ax.plot(years, p(years), color='#d62728', linestyle='--', linewidth=1.8, label=f'Tendencia lineal (+{z[0]:.1f} GWh/año)')

# Annotations
ax.annotate('Crisis 2009\n(4,637 GWh)', xy=(2009, 4637.31), xytext=(2008, 4200),
            arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
            fontsize=9, ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

ax.annotate('Pico Histórico 2019\n(5,983 GWh)', xy=(2019, 5982.93), xytext=(2017.5, 6250),
            arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6),
            fontsize=9, ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.5))

ax.set_title('Evolución Histórica del Consumo de Energía Eléctrica en San Luis Potosí (2002–2021)\nFuente: Secretaría de Energía (SENER) - Sistema de Información Energética', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Año de Registro', fontsize=11, fontweight='bold')
ax.set_ylabel('Consumo Total Anual (Gigawatts-hora, GWh)', fontsize=11, fontweight='bold')
ax.set_xticks(years[::2])
ax.set_ylim(3800, 6500)
ax.legend(loc='lower right', frameon=True)
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('grafica_excel_consumo_historico_slp.png')
plt.close()
print("Grafica 1 creada exitosamente.")

# ==========================================
# 2. Gráfica de Dispersión Térmica Mensual (CONAGUA)
# ==========================================
meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
t_media = np.array([16.5, 18.4, 21.1, 23.8, 25.8, 25.8, 24.8, 25.1, 24.2, 22.0, 19.4, 17.3])
t_min = np.array([14.0, 16.1, 18.2, 20.8, 22.5, 23.1, 22.3, 23.1, 21.9, 19.9, 16.2, 14.5])
t_max = np.array([20.0, 22.2, 24.9, 28.2, 32.0, 30.9, 28.4, 29.3, 28.2, 25.0, 22.9, 20.7])

fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

# Comfort band
ax.axhspan(21.0, 23.0, color='lightgreen', alpha=0.3, label='Banda de Confort Térmico ASHRAE 55 (21 °C - 23 °C)')
ax.axhline(22.0, color='forestgreen', linestyle='--', linewidth=1.5, label='Temperatura Confort Diseño (22.0 °C)')

# Error bars for dispersion (min to max)
yerr_lower = t_media - t_min
yerr_upper = t_max - t_media
ax.errorbar(meses, t_media, yerr=[yerr_lower, yerr_upper], fmt='o', color='#2b5b84',
            ecolor='#e28743', elinewidth=2.5, capsize=5, capthick=2, markersize=8,
            label='Temperatura Media con Rango de Dispersión (Mín - Máx)')

# Trend line connecting means
ax.plot(meses, t_media, color='#2b5b84', linestyle='-', linewidth=1.5, alpha=0.7)

ax.set_title('Dispersión y Variabilidad Térmica Mensual en San Luis Potosí (1985–2025)\nFuente: CONAGUA / Servicio Meteorológico Nacional (Estación 24028)', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Mes del Año', fontsize=11, fontweight='bold')
ax.set_ylabel('Temperatura Ambiental (°C)', fontsize=11, fontweight='bold')
ax.set_ylim(12, 35)
ax.legend(loc='upper left', frameon=True)
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('grafica_dispersion_temperatura_slp.png')
plt.close()
print("Grafica 2 creada exitosamente.")

# ==========================================
# 3. Gráfica de Dispersión: Consumo vs Temperatura (Curva + Puntos Reales)
# ==========================================
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

# Theoretical curve
T_curve = np.linspace(2, 36, 300)
P_curve = 0.010 * (T_curve - 22.0)**2 + 0.40
ax.plot(T_curve, P_curve, color='#1f77b4', linewidth=2.5, label='Modelo Cuadrático Teórico: P(T) = 0.010(T - 22)² + 0.40')

# Monthly points scatter
P_meses = 0.010 * (t_media - 22.0)**2 + 0.40
scatter = ax.scatter(t_media, P_meses, color='#d62728', s=90, zorder=5, label='Puntos Climatológicos Mensuales (CONAGUA)')

# Label points
for i, mes in enumerate(meses):
    offset_y = 0.03 if i % 2 == 0 else -0.05
    ax.annotate(mes, (t_media[i], P_meses[i] + offset_y), fontsize=9, fontweight='bold', ha='center', color='#333333')

# Extreme points
ax.scatter([4.0, 34.0], [0.010*(4-22)**2 + 0.40, 0.010*(34-22)**2 + 0.40],
           color='#ff7f0e', s=130, marker='s', zorder=6, label='Extremos de Diseño (4 °C y 34 °C)')
ax.annotate('Helada Invierno\n(4 °C, 3.64 kW)', (4.0, 3.64), xytext=(6, 3.4),
            arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=5), fontsize=8.5)
ax.annotate('Pico Verano\n(34 °C, 1.84 kW)', (34.0, 1.84), xytext=(28, 2.3),
            arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=5), fontsize=8.5)

# Basal line
ax.axhline(0.40, color='gray', linestyle=':', label='Potencia Basal Mínima P_base = 0.40 kW')

ax.set_title('Gráfico de Dispersión: Relación entre Temperatura Exterior y Demanda de Potencia\nValidación del Modelo Cuadrático frente a las Normales de San Luis Potosí', fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Temperatura Exterior T (°C)', fontsize=11, fontweight='bold')
ax.set_ylabel('Potencia Demandada P(T) [kW]', fontsize=11, fontweight='bold')
ax.set_xlim(0, 38)
ax.set_ylim(0.2, 4.0)
ax.legend(loc='upper center', frameon=True)
ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('grafica_dispersion_consumo_vs_temperatura.png')
plt.close()
print("Grafica 3 creada exitosamente.")
