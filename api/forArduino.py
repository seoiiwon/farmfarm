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

router = APIRouter(tags=["아두이노를 위한 API"])

@router.get("/arduino/settingEnv{crop_id}")
async def settingEnv(crop_id: int, db: Session=Depends(get_db)):
    cropEnv = db.query(CropModel).filter(CropModel.id == crop_id).first()
    return {
        "id" : cropEnv.id,
        "set_temperature" : cropEnv.set_temperature,
        "set_humidity" : cropEnv.set_humidity,
        "set_solidHumidity" : cropEnv.set_solidHumidity,
        "set_illuminance" : cropEnv.set_illuminance,
        "set_co2Concentration" : cropEnv.set_co2Concentration,
        "set_waterTemperature" : cropEnv.set_waterTemperature,
        "created_at" : cropEnv.created_at
    }

class UpdateSubData(BaseModel):
    co2Concentration: float
    waterTemperature: float


@router.put("/arduino/sub/{crop_id}")
async def updateSubData(updateSchema: UpdateSubData, crop_id: int, db: Session=Depends(get_db)):
    currentEnv = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).order_by(EnvironmentStatusModel.recorded_at.desc()).first()  

    if currentEnv:
        currentEnv.co2Concentration = updateSchema.co2Concentration
        currentEnv.waterTemperature = updateSchema.waterTemperature
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.commit()
    db.refresh(currentEnv)
    return {"solidHumidity" : currentEnv.solidHumidity}    
        


