# Modelación Matemática del Consumo Energético en una Vivienda Inteligente
##  San Luis Potosí.

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Institution](https://img.shields.io/badge/Tecnológico%20de%20Monterrey-Situación%20Problema-0039A6.svg)](https://tec.mx/)

---


## 📌 Descripción del Proyecto

El sector residencial representa cerca de un tercio del consumo de energía eléctrica a nivel mundial, siendo los sistemas de climatización (calefacción y aire acondicionado) responsables de hasta el 50% de la factura eléctrica en regiones con variabilidad climática.

En este proyecto se formula, analiza y valida un **modelo matemático riguroso** basado en **cálculo diferencial e integral** que describe la demanda energética de una vivienda unifamiliar inteligente de 130 m² en San Luis Potosí, S.L.P. A partir de 40 años de registros meteorológicos oficiales de **CONAGUA/SMN (1985–2025)** y dos décadas de datos energéticos de la **Secretaría de Energía (SENER)**, el modelo permite:
1. Evaluar la potencia eléctrica instantánea requerida en función de la temperatura exterior.
2. Calcular la velocidad de cambio instantánea del consumo mediante la **primera derivada** (`dP/dT`).
3. Demostrar el punto de mínima demanda energética global con la **segunda derivada** (`d²P/dT²`).
4. Determinar la energía total diaria acumulada (`kWh/día`) integrando la potencia en el ciclo diario de 24 horas mediante **integrales definidas**.
5. Implementar una **estrategia de control domótico adaptativo** (norma ANSI/ASHRAE 55) que logra un ahorro del **20.93% de energía diaria** en invierno.

---

## 📐 Formulación Matemática del Modelo

### 1. Ecuación Cuadrática de Potencia Instantánea: `P(T)`
```text
P(T) = a * (T - T_confort)² + P_base
```
Sustituyendo los parámetros calibrados para la vivienda:
```text
P(T) = 0.010 * (T - 22.0)² + 0.40

Desarrollo algebraico:
P(T) = 0.010 * (T² - 44.0*T + 484.0) + 0.40
P(T) = 0.010*T² - 0.44*T + 5.24   [kW]
```

### 2. Primera Derivada: Razón de Cambio Instantánea (`dP/dT`)
```text
dP/dT = 2 * (0.010) * (T - 22.0) = 0.020 * (T - 22.0)   [kW/°C]
```
- **Zona Fría (T < 22 °C):** `dP/dT < 0`. Al subir la temperatura hacia el confort, la calefacción se apaga y el gasto disminuye (a 10 °C ahorra `240 W/°C`).
- **Punto de Confort (T = 22 °C):** `dP/dT = 0`. Razón de cambio nula; la casa opera en equilibrio térmico.
- **Zona Cálida (T > 22 °C):** `dP/dT > 0`. Cada grado adicional de calor exige más compresión al minisplit (a 32 °C demanda `200 W/°C` adicionales).

### 3. Segunda Derivada y Optimización: `d²P/dT²`
```text
d²P/dT² = d/dT [ 0.020 * (T - 22.0) ] = +0.020 kW/°C² > 0
```
Al ser estrictamente positiva en todo el dominio, la función es cóncava hacia arriba, demostrando la existencia de un **Mínimo Absoluto Global en T = 22.0 °C**, donde el gasto es exclusivamente la potencia base de **0.40 kW**.

### 4. Función Armónica de Temperatura Diaria: `T(t)`
```text
T(t) = T_media - A * cos( (pi / 12) * (t - 6.0) )   [°C]
```
Sincronizada con el ciclo solar terrestre: mínimo al amanecer (06:00 h) y máximo en la tarde (18:00 h).

### 5. Integral Definida de Energía Diaria: `E_diaria`
```text
E_diaria = integral desde 0 hasta 24 de P(t) dt

Fórmula Analítica Simplificada:
E_diaria = 24 * [ P_base + a * ( (T_media - T_confort)² + 0.5 * A² ) ]   [kWh/día]
```

---

## ⚙️ Parámetros Físicos y Justificación Normativa

| Parámetro | Valor de Diseño | Unidad | Sustento Físico y Normatividad Oficial |
| :--- | :---: | :---: | :--- |
| **`T_confort`** | **22.0** | °C | **ANSI/ASHRAE 55-2020** y media anual histórica de 40 años de CONAGUA/SMN en San Luis Potosí. |
| **`P_base`** | **0.40** (400 W) | kW | Cargas fijas continuas: Refrigerador Inverter (120 W, **NOM-015-ENER-2018**) + Domótica/Red (80 W, **ISO/IEC 14543**) + Standby (200 W, **NOM-032-ENER-2013**). Centro del rango oficial CONUEE (350–500 W). |
| **`a`** | **0.010** | kW/°C² | Calibración real: Minisplit de 1.5 T a 34 °C (`1.44 kW / 12² = 0.010`). Envolvente habitacional (**NOM-020-ENER-2011**) y eficiencia de minisplits inverter (**NOM-026-ENER-2015**). |
| **`omega`** | **pi / 12** (≈ 0.2618) | rad/h | Frecuencia angular de la rotación terrestre de 24 horas (`2*pi / 24 h`). |
| **`T_media`** | **12.0 / 19.0 / 25.0** | °C | Normales de 40 años CONAGUA/SMN para Invierno (Ene), Transición (Mar) y Verano (May). |
| **`A`** | **8.0 / 7.0 / 9.0** | °C | Semiamplitud de la oscilación térmica diurna-nocturna (`(T_max - T_min) / 2`). |

---

## 📊 Resultados de Simulación y Ahorro Energético

### Consumo Diario por Escenario (Integración Analítica vs Numérica)
| Escenario Climatológico | Temp. Media | Semiamplitud | Consumo Exacto | Trapecios (NumPy) | Error |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Día Frío (Enero)** | 12.0 °C | 8.0 °C | **41.280 kWh/día** | 41.280 kWh/día | **0.000 %** |
| **Día Templado (Marzo)** | 19.0 °C | 7.0 °C | **17.640 kWh/día** | 17.640 kWh/día | **0.000 %** |
| **Día Cálido (Mayo)** | 25.0 °C | 9.0 °C | **21.480 kWh/día** | 21.480 kWh/día | **0.000 %** |

### Estrategia de Consigna Adaptativa (ASHRAE 55)
Ajustando el termostato a **20.0 °C en invierno** (con ropa abrigada ligera de interiores, 1.0 clo) y a **24.0 °C en verano** (con ropa fresca, 0.5 clo):

| Escenario | Consumo Fijo (22 °C) | Consumo Adaptativo | Ahorro Diario (kWh) | % Reducción |
| :--- | :---: | :---: | :---: | :---: |
| **Día Frío (Invierno)** | 41.280 kWh/día | **32.640 kWh/día** | **8.640 kWh/día** | **20.93 % de ahorro** |
| **Día Templado** | 17.640 kWh/día | **17.640 kWh/día** | 0.000 kWh/día | 0.00 % (Neutro) |
| **Día Cálido (Verano)** | 21.480 kWh/día | **19.560 kWh/día** | **1.920 kWh/día** | **8.94 % de ahorro** |

---

## 🗂️ Estructura del Repositorio

```text
├── Base de datos (consumo energético 2002 - 2022).xls # Base histórica oficial SENER
├── 1985-2026/                           # 42 reportes meteorológicos oficiales CONAGUA/SMN
├── informe_tecnico_entregables_1_y_2.md # Reporte técnico completo en Markdown
├── requirements.txt                     # Dependencias de Python requeridas
├── .gitignore                           # Exclusión de entregables y rúbricas
├── README.md                            # Documentación técnica completa
│
├── simulacion_modelo.py                 # Simulación completa (P, derivada, T(t), integrales)
├── graficar_puntos_evaluados.py         # Evaluación de normales mensuales y diferencias
├── graficar_datos_excel_y_clima.py      # Series de tiempo SENER y dispersión CONAGUA
├── graficar_series_tiempo_crudos.py     # Gráficas de puntos discretos hora por hora (24h)
├── generar_pdf_situacion_problema.py    # Script que maqueta el reporte y compila a PDF
│
├── grafica_1_modelo_y_derivada.png      # Figura 3: Parábola P(T) y derivada dP/dT
├── grafica_2_perfiles_temperatura.png   # Figura 6: Perfiles horarios T(t) en 24h
├── grafica_3_potencia_temporal.png      # Figura 7: Demanda de potencia horaria P(t)
├── grafica_4_comparacion_ahorro.png     # Figura 8: Barras de consumo y ahorro adaptativo
├── grafica_5_puntos_evaluados.png       # Figura 4: Evaluación de meses y barras de delta P
├── grafica_excel_consumo_historico_slp.png # Figura 1: Serie de tiempo SENER (2002-2021)
├── grafica_dispersion_temperatura_slp.png  # Figura 2: Dispersión térmica mensual CONAGUA
└── grafica_dispersion_consumo_vs_temperatura.png # Figura 5: Dispersión cruzada T vs P(T)
```

---

## 🚀 Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar las simulaciones y generar gráficas
```bash
# Simulación general y cálculo analítico/numérico de integrales
python simulacion_modelo.py

# Gráficas del Excel de la SENER y dispersión térmica de CONAGUA
python graficar_datos_excel_y_clima.py

# Evaluación de los 12 meses históricos de San Luis Potosí
python graficar_puntos_evaluados.py

# Compilar el documento Word y el PDF de 16 páginas (requiere Word en Windows)
python generar_pdf_situacion_problema.py
```

---

## 📚 Referencias Bibliográficas

1. **ANSI/ASHRAE Standard 55-2020:** *Thermal Environmental Conditions for Human Occupancy*. Atlanta, GA.
2. **Cengel, Y. A., & Boles, M. A. (2019):** *Termodinámica* (9.ª ed.). McGraw-Hill Education.
3. **CONAGUA & SMN (1985–2025):** *Normales Climatológicas por Estación: Estación 24028 San Luis Potosí, S.L.P.*
4. **CONUEE (2020):** *El uso de energía eléctrica para confort térmico, reto mayor de política pública*. Gobierno de México.
5. **Incropera, F. P., et al. (2011):** *Fundamentals of Heat and Mass Transfer* (7.ª ed.). John Wiley & Sons.
6. **NOM-015-ENER-2018:** *Eficacia energética de refrigeradores y congeladores electrodomésticos*. Secretaría de Economía.
7. **NOM-020-ENER-2011:** *Eficiencia energética en edificaciones: Envolvente para uso habitacional*. Secretaría de Economía.
8. **NOM-026-ENER-2015:** *Eficiencia energética en acondicionadores de aire tipo dividido (Minisplit Inverter)*. Secretaría de Economía.
9. **NOM-032-ENER-2013:** *Límites máximos de potencia eléctrica en modo de espera (Standby)*. Secretaría de Economía.
10. **SENER (2022):** *Sistema de Información Energética: Consumo de energía eléctrica por entidad federativa 2002–2022*.
11. **Stewart, J. (2018):** *Cálculo de una variable: Trascendentes tempranas* (8.ª ed.). Cengage Learning.
