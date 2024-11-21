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

router = APIRouter(tags=["작물 등록 API"])

class CropSchema(BaseModel):
    name: str
    nickname: str
    set_temperature: float
    set_humidity: float
    set_solidHumidity: float
    set_illuminance: float
    set_co2Concentration: float
    set_waterTemperature: float
    # created_at: datetime

class UpdateCropSchema(BaseModel):
    set_temperature: float
    set_humidity: float
    set_solidHumidity: float
    set_illuminance: float
    set_co2Concentration: float
    set_waterTemperature: float


@router.post("/create_new", status_code=status.HTTP_201_CREATED)
async def createNewCrop(CropSchema: CropSchema, db: Session=Depends(get_db)):
    try:
        crop = CropModel(
            name=CropSchema.name,
            nickname=CropSchema.nickname,
            set_temperature=CropSchema.set_temperature,
            set_humidity=CropSchema.set_humidity,
            set_solidHumidity=CropSchema.set_solidHumidity,
            set_illuminance=CropSchema.set_illuminance,
            set_co2Concentration=CropSchema.set_co2Concentration,
            set_waterTemperature=CropSchema.set_waterTemperature,
            created_at=datetime.now()
        )
        db.add(crop)
        db.commit()
        db.refresh(crop)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(
        content={
            "name": crop.name,
            "nickname": crop.nickname,
            "set_temperature": crop.set_temperature,
            "set_humidity": crop.set_humidity,
            "set_solidHumidity": crop.set_solidHumidity,
            "set_illuminance": crop.set_illuminance,
            "set_co2Concentration": crop.set_co2Concentration,
            "set_waterTemperature": crop.set_waterTemperature,
            "created_at": crop.created_at.strftime("%Y-%m-%d %H:%M"),
        }
    )

@router.put("/update_status/{crop_id}", status_code=status.HTTP_200_OK)
async def updateCropStatus(UpdateCropSchema: UpdateCropSchema, crop_id: int, db: Session=Depends(get_db)):
    crop = db.query(CropModel).filter(CropModel.id == crop_id).first()

    if crop:
        for key, value in UpdateCropSchema.model_dump(exclude_unset=True).items():
            setattr(crop, key, value)
        # crop.set_temperature=UpdateCropSchema.set_temperature
        # crop.set_humidity=UpdateCropSchema.set_humidity
        # crop.set_solidHumidity=UpdateCropSchema.set_solidHumidity
        # crop.set_illuminance=UpdateCropSchema.set_illuminance
        # crop.set_co2Concentration=UpdateCropSchema.set_co2Concentration
        # crop.set_waterTemperature=UpdateCropSchema.set_waterTemperature
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.commit()
    db.refresh(crop)
    return JSONResponse(
        content={
            "name": crop.name,
            "nickname": crop.nickname,
            "set_temperature": crop.set_temperature,
            "set_humidity": crop.set_humidity,
            "set_solidHumidity": crop.set_solidHumidity,
            "set_illuminance": crop.set_illuminance,
            "set_co2Concentration": crop.set_co2Concentration,
            "set_waterTemperature": crop.set_waterTemperature,
            "created_at": crop.created_at.strftime("%Y-%m-%d %H:%M"),
        }
    )
