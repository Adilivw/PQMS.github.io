from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CoatingDataBase(BaseModel):
    timestamp: datetime
    body_area: str
    
    # 膜厚数据
    average_thickness: Optional[float]
    variance_thickness: Optional[float]
    cpk_thickness: Optional[float]
    film_thickness: Optional[float]
    
    # 外观数据
    doi: Optional[float]
    sw: Optional[float]
    lw: Optional[float]
    r_value: Optional[float]
    gloss: Optional[float]
    
    # 色差数据
    l15: Optional[float]
    a15: Optional[float]
    b15: Optional[float]
    eab15: Optional[float]
    
    # 设备参数
    spray_distance: Optional[float]
    spray_pattern: Optional[str]
    overlap_ratio: Optional[float]
    spray_gun_speed: Optional[float]
    paint_flow: Optional[float]
    air_flow1: Optional[float]
    air_flow2: Optional[float]
    rotating_speed: Optional[float]
    voltage: Optional[float]
    
    # 环境参数
    temperature: Optional[float]
    humidity: Optional[float]
    wind_speed: Optional[float]
    
    # 油漆参数
    viscosity: Optional[float]

    class Config:
        orm_mode = True

class CoatingDataCreate(CoatingDataBase):
    pass

class PredictionParams(BaseModel):
    temperature: float
    humidity: float
    viscosity: float
    spray_distance: float
    spray_gun_speed: float 