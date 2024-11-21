from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CoatingData(Base):
    __tablename__ = 'coating_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    body_area = Column(String(50), nullable=False)
    
    # 膜厚数据
    average_thickness = Column(Float)
    variance_thickness = Column(Float)
    cpk_thickness = Column(Float)
    film_thickness = Column(Float)
    
    # 外观数据
    doi = Column(Float)
    sw = Column(Float)
    lw = Column(Float)
    r_value = Column(Float)
    gloss = Column(Float)
    
    # 色差数据
    l15 = Column(Float)
    a15 = Column(Float)
    b15 = Column(Float)
    eab15 = Column(Float)
    # ... 其他色差数据
    
    # 设备参数
    spray_distance = Column(Float)
    spray_pattern = Column(String(50))
    overlap_ratio = Column(Float)
    spray_gun_speed = Column(Float)
    paint_flow = Column(Float)
    air_flow1 = Column(Float)
    air_flow2 = Column(Float)
    rotating_speed = Column(Float)
    voltage = Column(Float)
    
    # 环境参数
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    
    # 油漆参数
    viscosity = Column(Float) 