import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime

from ..models.coating_data import CoatingData

class AnalysisService:
    def calculate_spc(
        self,
        db: Session,
        param_type: str,
        start_time: datetime,
        end_time: datetime
    ) -> Dict:
        """计算SPC控制图数据"""
        # 查询数据
        query = db.query(CoatingData)
        query = query.filter(CoatingData.timestamp.between(start_time, end_time))
        data = query.all()
        
        # 获取目标参数数据
        values = [getattr(item, param_type) for item in data]
        
        # 计算控制限
        mean = np.mean(values)
        std = np.std(values)
        ucl = mean + 3 * std
        lcl = mean - 3 * std
        
        # 计算过程能力指数
        usl = self.get_spec_limit(param_type, 'upper')
        lsl = self.get_spec_limit(param_type, 'lower')
        
        cp = (usl - lsl) / (6 * std)
        cpu = (usl - mean) / (3 * std)
        cpl = (mean - lsl) / (3 * std)
        cpk = min(cpu, cpl)
        
        return {
            'data': values,
            'ucl': ucl,
            'lcl': lcl,
            'cl': mean,
            'cp': cp,
            'cpk': cpk
        }

    def calculate_correlation(self, db: Session) -> Dict:
        """计算参数相关性"""
        # 查询数据
        data = db.query(CoatingData).all()
        
        # 准备数据框
        df = pd.DataFrame([{
            'temperature': item.temperature,
            'humidity': item.humidity,
            'viscosity': item.viscosity,
            'wind_speed': item.wind_speed,
            'voltage': item.voltage,
            'film_thickness': item.film_thickness,
            'doi': item.doi,
            'gloss': item.gloss,
            'color_diff': item.eab15
        } for item in data])
        
        # 计算相关系数矩阵
        corr_matrix = df.corr()
        
        # 转换为前端需要的格式
        result = []
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.index)):
                result.append([i, j, float(corr_matrix.iloc[i, j])])
                
        return {
            'correlation_data': result,
            'x_labels': list(corr_matrix.columns),
            'y_labels': list(corr_matrix.index)
        }

    def get_spec_limit(self, param_type: str, limit_type: str) -> float:
        """获取参数规格限"""
        spec_limits = {
            'film_thickness': {'upper': 30, 'lower': 20},
            'doi': {'upper': 100, 'lower': 80},
            'gloss': {'upper': 95, 'lower': 85}
        }
        return spec_limits.get(param_type, {}).get(limit_type, 0)

analysis_service = AnalysisService() 