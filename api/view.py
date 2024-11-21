from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from config.database import get_db
from models.models import Crop as CropModel, EnvironmentStatus as EnvironmentStatusModel
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter(tags=["View API"])

templates = Jinja2Templates(directory="./templates")


@router.get("/{crop_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def loadMain(request: Request, crop_id: int, db: Session = Depends(get_db)):
    crops = db.query(CropModel).all()
    crop = db.query(CropModel).filter(CropModel.id == crop_id).first()
    currentEnv = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).first()
    env = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).order_by(EnvironmentStatusModel.recorded_at.desc()).limit(10).all()    

    timestamp = [e.recorded_at for e in env]
    temperature = [e.temperature for e in env]
    
    plt.figure(figsize=(10, 5))
    plt.plot(timestamp, temperature, label='Temperature (°C)', color='#EA1717')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.title('Environmental Status Change Trend')
    plt.legend()
    plt.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    try:
        return templates.TemplateResponse(
            name="main.html", 
            context={
                "request": request,
                "crops": crops,
                "crop": crop,
                "currentEnv": currentEnv,
                "env": env,
                "temperature_graph": img_data
            }
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.get("/status_all", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def loadAllStatus(request: Request):
    try:
        return templates.TemplateResponse(name="allStatus.html", request=request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/add_crop", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def loadAddCrop(request: Request):
    try:
        return templates.TemplateResponse(name="addCrop.html", request=request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def createGraph(envList: list):
    if not envList:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    timestamp = [envList]




# # 현재까지의 상태로 그래프 이미지로 반환하는 api
# @router.get("/graph", response_class=StreamingResponse)
# async def loadEnvironmentGraph(db : Session=Depends(get_db)):
#     records = db.query(EnvironmentStatusModel).all()

#     if not records:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
#     timestamp = [record.recorded_at for record in records]

#     temperature = [record.temperature for record in records]
#     humidity = [record.humidity for record in records]
#     illuminance = [record.illuminance for record in records]
#     solidHumidity = [record.solidHumidity for record in records]
#     co2Concentration = [record.co2Concentration for record in records]
    

#     plt.figure(figsize=(10, 5))
#     plt.plot(timestamp, temperature, label='Temperature (°C)', color='#EA1717')
#     plt.plot(timestamp, humidity, label='Humidity (%)', color='#657AED')
#     plt.plot(timestamp, illuminance, label='illuminance (lux)', color='#FFEB52')
#     plt.plot(timestamp, solidHumidity, label='solidHumidity (%)', color='#856113')
#     plt.plot(timestamp, co2Concentration, label='co2Concentration (ppm)', color='#0C9B43')
#     plt.xlabel('Timestamp')
#     plt.ylabel('Values')
#     plt.title('Environmental Status Change Trend')
#     plt.legend()
#     plt.grid()

#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)

#     plt.close()

#     return StreamingResponse(buf, media_type='image/png')

