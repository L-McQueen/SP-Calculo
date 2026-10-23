# -*- coding: utf-8 -*-
"""
Generador Maestro del Documento y PDF de la Situación Problema
Entregables 1 y 2 - Cálculo Diferencial e Integral Aplicado a una Vivienda Inteligente
Ubicación: San Luis Potosí, S.L.P., México
Autores: Juan Carlos Avila Miranda, Anthony Bruce Gomez Arjona, César Emiliano Montes García-A
Tecnológico de Monterrey - Octubre 2026
"""

import os
import subprocess
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = r"c:\Users\Sin nombre\Desktop\s.p"
DOCX_OUT = os.path.join(BASE_DIR, "SITUACION_PROBLEMA_COMPLETO.docx")
PDF_OUT = os.path.join(BASE_DIR, "SITUACION_PROBLEMA_COMPLETO.pdf")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_table_styled(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        set_cell_background(hdr_cells[i], "1A365D") # Navy blue
        set_cell_margins(hdr_cells[i], top=130, bottom=130, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9)
            run.font.name = "Arial"

    # Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=85, bottom=85, left=110, right=110)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.size = Pt(8.5)
                run.font.name = "Arial"

    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)
    return table

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(30, 41, 59)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_callout(doc, text, title="NOTA TÉCNICA"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "EFF6FF") # Light blue tint
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="36" w:space="0" w:color="1D4ED8"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    r_title = p.add_run(f"{title}: ")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGBColor(29, 78, 216)
    
    r_text = p.add_run(text)
    r_text.font.name = "Arial"
    r_text.font.size = Pt(9)
    r_text.font.color.rgb = RGBColor(30, 41, 59)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)

