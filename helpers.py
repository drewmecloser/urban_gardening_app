from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from models import Base, Crop, GardenPlot, PlantedCrop
from datetime import timedelta
import click

engine = create_engine('sqlite:///gardening.db')
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

# CRUD operations for the Crop table
def add_new_crop(name, growing_days, water_freq):
    session = get_session()
    try:
        new_crop = Crop(name=name, growing_season_days=growing_days, water_frequency_days=water_freq)
        session.add(new_crop)
        session.commit()
    finally:
        session.close()

def get_all_crops():
    session = get_session()
    try:
        crops = session.query(Crop).all()
        return crops
    finally:
        session.close()

def delete_crop_by_id(crop_id):
    session = get_session()
    try:
        crop = session.query(Crop).filter_by(id=crop_id).first()
        if crop:
            session.delete(crop)
            session.commit()
            return True
        return False
    finally:
        session.close()

# CRUD operations for the GardenPlot table
def add_new_plot(plot_name, location, size_sq_ft):
    session = get_session()
    try:
        new_plot = GardenPlot(plot_name=plot_name, location=location, size_sq_ft=size_sq_ft)
        session.add(new_plot)
        session.commit()
    finally:
        session.close()

def get_all_plots():
    session = get_session()
    try:
        plots = session.query(GardenPlot).all()
        return plots
    finally:
        session.close()

def delete_plot_by_id(plot_id):
    session = get_session()
    try:
        plot = session.query(GardenPlot).filter_by(id=plot_id).first()
        if plot:
            session.delete(plot)
            session.commit()
            return True
        return False
    finally:
        session.close()

# PlantedCrop helpers (Create, Read, Delete)
def find_or_create_crop_by_name(name):
    session = get_session()
    try:
        crop = session.query(Crop).filter_by(name=name.title()).first()
        return crop
    finally:
        session.close()

def find_or_create_plot_by_name(plot_name):
    session = get_session()
    try:
        plot = session.query(GardenPlot).filter_by(plot_name=plot_name.title()).first()
        return plot
    finally:
        session.close()

def add_planted_crop(crop, garden_plot, planting_date):
    session = get_session()
    try:
        expected_harvest_date = planting_date + timedelta(days=crop.growing_season_days)
        planted_crop = PlantedCrop(
            crop_id=crop.id,
            plot_id=garden_plot.id,
            planting_date=planting_date,
            expected_harvest_date=expected_harvest_date
        )
        session.add(planted_crop)
        session.commit()
        return planted_crop
    finally:
        session.close()

def get_all_planted_crops():
    session = get_session()
    try:
        # Eagerly load the related 'crop' and 'garden_plot' objects
        plants = session.query(PlantedCrop).options(joinedload(PlantedCrop.crop), joinedload(PlantedCrop.garden_plot)).all()
        return plants
    finally:
        session.close()

def delete_planted_crop(planted_crop_id):
    session = get_session()
    try:
        planted_crop = session.query(PlantedCrop).filter_by(id=planted_crop_id).first()
        if planted_crop:
            session.delete(planted_crop)
            session.commit()
            return True
        return False
    finally:
        session.close()
