from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..database import get_db
from ..models.coating_data import CoatingData
from ..schemas import coating_schemas
from ..services import coating_service, analysis_service, ai_service

router = APIRouter()

# 数据管理相关接口
@router.get("/coating/data", response_model=List[coating_schemas.CoatingDataBase])
def get_coating_data(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    body_area: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return coating_service.get_coating_data(db, start_time, end_time, body_area, skip, limit)

@router.post("/coating/data", response_model=coating_schemas.CoatingDataBase)
def create_coating_data(
    data: coating_schemas.CoatingDataCreate,
    db: Session = Depends(get_db)
):
    return coating_service.create_coating_data(db, data)

# SPC分析相关接口
@router.get("/spc/analysis")
def get_spc_analysis(
    param_type: str,
    start_time: datetime,
    end_time: datetime,
    db: Session = Depends(get_db)
):
    return analysis_service.calculate_spc(db, param_type, start_time, end_time)

# 智能分析相关接口
@router.get("/analysis/correlation")
def get_correlation_analysis(
    db: Session = Depends(get_db)
):
    return analysis_service.calculate_correlation(db)

@router.post("/analysis/predict")
def predict_quality(
    params: coating_schemas.PredictionParams,
    db: Session = Depends(get_db)
):
    return ai_service.predict_quality(params)

# 实时监控相关接口
@router.get("/monitor/realtime")
def get_realtime_data(
    db: Session = Depends(get_db)
):
    return coating_service.get_latest_data(db) 