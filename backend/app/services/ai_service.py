import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List

class AIService:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, training_data: List[Dict]):
        """训练AI模型"""
        # 准备训练数据
        X = []  # 输入特征：温度、湿度、粘度等
        y = []  # 输出目标：膜厚、光泽度等
        
        for data in training_data:
            features = [
                data['temperature'],
                data['humidity'],
                data['viscosity'],
                data['spray_distance'],
                data['spray_gun_speed']
            ]
            targets = [
                data['film_thickness'],
                data['gloss'],
                data['doi']
            ]
            X.append(features)
            y.append(targets)
        
        X = np.array(X)
        y = np.array(y)
        
        # 数据���准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 训练模型
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict_quality(self, params: Dict) -> Dict:
        """预测涂装质量"""
        if not self.is_trained:
            raise Exception("模型未训练")
            
        # 准备输入数据
        features = np.array([[
            params['temperature'],
            params['humidity'],
            params['viscosity'],
            params['spray_distance'],
            params['spray_gun_speed']
        ]])
        
        # 数据标准化
        features_scaled = self.scaler.transform(features)
        
        # 预测
        predictions = self.model.predict(features_scaled)[0]
        
        # 计算可信度（使用模型的预测概率）
        confidence = np.mean(self.model.predict_proba(features_scaled), axis=1)[0] * 100
        
        return {
            'thickness': float(predictions[0]),
            'gloss': float(predictions[1]),
            'doi': float(predictions[2]),
            'confidence': float(confidence)
        }

    def get_feature_importance(self) -> Dict:
        """获取特征重要性"""
        if not self.is_trained:
            raise Exception("模型未训练")
            
        feature_names = [
            'temperature',
            'humidity',
            'viscosity',
            'spray_distance',
            'spray_gun_speed'
        ]
        
        importance = self.model.feature_importances_
        return dict(zip(feature_names, importance))

ai_service = AIService() 