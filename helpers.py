from models import Crop, GardenPlot, PlantedCrop, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

engine = create_engine('sqlite:///gardening.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def create_database_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def find_or_create_crop(name, growing_days=None, water_freq=None):
    """Finds a crop by name or creates a new one if it doesn't exist."""
    crop = session.query(Crop).filter_by(name=name.title()).first()
    if not crop:
        if growing_days is None:
            raise ValueError("Growing season days are required for a new crop.")
        if water_freq is None:
            raise ValueError("Watering frequency is required for a new crop.")
            
        crop = Crop(name=name.title(), growing_season_days=growing_days, water_frequency_days=water_freq)
        session.add(crop)
        session.commit()
    return crop

def find_or_create_plot(plot_name, location=None, size_sq_ft=None):
    """Finds a garden plot by name or creates a new one."""
    garden_plot = session.query(GardenPlot).filter_by(plot_name=plot_name.title()).first()
    if not garden_plot:
        if location is None or size_sq_ft is None:
            raise ValueError("Location and size are required for a new garden plot.")
            
        garden_plot = GardenPlot(plot_name=plot_name.title(), location=location, size_sq_ft=size_sq_ft)
        session.add(garden_plot)
        session.commit()
    return garden_plot

def add_planted_crop(crop, garden_plot, planting_date):
    """Adds a new planted crop to the database."""
    expected_harvest = None
    if crop.growing_season_days:
        expected_harvest = planting_date + timedelta(days=crop.growing_season_days)
    
    new_plant = PlantedCrop(
        crop=crop,
        garden_plot=garden_plot,
        planting_date=planting_date,
        expected_harvest_date=expected_harvest
    )
    session.add(new_plant)
    session.commit()
    return new_plant

def get_all_planted_crops():
    """Retrieves all planted crops from the database."""
    return session.query(PlantedCrop).all()

def find_planted_crop_by_id(plant_id):
    """Finds a planted crop by its ID."""
    return session.query(PlantedCrop).filter_by(id=plant_id).first()

def delete_planted_crop(plant_id):
    """Deletes a planted crop by its ID."""
    plant_to_harvest = find_planted_crop_by_id(plant_id)
    if plant_to_harvest:
        session.delete(plant_to_harvest)
        session.commit()
        return True
    return False

def get_all_crops():
    """Retrieves all available crops."""
    return session.query(Crop).all()

def get_all_plots():
    """Retrieves all available garden plots."""
    return session.query(GardenPlot).all()