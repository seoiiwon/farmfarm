from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    set_temperature = Column(Float, nullable=False)  # 온도
    set_humidity = Column(Float, nullable=False)     # 습도
    set_solidHumidity = Column(Float, nullable=False)  # 지습
    set_illuminance = Column(Float, nullable=False)  # 조도
    set_co2Concentration = Column(Float, nullable=False)  # CO2 농도
    set_waterTemperature = Column(Float, nullable=False) # 수온
    created_at = Column(DateTime, nullable=False)
    environment_status = relationship("EnvironmentStatus", back_populates="crop")

class EnvironmentStatus(Base):
    __tablename__ = "environment_status"  

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    temperature = Column(Float, nullable=False)  # 온도
    humidity = Column(Float, nullable=False)     # 습도
    solidHumidity = Column(Float, nullable=False)  # 지습
    illuminance = Column(Float, nullable=False)  # 조도
    co2Concentration = Column(Float, nullable=False)  # CO2 농도
    waterTemperature = Column(Float, nullable=False) # 수온
    recorded_at = Column(DateTime, nullable=False)

    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=False)
    crop = relationship("Crop", back_populates="environment_status")
    