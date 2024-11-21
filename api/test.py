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

router = APIRouter(tags=["재배 환경 API"])

templates = Jinja2Templates(directory="./templates")

class Crop(BaseModel):
    name: str

class EnvironmentStatus(BaseModel):
    temperature: float
    humidity: float
    solidHumidity: float
    illuminance: float
    co2Concentration: float
    recorded_at: datetime




# 아두이노에서 상태 전송하면 데이터 입력하는 api
@router.post("/record/{crop_name}", status_code=status.HTTP_201_CREATED)
async def recordEnvironmentStatus(
    crop_name: str, environmentStatusSchema: EnvironmentStatus, db: Session = Depends(get_db)
):
    crop = db.query(CropModel).filter(CropModel.name == crop_name).first()

    if not crop:
        crop = CropModel(name=crop_name)
        db.add(crop)
        db.commit()
        db.refresh(crop)

    if not environmentStatusSchema:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    try:
        newRecord = EnvironmentStatusModel(
            temperature=environmentStatusSchema.temperature,
            humidity=environmentStatusSchema.humidity,
            solidHumidity=environmentStatusSchema.solidHumidity,
            illuminance=environmentStatusSchema.illuminance,
            co2Concentration=environmentStatusSchema.co2Concentration,
            recorded_at=datetime.now(),
            crop_id=crop.id,
        )
        db.add(newRecord)
        db.commit()
        db.refresh(newRecord)
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JSONResponse(
        content={
            "temperature": newRecord.temperature,
            "humidity": newRecord.humidity,
            "solidHumidity": newRecord.solidHumidity,
            "illuminance": newRecord.illuminance,
            "co2Concentration": newRecord.co2Concentration,
            "recorded_at": newRecord.recorded_at.strftime("%Y-%m-%d %H:%M"),
            "crop_name": crop.name,
        }
    )

# 현재까지의 상태로 그래프 이미지로 반환하는 api
@router.get("/graph", response_class=StreamingResponse)
async def loadEnvironmentGraph(db : Session=Depends(get_db)):
    records = db.query(EnvironmentStatusModel).all()

    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    timestamp = [record.recorded_at for record in records]

    temperature = [record.temperature for record in records]
    humidity = [record.humidity for record in records]
    illuminance = [record.illuminance for record in records]
    solidHumidity = [record.solidHumidity for record in records]
    co2Concentration = [record.co2Concentration for record in records]
    

    plt.figure(figsize=(10, 5))
    plt.plot(timestamp, temperature, label='Temperature (°C)', color='#EA1717')
    plt.plot(timestamp, humidity, label='Humidity (%)', color='#657AED')
    plt.plot(timestamp, illuminance, label='illuminance (lux)', color='#FFEB52')
    plt.plot(timestamp, solidHumidity, label='solidHumidity (%)', color='#856113')
    plt.plot(timestamp, co2Concentration, label='co2Concentration (ppm)', color='#0C9B43')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Environmental Status Change Trend')
    plt.legend()
    plt.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    plt.close()

    return StreamingResponse(buf, media_type='image/png')









