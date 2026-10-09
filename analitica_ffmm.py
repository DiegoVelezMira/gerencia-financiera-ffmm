import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class DetectorAnomaliasFFMM:
    def __init__(self, contamination=0.06, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
        self.features = ['Monto_CDP_COP', 'Dias_CDP_a_CRP', 'Ratio_CRP_CDP', 'Ratio_Obligado_CRP']

    def preparar_features(self, df):
        data = df.copy()
        if 'Ratio_CRP_CDP' not in data.columns:
            data['Ratio_CRP_CDP'] = data['Monto_CRP_COP'] / data['Monto_CDP_COP'].replace(0, np.nan)
        if 'Ratio_Obligado_CRP' not in data.columns:
            data['Ratio_Obligado_CRP'] = data['Monto_Obligado_COP'] / data['Monto_CRP_COP'].replace(0, np.nan)
        
        data[self.features] = data[self.features].fillna(0)
        return data

    def fit_predict(self, df):
        data = self.preparar_features(df)
        X = data[self.features]
        
        data['Anomaly_Score'] = self.model.fit_predict(X)
        data['Es_Anomalia_ML'] = data['Anomaly_Score'] == -1
        
        def aplicar_reglas(row):
            reglas = []
            if row['Monto_CDP_COP'] > 50000000000:
                reglas.append("Monto Atípico Excesivo (>50.000M)")
            if row['Dias_CDP_a_CRP'] > 120:
                reglas.append("Retraso Severo en Contratación (>120 días)")
            if row['Ratio_Obligado_CRP'] < 0.25 and row['Dias_CDP_a_CRP'] > 20:
                reglas.append("Subejecución de Caja (Obligado < 25%)")
            return " | ".join(reglas) if reglas else "Cumple Parámetros"

        data['Diagnostico_Regla_Negocio'] = data.apply(aplicar_reglas, axis=1)
        data['Alerta_Final'] = data['Es_Anomalia_ML'] | (data['Diagnostico_Regla_Negocio'] != "Cumple Parámetros")
        return data


class MotorCalceLiquidez:
    def __init__(self, df_calce, df_portafolio):
        self.df_calce = df_calce.copy()
        self.df_portafolio = df_portafolio.copy()

    def calcular_rendimiento_total(self):
        total_invertido = self.df_portafolio['Monto_Invertido_COP'].sum()
        rendimiento_total = self.df_portafolio['Rendimiento_Anual_COP'].sum()
        tasa_ponderada = (self.df_portafolio['Monto_Invertido_COP'] * self.df_portafolio['Tasa_Rendimiento_EA']).sum() / total_invertido
        
        return {
            'Total_Invertido_COP': total_invertido,
            'Rendimiento_Anual_Est_COP': rendimiento_total,
            'Tasa_Ponderada_EA': tasa_ponderada
        }

    def evaluar_brechas_mes_a_mes(self):
        df = self.df_calce.copy()
        df['Deficit_COP_M'] = df['Brecha_Liquidez_COP_M'].apply(lambda x: abs(x) if x < 0 else 0)
        df['Superavit_COP_M'] = df['Brecha_Liquidez_COP_M'].apply(lambda x: x if x > 0 else 0)
        
        total_deficit = df['Deficit_COP_M'].sum()
        total_superavit = df['Superavit_COP_M'].sum()
        
        return df, {
            'Total_Deficit_Acumulado_M': total_deficit,
            'Total_Superavit_Acumulado_M': total_superavit,
            'Estado_Global_Calce': 'Calzado con Rebalanceo' if total_superavit >= total_deficit else 'Riesgo Liquidez'
        }
