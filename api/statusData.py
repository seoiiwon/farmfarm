from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from pydantic import BaseModel
from datetime import datetime
from models.models import Crop as CropModel, EnvironmentStatus as EnvironmentStatusModel
import matplotlib.pyplot as plt
import io

router = APIRouter(tags=["작물 상태 API"])

class EnvStatusSchema(BaseModel):
    crop_id: int
    temperature: float
    humidity: int
    solidHumidity: float
    illuminance: float
    co2Concentration: float
    waterTemperature: float
    recorded_at: datetime

@router.post("/get_env/{_crop_id}", status_code=status.HTTP_200_OK)
async def getNewEnvStatus(EnvStatusSchema: EnvStatusSchema, _crop_id: int, db: Session=Depends(get_db)):
    # crop_id가 존재하는지 확인
    crop = db.query(CropModel).filter(CropModel.id == _crop_id).first()
    if not crop:
        # crop_id가 유효하지 않으면 404 에러 발생
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    try:
        newEnv = EnvironmentStatusModel(
            temperature=EnvStatusSchema.temperature,
            humidity=EnvStatusSchema.humidity,
            solidHumidity=EnvStatusSchema.solidHumidity,
            illuminance=EnvStatusSchema.illuminance,
            co2Concentration=EnvStatusSchema.co2Concentration,
            waterTemperature=EnvStatusSchema.waterTemperature,
            recorded_at=datetime.now(),
            crop_id=_crop_id
        )
        db.add(newEnv)
        db.commit()
        db.refresh(newEnv)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return JSONResponse(
        content={
            "id": newEnv.id,
            "crop_id": newEnv.crop_id,
            "temperature": newEnv.temperature,
            "humidity": newEnv.humidity,
            "solidHumidity": newEnv.solidHumidity,
            "illuminance": newEnv.illuminance,
            "co2Concentration": newEnv.co2Concentration,
            "waterTemperature": newEnv.waterTemperature,
            "recorded_at": newEnv.recorded_at.strftime("%Y-%m-%d %H:%M"),
        }
    )