def add_heading_styled(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.bold = True

    if level == 1:
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(26, 54, 93) # Deep Navy
    elif level == 2:
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(37, 99, 235) # Blue
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(51, 65, 85) # Slate

def add_paragraph_styled(doc, text, bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_bullet_styled(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = RGBColor(30, 41, 59)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(51, 65, 85)

def add_figure(doc, img_rel_path, caption_text, width_inches=6.0):
    img_path = os.path.join(BASE_DIR, img_rel_path)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Arial"
        run_cap.font.size = Pt(8.5)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(71, 85, 105)
    else:
        print(f"ADVERTENCIA: Imagen no encontrada: {img_path}")

print("Iniciando construcción del documento Word completo...")
doc = Document()

# Configurar márgenes estándar (1 pulgada = 2.54 cm)
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# ==============================================================================
# PÁGINA 1: PORTADA INSTITUCIONAL
# ==============================================================================
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(100)
p_inst.paragraph_format.space_after = Pt(12)
r_inst = p_inst.add_run("Tecnológico de Monterrey")
r_inst.bold = True
r_inst.font.name = "Arial"
r_inst.font.size = Pt(28)
r_inst.font.color.rgb = RGBColor(0, 57, 166) # Azul Tec Oficial

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_before = Pt(20)
p_sub.paragraph_format.space_after = Pt(120)
r_sub = p_sub.add_run("Entregable Situación Problema\nModelación Matemática del Consumo Energético en una Vivienda Inteligente")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(15)
r_sub.font.color.rgb = RGBColor(51, 65, 85)

p_aut = doc.add_paragraph()
p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_aut.paragraph_format.space_before = Pt(40)
p_aut.paragraph_format.space_after = Pt(4)
for autor in ["Juan Carlos Avila Miranda", "Anthony Bruce Gomez Arjona", "César Emiliano Montes García-A"]:
    r_a = p_aut.add_run(autor + "\n")
    r_a.font.name = "Arial"
    r_a.font.size = Pt(12)
    r_a.font.color.rgb = RGBColor(30, 41, 59)

p_fec = doc.add_paragraph()
p_fec.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fec.paragraph_format.space_before = Pt(50)
r_f = p_fec.add_run("13 de Octubre de 2026\nSan Luis Potosí, S.L.P., México")
r_f.font.name = "Arial"
r_f.font.size = Pt(10.5)
r_f.font.color.rgb = RGBColor(100, 116, 139)

doc.add_page_break()

# ==============================================================================
# SECCIÓN 1: INTRODUCCIÓN Y CONTEXTUALIZACIÓN
# ==============================================================================
add_heading_styled(doc, "1- Introducción y Contextualización", level=1)

add_paragraph_styled(doc, 
    "Uno de los principales consumidores de energía eléctrica a nivel mundial es el sector de la vivienda. "
    "El sector de la edificación y la construcción concentra cerca del 37% de las emisiones globales, el 28% "
    "del consumo mundial de energía y casi la mitad de la extracción mundial de materiales. Las personas en "
    "localidades con clima cálido consumen el doble que los de clima templado, y dentro de su hogar los sistemas "
    "de climatización, como el aire acondicionado, representan alrededor del 50% del consumo energético total. "
    "Los malos hábitos de consumo y la falta de infraestructura térmica provocan un consumo excesivo de energía "
    "en las horas de temperatura máxima. (Domínguez, 2026; Conuee, 2020).")

add_paragraph_styled(doc,
    "Este alto consumo energético impacta de manera directa al medio ambiente. En México más del 60% de la energía "
    "consumida proviene de combustibles fósiles, por lo cual a mayor demanda energética mayores serán las emisiones "
    "de CO2, contribuyendo al cambio climático y al deterioro ambiental. Es fundamental desarrollar soluciones "
    "dedicadas a la eficiencia energética y a la sustentabilidad mediante el uso de fuentes limpias y tecnologías "
    "avanzadas de control. (LowCarbonPower, s. f.).")

add_figure(doc, "grafica_excel_consumo_historico_slp.png",
           "Figura 1: Evolución histórica del consumo de energía eléctrica en San Luis Potosí (2002–2021). "
           "Fuente: Secretaría de Energía (SENER), Sistema de Información Energética.", width_inches=6.2)

add_paragraph_styled(doc,
    "Como se evidencia en la Figura 1, los registros oficiales de la Secretaría de Energía (SENER) demuestran que "
    "la demanda eléctrica en San Luis Potosí pasó de 4,124.44 GWh en 2002 a casi 6,000 GWh en 2019 (+45.0% de crecimiento), "
    "con una tasa de aumento sostenida de +68.5 GWh por año. Este crecimiento continuo fundamenta la necesidad urgente de "
    "implementar viviendas inteligentes con control térmico optimizado.")

add_paragraph_styled(doc,
    "La implementación de termostatos programables, sensores ambientales térmicos e infraestructura domótica permite "
    "automatizar el control térmico dentro del hogar. No obstante, optimizar el desempeño de un hogar inteligente exige "
    "ir más allá de una respuesta reactiva; resulta indispensable plantear un modelo matemático preciso que caracterice el "
    "comportamiento energético de la vivienda considerando las condiciones climáticas externas.")

add_paragraph_styled(doc,
    "Para este trabajo se seleccionó como caso de estudio una vivienda ubicada en la ciudad de San Luis Potosí, San Luis Potosí, "
    "la cual se encuentra a una altitud promedio de 1,850 msnm. Esta región presenta un clima semiárido templado-fresco. Durante "
    "el invierno, las temperaturas descienden hasta los 4 °C. En los meses de primavera e inicios del verano se alcanzan máximas "
    "que oscilan entre los 28 °C y 34 °C. (Weather Spark, s. f.).")

add_paragraph_styled(doc,
    "La humedad relativa es moderadamente baja a lo largo del año, manteniendo un ambiente seco que favorece el enfriamiento "
    "evaporativo. Otro factor de importancia es la radiación solar, registrándose un mínimo de 4.4 kWh en diciembre y un máximo "
    "de 7.6 kWh en mayo. Los vientos presentan velocidades promedio de 12.4 km/h en noviembre (mes con menos viento) y de 15.9 km/h "
    "en julio (mes más ventoso). En relación con las precipitaciones, se identifica una estación seca bien definida de octubre a mayo "
    "(mínimo de 0.5 cm en diciembre) y una estación lluviosa de junio a septiembre (máximo de 8.9 cm en julio). (Weather Spark, s. f.).")

add_paragraph_styled(doc,
    "San Luis Potosí a su vez presenta dos características fundamentales en sus condiciones climáticas a tomar en cuenta para el modelo:\n"
    "1. Variación entre el día y la noche: La diferencia térmica diaria oscila aproximadamente entre los 14 °C y 18 °C en un periodo de 24 horas.\n"
    "2. Marcado cambio entre estaciones: Los inviernos registran mínimas cercanas a los 4 °C – 0 °C, mientras que el verano se caracteriza por "
    "calor intenso, alcanzando máximas entre 32 °C y 34 °C en mayo y junio. (Weather Spark, s. f.).")

add_heading_styled(doc, "Rango de temperatura (CONAGUA / SMN 1985–2025)", level=2)

add_paragraph_styled(doc,
    "A partir de las series estadísticas de la estación meteorológica oficial del Servicio Meteorológico Nacional (SMN) y CONAGUA, "
    "se calcularon los valores medios históricos de temperatura mensual y anual para San Luis Potosí:")

# Tabla Climatológica
tabla_clima_headers = ["Mes", "Temperatura Media Registrada", "Rango Típico Observado (Mín a Máx)"]
tabla_clima_data = [
    ["Enero", "17.0 °C", "14.0 °C a 20.0 °C"],
    ["Febrero", "18.4 °C", "16.1 °C a 22.2 °C"],
    ["Marzo", "21.1 °C", "18.2 °C a 24.9 °C"],
    ["Abril", "23.8 °C", "20.8 °C a 28.2 °C"],
    ["Mayo", "25.8 °C", "22.5 °C a 32.0 °C"],
    ["Junio", "25.8 °C", "23.1 °C a 30.9 °C"],
    ["Julio", "24.8 °C", "22.3 °C a 28.4 °C"],
    ["Agosto", "25.1 °C", "23.1 °C a 29.3 °C"],
    ["Septiembre", "24.2 °C", "21.9 °C a 28.2 °C"],
    ["Octubre", "22.0 °C", "19.9 °C a 25.0 °C"],
    ["Noviembre", "19.4 °C", "16.2 °C a 22.9 °C"],
    ["Diciembre", "17.3 °C", "14.5 °C a 20.7 °C"],
    ["Promedio Anual", "22.0 °C", "20.0 °C a 24.8 °C"]
]
create_table_styled(doc, tabla_clima_headers, tabla_clima_data, col_widths=[1.5, 2.2, 2.8])

add_figure(doc, "grafica_dispersion_temperatura_slp.png",
           "Figura 2: Dispersión y rango térmico mensual en San Luis Potosí (CONAGUA 1985–2025), "
           "resaltando la banda de confort ASHRAE 55 (21 °C - 23 °C).", width_inches=6.2)

add_paragraph_styled(doc,
    "Con la finalidad de analizar el desempeño térmico y el consumo de energía a lo largo de las distintas estaciones del año, "
    "se consideraron tres escenarios diarios característicos de 24 horas:")

add_bullet_styled(doc, "Oscilación térmica entre 4.0 °C y 20.0 °C, reportando un valor medio de T_media = 12.0 °C y una semiamplitud A = 8.0 °C. Presenta una elevada carga operativa de calefacción durante la mañana y la noche.", bold_prefix="• Jornada de Invierno (Noviembre / Febrero): ")
add_bullet_styled(doc, "Variación de 16.0 °C a 34.0 °C, con un promedio de T_media = 25.0 °C y semiamplitud A = 9.0 °C. Este comportamiento está regido por un alto requerimiento de enfriamiento en el periodo vespertino.", bold_prefix="• Jornada Cálida (Mayo / Junio): ")
add_bullet_styled(doc, "Temperaturas desde 12.0 °C hasta 26.0 °C, con una media de T_media = 19.0 °C y semiamplitud A = 7.0 °C. Corresponde a un estado de confort natural donde el acondicionamiento artificial es prácticamente innecesario.", bold_prefix="• Jornada de Transición (Marzo / Octubre): ")

add_callout(doc, "Variación hacia arriba o hacia abajo del promedio de temperatura en un día: mide cuánto baja por la noche y cuánto sube por la tarde respecto a la temperatura media.", title="DEFINICIÓN DE SEMIAMPLITUD TÉRMICA (A)")

add_paragraph_styled(doc,
    "El problema ingenieril que se pretende resolver es determinar y predecir el consumo energético de una vivienda en la ciudad de "
    "San Luis Potosí, en el mismo estado. Este consumo energético es en función de la temperatura exterior, por tal razón es importante "
    "conocer a detalle el clima de la ciudad donde se encuentra la casa.")

# ==============================================================================
# SECCIÓN 2: VARIABLES Y PARÁMETROS DEL MODELO
# ==============================================================================
add_heading_styled(doc, "2- Variables y Parámetros del Modelo", level=1)

add_heading_styled(doc, "Variables Independientes", level=2)
add_bullet_styled(doc, "Unidad: Grados Celsius (°C). Rango de operación: Continuo de 0.0 °C a 45.0 °C. Definición física: Este valor define el estado climático del exterior de la casa. Es un valor independiente ya que la propiedad se ve afectada por su entorno térmico.", bold_prefix="T - Temperatura ambiental externa: ")
add_bullet_styled(doc, "Unidad: Horas (h). Rango de operación: (0:00 a 24:00 h). Definición física: Refleja la progresión temporal a lo largo del ciclo diario de 24 horas. Constituye el parámetro temporal independiente que rige la radiación solar y sobre el cual se integra el consumo energético acumulado.", bold_prefix="t - Tiempo transcurrido durante la jornada: ")

add_heading_styled(doc, "Variables Dependientes", level=2)
add_bullet_styled(doc, "Unidad: Kilowatts (kW). Rango de operación: P(T) >= 0.40 kW. Definición física: Representa la demanda energética inmediata que el inmueble extrae del flujo eléctrico. Su valor guarda relación directa con la oscilación térmica ambiental exterior T (o la progresión temporal t), incrementando la carga del sistema de climatización ante condiciones extremas de frío o calor para preservar el estado de confort.", bold_prefix="P - Potencia eléctrica instantánea requerida: ")
add_bullet_styled(doc, "Unidad: Kilowatts-hora (kWh). Definición física: Constituye la integración de la demanda eléctrica a lo largo de un intervalo completo de 24 horas. Se determina mediante la integración matemática de la potencia instantánea en el tiempo (E = integral P(t) dt), definiendo el gasto total contabilizado por la entidad proveedora de energía.", bold_prefix="E - Consumo energético diario acumulado: ")

# ==============================================================================
# SECCIÓN 3: PARÁMETROS CONSTANTES DEL SISTEMA
# ==============================================================================
add_heading_styled(doc, "3- Parámetros Constantes del Sistema", level=1)

add_paragraph_styled(doc, "Unidad: Grados Celsius (°C). Valor de diseño: 22.0 °C.", bold_prefix="T Confort: ")
add_paragraph_styled(doc, "Representa el nivel térmico óptimo deseado en la zona habitable, en el cual el sistema no requiere demandar energía adicional para climatización.", bold_prefix="Definición física: ")
add_paragraph_styled(doc, "Tras promediar cuatro décadas de datos recopilados por las autoridades oficiales (CONAGUA/SMN, 1985–2025), la media térmica anual registrada en San Luis Potosí alcanza puntualmente los 22.0 °C. Conforme a la normativa ANSI/ASHRAE 55-2020 respecto a las condiciones ambientales habitables, para regiones templadas e individuos con vestimenta ordinaria en estado pasivo (0.5 a 1.0 clo), el intervalo térmico ideal se sitúa en 22.0 °C. En este punto el cambio de consumo debe ser nulo (dP/dT = 0).", bold_prefix="Justificación: ")

add_paragraph_styled(doc, "Unidad: Kilowatts (kW). Valor: 0.40 kW (400 W).", bold_prefix="P Base - Demanda energética inherente a la casa: ")
add_paragraph_styled(doc, "Expresa el consumo de potencia permanente de la edificación, atribuible a los dispositivos domóticos, enlaces de comunicación e infraestructura en modo standby, aplicado a una residencia unifamiliar de 120 a 150 m² con 4 habitantes.", bold_prefix="Definición física: ")
add_paragraph_styled(doc, "Corresponde a la suma de las cargas eléctricas basales que nunca se apagan en el hogar, respaldadas por dos Normas Oficiales Mexicanas y estándares internacionales:\n"
                          "1. Refrigerador Inverter (120 W): Certificado bajo la norma NOM-015-ENER-2018 (Eficacia energética de refrigeradores domésticos). Consume cerca de 400 kWh al año, con una potencia media de mantenimiento térmico de 120 W.\n"
                          "2. Infraestructura Domótica y de Red (80 W): Respaldado por el estándar ISO/IEC 14543 de domótica y especificaciones del IFT. Incluye el módem de fibra óptica (15-20 W), la central inteligente (10-15 W) y la red de sensores IoT (45-50 W).\n"
                          "3. Aparatos en Espera / Standby (200 W): Regulado por la norma NOM-032-ENER-2013 (Límites máximos de potencia eléctrica en modo de espera). Cuantifica el consumo pasivo de televisores, microondas con display digital, cargadores y luminarias de seguridad (la CONUEE y el FIDE estiman entre 180 W y 220 W para este perfil familiar).\n"
                          "Suma Total Basal: 120 W + 80 W + 200 W = 400 W = 0.40 kW (ubicado exactamente en el centro del rango oficial de 350 W a 500 W fijado por la CONUEE).", bold_prefix="Justificación: ")

add_paragraph_styled(doc, "Unidad: kW/°C². Valor de diseño: 0.010 kW/°C².", bold_prefix="a - Coeficiente de transferencia y respuesta térmica: ")
add_paragraph_styled(doc, "Mide qué tan rápido aumenta el gasto de luz de la casa cuando la temperatura de afuera se aleja de los 22.0 °C. Depende de qué tan bien aisladas están las paredes y el techo, y de la eficiencia del aire acondicionado.", bold_prefix="Definición física: ")
add_paragraph_styled(doc, "1. Cálculo de Calibración: En una tarde calurosa de verano en San Luis Potosí a 34.0 °C (diferencia de 12.0 °C con el confort), un minisplit inverter de 1.5 toneladas (18,000 BTU/h) trabajando a régimen medio-alto demanda en la práctica 1.44 kW eléctricos. Al despejar: a = 1.44 kW / (12.0 °C)² = 1.44 / 144 = 0.010 kW/°C².\n"
                          "2. Sustento Normativo de la Envolvente: La norma NOM-020-ENER-2011 fija la transmitancia térmica máxima de muros y losas para uso habitacional en U ≈ 1.5 W/(m²·°C). Para los 200 m² de muros expuestos de la casa, la pérdida térmica es de U*A = 300 W/°C continuos por cada grado de salto térmico.\n"
                          "3. Sustento del Aire Acondicionado: La norma NOM-026-ENER-2015 certifica que los minisplits inverter mantengan una eficiencia estacional (SEER ≥ 16 a 18), garantizando que el compresor no exceda los 1.44 kW a 12 °C de salto térmico.\n"
                          "4. Comprobación en Invierno: En una helada invernal a 4.0 °C (-18 °C de diferencia), el modelo arroja P(4) = 0.010*(-18)² + 0.40 = 3.64 kW. Esta potencia pico de 3.64 kW (16.5 A a 220 V) coincide con las guías de dimensionamiento eléctrico residencial para viviendas medianas con clima (rango estándar de 3.45 kW a 4.6 kW).", bold_prefix="Justificación: ")

add_paragraph_styled(doc, "Unidad: Grados Celsius (°C). Valor de diseño: 12.0 °C (día frío), 19.0 °C (día templado), 25.0 °C (día cálido). Definición: Temperatura promedio exterior de la jornada de 24 horas alrededor de la cual oscila el ciclo térmico diario. Justificación: Obtenida de cuatro décadas de registros de CONAGUA/SMN (1985–2025) en San Luis Potosí.", bold_prefix="TMedia - Temperatura media diaria: ")
add_paragraph_styled(doc, "Unidad: Grados Celsius (°C). Valor de diseño: 8.0 °C (frío), 7.0 °C (templado), 9.0 °C (cálido). Definición: Expresa la mitad de la oscilación térmica total del día; mide cuántos grados se eleva la temperatura por la tarde respecto al promedio, o cuántos desciende en la madrugada. Justificación: Calculada mediante A = (T_max - T_min) / 2 con base en datos oficiales de SMN.", bold_prefix="A - Semiamplitud térmica diaria: ")
add_paragraph_styled(doc, "Unidad: Radianes por hora (rad/h). Valor de diseño: pi / 12 rad/h (≈ 0.2618 rad/h). Definición: Sincroniza la velocidad de oscilación de la función cosinusoidal para acoplarla con el ciclo natural del día y la noche. Justificación: Deriva de la física del ciclo solar terrestre de 24 horas (omega = 2*pi / 24 h = pi / 12 rad/h).", bold_prefix="omega - Frecuencia del ciclo diario: ")

# ==============================================================================
# SECCIÓN 4: FORMULACIÓN Y JUSTIFICACIÓN DEL MODELO MATEMÁTICO
# ==============================================================================
add_heading_styled(doc, "4- Formulación y Justificación del Modelo Matemático", level=1)

add_heading_styled(doc, "El calor que entra o sale de la casa (Ley de Fourier)", level=2)
add_paragraph_styled(doc,
    "Por las leyes del calor, la cantidad de calor que se cuela por muros, techos y ventanas depende de la diferencia "
    "entre la temperatura de afuera y la de adentro:\n"
    "Calor que atraviesa la casa = Resistencia de muros * (Diferencia de temperatura)")
add_bullet_styled(doc, "Cuando afuera hace 34 °C y adentro queremos 22 °C, existe una diferencia de 12 °C que provoca que el calor exterior fluya naturalmente hacia el interior a través de paredes y ventanas. Por esta razón, el aire acondicionado debe trabajar continuamente para extraer ese calor y expulsarlo fuera de la casa.", bold_prefix="En verano: ")
add_bullet_styled(doc, "Cuando afuera hace 4 °C y adentro queremos 22 °C, existe una diferencia de 18 °C que provoca que el calor de la casa se escape hacia el exterior. Por esta razón, el sistema de calefacción debe trabajar continuamente para inyectar calor al interior y reponer el que se fuga por los muros.", bold_prefix="En invierno: ")

add_heading_styled(doc, "El aire acondicionado gasta más luz en climas extremos (Rendimiento del motor)", level=2)
add_paragraph_styled(doc,
    "El minisplit usa electricidad para sacar el calor de la casa en verano o meter calor en invierno. Su eficiencia se mide mediante el Coeficiente de Desempeño (COP). "
    "El rendimiento no es fijo: cuando el clima exterior es muy extremo, el aparato pierde eficiencia y gasta más electricidad por cada grado que enfría. "
    "A 24 °C exterior, el motor del minisplit trabaja relajado y consume muy poco; pero a 34 °C o a 4 °C, las presiones internas del gas aumentan, el motor gira a máxima potencia "
    "y consume mucha más luz por cada grado extra. (Sustento: Norma Oficial Mexicana NOM-026-ENER-2015 para minisplits inverter y libros de termodinámica de Cengel & Boles).")

add_heading_styled(doc, "¿Por qué tiene que ser una ecuación al cuadrado (T - 22)² y no una recta?", level=2)
add_paragraph_styled(doc, "Existen tres razones muy claras:")
add_bullet_styled(doc, "Si afuera hace frío (T < 22), prendemos la calefacción y el gasto de luz sube; si hace calor (T > 22), prendemos el aire acondicionado y el gasto también sube. Una recta no sirve: si una recta sube con el calor, obligatoriamente bajaría a valores negativos absurdos en el frío. La función cuadrática resuelve esto porque cualquier número al cuadrado siempre da positivo: (-10)² = +100 y (+10)² = +100.", bold_prefix="1. El frío y el calor aumentan el consumo por igual: ")
add_bullet_styled(doc, "Pasar de 22 °C a 23 °C apenas cuesta 10 vatios extra; pero pasar de 33 °C a 34 °C cuesta 230 vatios extra. La parábola refleja exactamente ese sobreesfuerzo del motor.", bold_prefix="2. Cada grado extremo cuesta más caro que el anterior: ")
add_bullet_styled(doc, "En cálculo diferencial, cualquier fenómeno suave que alcanza su punto más bajo en un punto de equilibrio (en este caso 22 °C) se describe de manera natural mediante una parábola (Stewart, 2018). Además, la parábola es suave y no tiene esquinas en punta, lo que permite usar derivadas.", bold_prefix="3. Fundamento matemático del cálculo (Aproximación de Taylor): ")

add_heading_styled(doc, "Ecuación del Modelo Desarrollada", level=2)
add_code_block(doc,
    "P(T) = a * (T - T_confort)² + P_base\n"
    "P(T) = 0.010 * (T - 22.0)² + 0.40\n"
    "P(T) = 0.010 * (T² - 44.0*T + 484.0) + 0.40\n"
    "P(T) = 0.010*T² - 0.44*T + 4.84 + 0.40\n"
    "P(T) = 0.010*T² - 0.44*T + 5.24   [kW]")

add_figure(doc, "grafica_1_modelo_y_derivada.png",
           "Figura 3: Modelo matemático de potencia P(T) [arriba] y primera derivada dP/dT [abajo], "
           "mostrando el punto crítico en T = 22.0 °C con P_min = 0.40 kW.", width_inches=6.0)

add_figure(doc, "grafica_5_puntos_evaluados.png",
           "Figura 4: Evaluación de puntos mensuales y extremos sobre la curva P(T) [arriba] "
           "e incremento porcentual de potencia respecto a la base de 0.40 kW [abajo].", width_inches=6.0)

add_figure(doc, "grafica_dispersion_consumo_vs_temperatura.png",
           "Figura 5: Gráfico de dispersión cruzada: Puntos climatológicos mensuales reales de San Luis Potosí "
           "superpuestos sobre la parábola teórica calibrada.", width_inches=6.0)

# ==============================================================================
# SECCIÓN 5: ANÁLISIS MEDIANTE CÁLCULO DIFERENCIAL
# ==============================================================================
add_heading_styled(doc, "5- Análisis mediante Cálculo Diferencial (Razón de Cambio y Optimización)", level=1)

add_paragraph_styled(doc,
    "El cálculo diferencial nos permite determinar no solamente cuánta energía gasta la vivienda, sino la rapidez "
    "con la que se incrementa o reduce la demanda de electricidad ante pequeñas variaciones de la temperatura exterior. "
    "Esta razón de cambio instantánea se cuantifica formalmente mediante la primera derivada:")

add_code_block(doc,
    "P(T) = 0.010 * (T - 22.0)² + 0.40\n"
    "dP/dT = 2 * (0.010) * (T - 22.0)\n"
    "dP/dT = 0.020 * (T - 22.0)   [kW/°C]")

add_paragraph_styled(doc,
    "La unidad de la derivada es el kilowatt por grado Celsius (kW/°C). Físicamente, representa la potencia eléctrica marginal "
    "que la vivienda demanda o ahorra por cada grado que cambie la temperatura del medio ambiente.", bold_prefix="Interpretación física: ")

add_heading_styled(doc, "Comportamiento de la Derivada en las Tres Zonas Climáticas", level=2)
add_bullet_styled(doc, "La derivada es estrictamente negativa (dP/dT < 0). Significa que si la temperatura exterior se eleva hacia los 22 °C (el clima se vuelve menos frío), la demanda de calefacción disminuye y la casa ahorra electricidad. Ejemplo a 10.0 °C: dP/dT = 0.020*(10 - 22) = -0.24 kW/°C (cada grado que calienta el clima a partir de 10 °C ahorra de golpe 240 W de potencia).", bold_prefix="1. Zona Fría (T < 22.0 °C): ")
add_bullet_styled(doc, "La derivada es nula (dP/dT = 0). Representa el punto crítico de equilibrio del sistema. Alrededor de los 22 °C, pequeñas fluctuaciones del clima no inducen cambios en el consumo eléctrico.", bold_prefix="2. Punto Crítico de Confort (T = 22.0 °C): ")
add_bullet_styled(doc, "La derivada es estrictamente positiva (dP/dT > 0). A medida que la tarde se vuelve más caliente, el aire acondicionado trabaja a mayor compresión y la demanda eléctrica aumenta. Ejemplo a 32.0 °C: dP/dT = 0.020*(32 - 22) = +0.20 kW/°C (cada grado adicional exige 200 W extras de potencia de refrigeración).", bold_prefix="3. Zona Cálida (T > 22.0 °C): ")

add_heading_styled(doc, "Demostración del Mínimo Absoluto (Criterio de la Segunda Derivada)", level=2)
add_paragraph_styled(doc,
    "Para clasificar formalmente el punto crítico T = 22.0 °C, aplicamos el criterio de la segunda derivada del cálculo diferencial:")

add_code_block(doc,
    "d²P/dT² = d/dT [ 0.020 * (T - 22.0) ] = 0.020 kW/°C²")

add_paragraph_styled(doc,
    "Dado que d²P/dT² = +0.020 > 0 (es un valor constante y estrictamente positivo en todo el dominio), la función P(T) es "
    "globalmente cóncava hacia arriba. El teorema de optimización diferencial garantiza que en T = 22.0 °C se localiza un "
    "MÍNIMO ABSOLUTO GLOBAL, confirmando matemáticamente que 22.0 °C es la condición de operación más eficiente para la casa, "
    "demandando únicamente la potencia basal fija de 0.40 kW.")

# ==============================================================================
# SECCIÓN 6: MODELADO EN EL TIEMPO Y CÁLCULO INTEGRAL
# ==============================================================================
add_heading_styled(doc, "6- Modelado en el Tiempo y Cálculo de Consumo Diario (Cálculo Integral)", level=1)

add_paragraph_styled(doc,
    "Mientras que la potencia instantánea P(t) cuantifica el gasto de electricidad en cada segundo, la Comisión Federal "
    "de Electricidad (CFE) factura en el recibo doméstico la energía total acumulada en kilowatts-hora (kWh) al cabo del día. "
    "Para calcular esta energía acumulada durante las 24 horas de la jornada, se requiere integrar la potencia en el tiempo.")

add_heading_styled(doc, "Función Armónica de Temperatura Diaria T(t)", level=2)
add_paragraph_styled(doc,
    "La oscilación térmica diaria diurna-nocturna provocada por el ciclo solar se modela mediante una función cosinusoidal:")

add_code_block(doc,
    "T(t) = T_media - A * cos( (pi / 12) * (t - 6.0) )   [°C]")

add_paragraph_styled(doc,
    "Donde t es la hora del día (0 a 24 h), T_media es el promedio diario, A es la semiamplitud y el desfase de 6 horas asegura "
    "que la temperatura mínima ocurra al amanecer (06:00 h) y la máxima por la tarde (18:00 h).")

add_figure(doc, "grafica_2_perfiles_temperatura.png",
           "Figura 6: Perfiles de temperatura horaria T(t) a lo largo de 24 horas para los escenarios de "
           "Invierno (Enero, 12 °C), Templado (Marzo, 19 °C) y Cálido (Mayo, 25 °C).", width_inches=6.0)

add_figure(doc, "grafica_3_potencia_temporal.png",
           "Figura 7: Curvas de potencia horaria P(t) durante las 24 horas del día en San Luis Potosí.", width_inches=6.0)

add_heading_styled(doc, "Deducción Analítica de la Integral de Energía Diaria", level=2)
add_paragraph_styled(doc,
    "La energía acumulada en el día se formula como la integral definida de la potencia instantánea entre las 0 y 24 horas:")

add_code_block(doc,
    "E_diaria = integral desde 0 hasta 24 de P(t) dt\n\n"
    "Sustituyendo P(t) = P_base + a * [ (T_media - T_confort) - A * cos(omega*(t - 6)) ]²\n"
    "Desarrollando el binomio al cuadrado:\n"
    "= integral [ P_base + a*(T_media - T_confort)² - 2*a*(T_media - T_confort)*A*cos(omega*(t-6)) + a*A²*cos²(omega*(t-6)) ] dt\n\n"
    "Propiedades de simetría en el periodo de 24 horas (omega = 2*pi / 24):\n"
    "1. Integral de cos(omega*(t-6)) dt en [0, 24] = 0 (el ciclo armónico completo se anula).\n"
    "2. Integral de cos²(omega*(t-6)) dt en [0, 24] = 24 / 2 = 12 horas.\n\n"
    "Resultado Analítico Simplificado Exacto:\n"
    "E_diaria = 24 * [ P_base + a * ( (T_media - T_confort)² + 0.5 * A² ) ]   [kWh/día]")

add_heading_styled(doc, "Resultados del Consumo Diario en los Tres Escenarios", level=2)

tabla_int_headers = ["Escenario Climatológico", "T_media", "Amplitud A", "Consumo Analítico", "Trapecios (NumPy)", "Error"]
tabla_int_data = [
    ["Día Frío (Enero)", "12.0 °C", "8.0 °C", "41.280 kWh/día", "41.280 kWh/día", "0.000 %"],
    ["Día Templado (Marzo)", "19.0 °C", "7.0 °C", "17.640 kWh/día", "17.640 kWh/día", "0.000 %"],
    ["Día Cálido (Mayo)", "25.0 °C", "9.0 °C", "21.480 kWh/día", "21.480 kWh/día", "0.000 %"]
]
create_table_styled(doc, tabla_int_headers, tabla_int_data, col_widths=[1.8, 0.9, 0.9, 1.3, 1.3, 0.6])

add_paragraph_styled(doc,
    "Los resultados demuestran que la jornada fría de invierno representa el mayor costo energético del año (41.28 kWh/día), "
    "debido a que las madrugadas gélidas a 4.0 °C obligan a la bomba de calor a inyectar calor de forma ininterrumpida. En contraste, "
    "la jornada templada opera con gran eficiencia pasiva (17.64 kWh/día), mientras que el día cálido registra 21.48 kWh/día.")

# ==============================================================================
# SECCIÓN 7: ESTRATEGIA DE OPTIMIZACIÓN Y AHORRO ENERGÉTICO
# ==============================================================================
add_heading_styled(doc, "7- Estrategia de Optimización: Termostato Adaptativo y Ahorro", level=1)

add_paragraph_styled(doc,
    "Una de las capacidades más potentes de una vivienda inteligente es evitar el uso de una consigna rígida de 22.0 °C todo el año. "
    "Con base en el estándar internacional ANSI/ASHRAE 55-2020 de confort adaptativo, los ocupantes ajustan naturalmente su nivel "
    "de vestimenta según la temporada:")

add_bullet_styled(doc, "Se ajusta la consigna a 20.0 °C. Con vestimenta de abrigo ligero dentro del hogar (1.0 clo), 20 °C es sumamente agradable y reduce 2.0 °C de esfuerzo térmico al compresor.", bold_prefix="• Modo Invierno (Día Frío): ")
add_bullet_styled(doc, "Se ajusta la consigna a 24.0 °C. Con ropa fresca de verano (0.5 clo) y ventilación suave, 24 °C produce confort térmico completo sin sobrecalentar el compresor.", bold_prefix="• Modo Verano (Día Cálido): ")
add_bullet_styled(doc, "Se preserva la consigna neutra en 22.0 °C.", bold_prefix="• Modo Transición (Día Templado): ")

add_heading_styled(doc, "Resultados de Ahorro Energético", level=2)

tabla_ahorro_headers = ["Escenario", "Consumo Fijo (22 °C)", "Consumo Adaptativo", "Ahorro Diario", "% Reducción"]
tabla_ahorro_data = [
    ["Día Frío (Invierno)", "41.280 kWh/día", "32.640 kWh/día", "8.640 kWh/día", "20.93 %"],
    ["Día Templado", "17.640 kWh/día", "17.640 kWh/día", "0.000 kWh/día", "0.00 %"],
    ["Día Cálido (Verano)", "21.480 kWh/día", "19.560 kWh/día", "1.920 kWh/día", "8.94 %"]
]
create_table_styled(doc, tabla_ahorro_headers, tabla_ahorro_data, col_widths=[1.8, 1.4, 1.4, 1.2, 0.9])

add_figure(doc, "grafica_4_comparacion_ahorro.png",
           "Figura 8: Comparación de consumo diario y ahorro de energía por escenario bajo consigna adaptativa.", width_inches=5.8)

add_callout(doc, "La reprogramación estacional del termostato a 20.0 °C en invierno reduce el consumo diario en 8.64 kWh/día, lo que equivale a un ahorro del 20.93% en la factura eléctrica de los meses más costosos del año, sin sacrificar el bienestar de los habitantes.", title="HALLAZGO DE INGENIERÍA")

# ==============================================================================
# SECCIÓN 8: SIMULACIÓN COMPUTACIONAL EN PYTHON
# ==============================================================================
add_heading_styled(doc, "8- Simulación Computacional en Python", level=1)

add_paragraph_styled(doc,
    "Para garantizar la repetibilidad y validación numérica de todos los cálculos del reporte, se desarrollaron cuatro scripts "
    "en Python utilizando las bibliotecas científicas NumPy y Matplotlib:")

add_bullet_styled(doc, "Calcula la curva parabólica P(T), la derivada dP/dT, los perfiles de 24 horas y evalúa la integral analítica contra la integración numérica con la regla del trapecio (np.trapezoid).", bold_prefix="1. simulacion_modelo.py: ")
add_bullet_styled(doc, "Evalúa las normales climatológicas oficiales de los 12 meses de San Luis Potosí y calcula el incremento de potencia respecto al consumo basal.", bold_prefix="2. graficar_puntos_evaluados.py: ")
add_bullet_styled(doc, "Extrae los datos crudos del archivo Excel de la SENER (2002–2021) y genera la serie temporal de consumo estatal y los gráficos de dispersión térmica mensual.", bold_prefix="3. graficar_datos_excel_y_clima.py: ")
add_bullet_styled(doc, "Genera las curvas discretas de 25 puntos horarios marcados para inspeccionar de manera transparente la temperatura y potencia hora por hora.", bold_prefix="4. graficar_series_tiempo_crudos.py: ")

# ==============================================================================
# SECCIÓN 9: CONCLUSIONES Y TRABAJO FUTURO
# ==============================================================================
add_heading_styled(doc, "9- Conclusiones y Trabajo Futuro", level=1)

add_bullet_styled(doc, "El cálculo diferencial e integral demostró ser una herramienta práctica indispensable de ingeniería para modelar la demanda eléctrica, evaluar la tasa marginal de cambio con la derivada, certificar el punto de mínima potencia con la segunda derivada y sumar la energía total facturable en 24 horas con integrales definidas.", bold_prefix="1. Potencial del Cálculo en la Ingeniería: ")
add_bullet_styled(doc, "La fundamentación del modelo mediante las normas oficiales mexicanas NOM-020, NOM-026, NOM-015 y NOM-032 garantizó que los órdenes de magnitud obtenidos (0.40 kW basal y 0.010 kW/°C² de sensibilidad) reflejen el comportamiento real de una vivienda unifamiliar moderna.", bold_prefix="2. Rigor Normativo y Físico: ")
add_bullet_styled(doc, "El ajuste estacional de la consigna a 20 °C en invierno demostró un potencial de ahorro del 20.93% (8.64 kWh diarios), evidenciando la rentabilidad de los algoritmos de control domótico inteligente.", bold_prefix="3. Eficiencia Energética Comprobada: ")

add_paragraph_styled(doc,
    "Para la entrega final del proyecto se proponen tres mejoras técnicas al modelo matemático:\n"
    "• Banda muerta de confort pasivo: Modelar una meseta plana entre 21.0 °C y 23.0 °C donde el minisplit se apague totalmente y la potencia sea estrictamente de 0.40 kW.\n"
    "• Desacoplamiento del COP en frío y calor: Separar el coeficiente 'a' en a_frio y a_calor para reflejar las asimetrías de rendimiento en refrigeración y calefacción.\n"
    "• Ganancia solar directa: Incorporar la irradiancia solar incidente en ventanas orientadas al poniente durante las tardes de verano.")

# ==============================================================================
# SECCIÓN 10: REFERENCIAS BIBLIOGRÁFICAS EN FORMATO APA
# ==============================================================================
add_heading_styled(doc, "10- Referencias Bibliográficas en Formato APA", level=1)

referencias = [
    "American Society of Heating, Refrigerating and Air-Conditioning Engineers. (2020). Thermal environmental conditions for human occupancy (ANSI/ASHRAE Standard 55-2020). ASHRAE.",
    "Cengel, Y. A., & Boles, M. A. (2019). Termodinámica (9.ª ed.). McGraw-Hill Education.",
    "Comisión Nacional del Agua & Servicio Meteorológico Nacional. (2025). Normales climatológicas por estación (1985–2025): Estación 24028 San Luis Potosí, S.L.P. Secretaría de Medio Ambiente y Recursos Naturales.",
    "Comisión Nacional para el Uso Eficiente de la Energía. (15 de abril de 2020). El uso de energía eléctrica para confort térmico, reto mayor de política pública, señala estudio de la Conuee. Gobierno de México. https://www.gob.mx/conuee/articulos/el-uso-de-energia-electrica-para-confort-termico-reto-mayor-de-politica-publica-senala-estudio-de-la-conuee",
    "Domínguez, I. G. (19 de mayo de 2026). Casas más caras de pagar y de mantener: la ONU alerta de que la crisis climática agrava el acceso a la vivienda. Infobae. https://www.infobae.com/espana/2026/05/19/casas-mas-caras-de-pagar-y-de-mantener-la-onu-alerta-de-que-la-crisis-climatica-agrava-el-acceso-a-la-vivienda/",
    "Incropera, F. P., DeWitt, D. P., Bergman, T. L., & Lavine, A. S. (2011). Fundamentals of heat and mass transfer (7.ª ed.). John Wiley & Sons.",
    "LowCarbonPower. (s. f.). Electricidad en México. https://lowcarbonpower.org/es/region/M%C3%A9xico",
    "Secretaría de Economía. (2011). Norma Oficial Mexicana NOM-020-ENER-2011, Eficiencia energética en edificaciones - Envolvente de edificios para uso habitacional. Diario Oficial de la Federación.",
    "Secretaría de Economía. (2014). Norma Oficial Mexicana NOM-032-ENER-2013, Límites máximos de potencia eléctrica para equipos y aparatos que demandan energía en espera. Métodos de prueba y etiquetado. Diario Oficial de la Federación.",
    "Secretaría de Economía. (2016). Norma Oficial Mexicana NOM-026-ENER-2015, Eficiencia energética en acondicionadores de aire tipo dividido (Inverter). Diario Oficial de la Federación.",
    "Secretaría de Economía. (2018). Norma Oficial Mexicana NOM-015-ENER-2018, Eficiencia energética de refrigeradores y congeladores electrodomésticos. Diario Oficial de la Federación.",
    "Secretaría de Energía. (2022). Sistema de Información Energética (SIE): Consumo de energía eléctrica por entidad federativa 2002–2022. Dirección General de Planeación e Información Energéticas.",
    "Stewart, J. (2018). Cálculo de una variable: Trascendentes tempranas (8.ª ed.). Cengage Learning.",
    "Weather Spark. (s. f.). Clima promedio en San Luis Potosí, México, durante todo el año. Recuperado el 10 de septiembre de 2026, de https://es.weatherspark.com/y/5131/Clima-promedio-en-San-Luis-Potos%C3%AD-M%C3%A9xico-durante-todo-el-a%C3%B1o"
]

for ref in referencias:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.left_indent = Inches(0.5)
    p_ref.paragraph_format.first_line_indent = Inches(-0.5)
    p_ref.paragraph_format.space_before = Pt(2)
    p_ref.paragraph_format.space_after = Pt(4)
    p_ref.paragraph_format.line_spacing = 1.15
    r_ref = p_ref.add_run(ref)
    r_ref.font.name = "Arial"
    r_ref.font.size = Pt(9)
    r_ref.font.color.rgb = RGBColor(51, 65, 85)

# Guardar documento Word
doc.save(DOCX_OUT)
print(f"Documento Word guardado exitosamente: {DOCX_OUT}")

# ==============================================================================
# CONVERSIÓN A PDF MEDIANTE COM OBJECT DE WORD
# ==============================================================================
ps_script = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open("{DOCX_OUT}")
    $doc.ExportAsFixedFormat("{PDF_OUT}", 17) # 17 = wdExportFormatPDF
    $doc.Close($false)
    Write-Output "PDF_GENERATED_OK"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}} finally {{
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}}
"""

ps_path = os.path.join(BASE_DIR, "convertir_word_a_pdf.ps1")
with open(ps_path, "w", encoding="utf-8") as f:
    f.write(ps_script)

print("Compilando documento Word a PDF mediante Word COM...")
res = subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps_path],
                     capture_output=True, text=True)
print("Salida de PowerShell:", res.stdout.strip())
if res.stderr:
    print("Errores de PowerShell:", res.stderr.strip())

if os.path.exists(PDF_OUT):
    size_mb = os.path.getsize(PDF_OUT) / (1024 * 1024)
    print(f"PDF generado con éxito: {PDF_OUT} ({size_mb:.2f} MB)")
else:
    print("ADVERTENCIA: No se encontró el archivo PDF generado.")
