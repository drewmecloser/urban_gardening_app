from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import date

Base = declarative_base()

class Crop(Base):
    __tablename__ = 'crops'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    growing_season_days = Column(Integer)
    water_frequency_days = Column(Integer)

    planted_instances = relationship("PlantedCrop", back_populates="crop")

    def __repr__(self):
        return f"<Crop(name='{self.name}', growing_season_days={self.growing_season_days})>"

class GardenPlot(Base):
    __tablename__ = 'garden_plots'
    id = Column(Integer, primary_key=True)
    plot_name = Column(String(255), nullable=False, unique=True)
    location = Column(String(255))
    size_sq_ft = Column(Integer)

    planted_crops = relationship("PlantedCrop", back_populates="garden_plot")

    def __repr__(self):
        return f"<GardenPlot(plot_name='{self.plot_name}')>"

class PlantedCrop(Base):
    __tablename__ = 'planted_crops'
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=False)
    plot_id = Column(Integer, ForeignKey('garden_plots.id'), nullable=False)
    planting_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date)

    crop = relationship("Crop", back_populates="planted_instances")
    garden_plot = relationship("GardenPlot", back_populates="planted_crops")

    def __repr__(self):
        return f"<PlantedCrop(crop_id={self.crop_id}, plot_id={self.plot_id})>"