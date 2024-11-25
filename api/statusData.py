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
    humidity: float
    solidHumidity: float
    illuminance: float
    co2Concentration: float
    waterTemperature: float
    recorded_at: datetime



@router.post("/get_env/{_crop_id}", status_code=status.HTTP_200_OK)
async def getNewEnvStatus(EnvStatusSchema: EnvStatusSchema, _crop_id: int, db: Session = Depends(get_db)):
    crop = db.query(CropModel).filter(CropModel.id == _crop_id).first()
    if not crop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    last_env_status = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == _crop_id)\
        .order_by(EnvironmentStatusModel.recorded_at.desc()).first()

    temperature = EnvStatusSchema.temperature if EnvStatusSchema.temperature is not None else (last_env_status.temperature if last_env_status else 0)
    humidity = EnvStatusSchema.humidity if EnvStatusSchema.humidity is not None else (last_env_status.humidity if last_env_status else 0)
    solid_humidity = EnvStatusSchema.solidHumidity if EnvStatusSchema.solidHumidity is not None else (last_env_status.solidHumidity if last_env_status else 0)
    illuminance = EnvStatusSchema.illuminance if EnvStatusSchema.illuminance is not None else (last_env_status.illuminance if last_env_status else 0)
    co2_concentration = EnvStatusSchema.co2Concentration if EnvStatusSchema.co2Concentration is not None else (last_env_status.co2Concentration if last_env_status else 0)
    water_temperature = EnvStatusSchema.waterTemperature if EnvStatusSchema.waterTemperature is not None else (last_env_status.waterTemperature if last_env_status else 0)

    try:
        newEnv = EnvironmentStatusModel(
            temperature=temperature,
            humidity=humidity,
            solidHumidity=solid_humidity,
            illuminance=illuminance,
            co2Concentration=co2_concentration,
            waterTemperature=water_temperature,
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