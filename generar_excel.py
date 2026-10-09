import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

os.makedirs('data', exist_ok=True)
np.random.seed(2026)

fuerzas = ['Ejército Nacional', 'Armada de Colombia', 'Fuerza Aérea Colombiana', 'Comando General FF.MM.']
unidades = {
    'Ejército Nacional': ['DIV01-StaMarta', 'DIV05-Bogota', 'DIV07-Medellin', 'COEJC-Central'],
    'Armada de Colombia': ['BN1-Cartagena', 'BN2-Buenaventura', 'BN4-Uraba', 'ARC-Central'],
    'Fuerza Aérea Colombiana': ['CATAAM-Bogota', 'CACOM1-Palanquero', 'CACOM5-Rionegro', 'FAC-Central'],
    'Comando General FF.MM.': ['COGFM-Central', 'CCOES-Caste', 'JEMCO-Bogota']
}

rubros_operativos = [
    ('2-01-01-01-002', 'Raciones de Campaña y Nutrición'),
    ('2-01-01-02-005', 'Mantenimiento y Repuestos Aeronaves'),
    ('2-01-01-02-008', 'Combustibles y Lubricantes para Flota'),
    ('2-01-01-02-012', 'Prendas de Vestir e Intendencia Militar'),
    ('2-02-02-01-003', 'Mantenimiento de Infraestructura de Bases'),
    ('1-01-01-01-001', 'Primas de Orden Público y Servicios'),
    ('2-03-01-01-005', 'Equipos de Comunicaciones y Ciberdefensa')
]

data_siif = []
fecha_inicio = datetime(2026, 1, 1)

for i in range(1, 301):
    fuerza = np.random.choice(fuerzas)
    unidad = np.random.choice(unidades[fuerza])
    rubro_cod, rubro_desc = rubros_operativos[np.random.randint(0, len(rubros_operativos))]
    
    monto_cdp = round(float(np.random.uniform(800, 18000) * 1e6), -6)
    dias_cdp_crp = int(np.random.randint(5, 40))
    ratio_crp = np.random.uniform(0.88, 1.0)
    ratio_obli = np.random.uniform(0.75, 1.0)
    
    es_anomalia = False
    tipo_anomalia = 'Normal'
    if np.random.rand() < 0.06:
        es_anomalia = True
        tipo_anomalia = np.random.choice(['Monto Atípico Excesivo', 'Retraso Extremo CRP', 'Subejecución Severa'])
        if tipo_anomalia == 'Monto Atípico Excesivo':
            monto_cdp = round(float(np.random.uniform(85000, 130000) * 1e6), -6)
        elif tipo_anomalia == 'Retraso Extremo CRP':
            dias_cdp_crp = int(np.random.randint(150, 270))
        elif tipo_anomalia == 'Subejecución Severa':
            ratio_obli = np.random.uniform(0.05, 0.22)

    monto_crp = round(monto_cdp * ratio_crp, -6)
    monto_obligado = round(monto_crp * ratio_obli, -6)
    monto_pagado = monto_obligado
    
    fecha_cdp = fecha_inicio + timedelta(days=int(np.random.randint(0, 240)))
    fecha_crp = fecha_cdp + timedelta(days=dias_cdp_crp)
    
    data_siif.append({
        'ID_Registro': f'REG-2026-{i:03d}',
        'Fecha_CDP': fecha_cdp.strftime('%Y-%m-%d'),
        'Fecha_CRP': fecha_crp.strftime('%Y-%m-%d'),
        'Fuerza': fuerza,
        'Unidad_Ejecutora': unidad,
        'Codigo_Rubro': rubro_cod,
        'Descripcion_Rubro': rubro_desc,
        'Fuente_Financiacion': 'Nación 11 (Crédito/Tesoro)',
        'Monto_CDP_COP': monto_cdp,
        'Monto_CRP_COP': monto_crp,
        'Monto_Obligado_COP': monto_obligado,
        'Monto_Pagado_COP': monto_pagado,
        'Dias_CDP_a_CRP': dias_cdp_crp,
        'Es_Anomalia_Inyectada': es_anomalia,
        'Tipo_Anomalia_Simulada': tipo_anomalia
    })

df_siif = pd.DataFrame(data_siif)

data_portafolio = [
    {'ID_Inversion': 'INV-2026-TES01', 'Instrumento': 'TES Clase B Tasa Fija 2028', 'Monto_Invertido_COP': 25000000000, 'Participacion_%': 0.50, 'Tasa_Rendimiento_EA': 0.105, 'Rendimiento_Anual_COP': 2625000000},
    {'ID_Inversion': 'INV-2026-CUN01', 'Instrumento': 'Cuenta Única Nacional Remunerada', 'Monto_Invertido_COP': 12500000000, 'Participacion_%': 0.25, 'Tasa_Rendimiento_EA': 0.090, 'Rendimiento_Anual_COP': 1125000000},
    {'ID_Inversion': 'INV-2026-FIC01', 'Instrumento': 'FIC Liquidez Vista AAA', 'Monto_Invertido_COP': 7500000000, 'Participacion_%': 0.15, 'Tasa_Rendimiento_EA': 0.092, 'Rendimiento_Anual_COP': 690000000},
    {'ID_Inversion': 'INV-2026-CDT01', 'Instrumento': 'CDT Bancario 180D Tasa Fija', 'Monto_Invertido_COP': 5000000000, 'Participacion_%': 0.10, 'Tasa_Rendimiento_EA': 0.097, 'Rendimiento_Anual_COP': 485000000}
]
df_portafolio = pd.DataFrame(data_portafolio)

meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
pac_exigibilidad = [2500, 2500, 2500, 1660, 1670, 1670, 4160, 4170, 4170, 8330, 8330, 8340]
vencimientos_inv = [3000, 2000, 2500, 2000, 1500, 1500, 5000, 3500, 4000, 10000, 7500, 7500]

df_calce = pd.DataFrame({
    'Mes_Vigencia': meses,
    'Exigibilidad_PAC_COP_M': pac_exigibilidad,
    'Vencimiento_Inversion_COP_M': vencimientos_inv,
    'Brecha_Liquidez_COP_M': np.array(vencimientos_inv) - np.array(pac_exigibilidad)
})

with pd.ExcelWriter('data/dataset_master_gerencia_ffmm.xlsx', engine='openpyxl') as writer:
    df_siif.to_excel(writer, sheet_name='Ejecucion_SIIF', index=False)
    df_portafolio.to_excel(writer, sheet_name='Portafolio_50kM', index=False)
    df_calce.to_excel(writer, sheet_name='Calce_Liquidez_PAC', index=False)

print("✅ Excel generado correctamente.")
