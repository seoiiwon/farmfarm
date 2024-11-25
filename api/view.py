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
import json

router = APIRouter(tags=["View API"])

templates = Jinja2Templates(directory="./templates")

def generateEnvironmentalGraphs(env):
    timestamp = [e.recorded_at for e in env]
    temperature = [e.temperature for e in env]
    humidity = [e.humidity for e in env]
    solidHumidity = [e.solidHumidity for e in env]
    illuminance = [e.illuminance for e in env]
    co2Concentration = [e.co2Concentration for e in env]
    waterTemperature = [e.waterTemperature for e in env]

    graphDict = {
        "temperature": temperature,
        "humidity": humidity,
        "solidHumidity": solidHumidity,
        "illuminance": illuminance,
        "co2Concentration": co2Concentration,
        "waterTemperature": waterTemperature
    }

    result = {}

    for key, values in graphDict.items():
        plt.figure(figsize=(10, 5))
        plt.plot(timestamp, values, label=key, color='#EA1717') 
        plt.xlabel('Timestamp')
        plt.ylabel('Values')
        plt.title(f'{key} Change Trend')
        plt.legend()
        plt.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()

        result[key] = img_data

    return result

def generateEnvironmentalTotalGraphs(env):
    timestamp = [e.recorded_at for e in env]
    temperature = [e.temperature for e in env]
    humidity = [e.humidity for e in env]
    solidHumidity = [e.solidHumidity for e in env]
    illuminance = [e.illuminance for e in env]
    co2Concentration = [e.co2Concentration for e in env]
    waterTemperature = [e.waterTemperature for e in env]
    plt.figure(figsize=(10, 8))
    plt.plot(timestamp, temperature, label='Temperature (°C)', color='#EA1717')
    plt.plot(timestamp, humidity, label='Humidity (%)', color='#657AED')
    plt.plot(timestamp, illuminance, label='illuminance (lux)', color='#FFEB52')
    plt.plot(timestamp, solidHumidity, label='solidHumidity (%)', color='#856113')
    plt.plot(timestamp, co2Concentration, label='co2Concentration (ppm)', color='#0C9B43')
    plt.plot(timestamp, waterTemperature, label="waterTemperature (%)", color="#121212")
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

    return img_data



@router.get("/{crop_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def loadMain(request: Request, crop_id: int, db: Session = Depends(get_db)):
    crops = db.query(CropModel).all()
    crop = db.query(CropModel).filter(CropModel.id == crop_id).first()
    currentEnv = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).first()
    env = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).order_by(EnvironmentStatusModel.recorded_at.desc()).limit(10).all()    

    graph_images = generateEnvironmentalGraphs(env)

    try:
        return templates.TemplateResponse(
            name="main.html", 
            context={
                "request": request,
                "crops": crops,
                "crop": crop,
                "currentEnv": currentEnv,
                "env": env,
                "graphs": json.dumps(graph_images), 
                "graphsForDisplay": graph_images,
            }
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@router.get("/status_all/{crop_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def loadAllStatus(crop_id: int, request: Request, db: Session=Depends(get_db)):
    currentEnv = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).order_by(EnvironmentStatusModel.recorded_at.desc()).first()
    env = db.query(EnvironmentStatusModel).filter(EnvironmentStatusModel.crop_id == crop_id).order_by(EnvironmentStatusModel.recorded_at.desc()).limit(10).all()    
    graph_image = generateEnvironmentalTotalGraphs(env)
    crop = db.query(CropModel).filter(CropModel.id == crop_id).first()

    try:
        return templates.TemplateResponse(
            name="allStatus.html", 
            context={
                "request": request,
                "graph_image": graph_image,
                "crop": crop,
                "currentEnv": currentEnv
            }
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/add_crop/{crop_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def loadAddCrop(crop_id: int, request: Request):
    try:
        return templates.TemplateResponse(name="addCrop.html", request=request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)