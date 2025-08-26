from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Crop, GardenPlot, PlantedCrop
from datetime import date, timedelta

engine = create_engine('sqlite:///gardening.db')    

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(engine)

def seed_data():
    print("Seeding database initial data...")
    Session = sessionmaker(bind=engine)
    session = Session()

    # sample crops
    tomato = Crop(name='Tomato', growing_season_days=75, water_frequency_days=2)
    basil = Crop(name='Basil', growing_season_days=60, water_frequency_days=3)
    lettuce = Crop(name='Lettuce', growing_season_days=50, water_frequency_days=1)

    session.add_all([tomato, basil, lettuce])
    session.commit()

    # sample garden plots
    raised_bed = GardenPlot(plot_name='Raised Bed', location='Backyard', size_sq_ft=20)
    window_box = GardenPlot(plot_name='Window Box', location='Kitchen Window', size_sq_ft=5)
    
    
    session.add_all([raised_bed, window_box])
    session.commit()

    # sample planted crops
    today = date.today()
    tomato_planted = PlantedCrop(
        crop=tomato,
        garden_plot=raised_bed,
        planting_date=today  - timedelta(days=20),
        expected_harvest_date=today + timedelta(days=55)
    )

    basil_planted = PlantedCrop(
        crop=basil,
        garden_plot=window_box,
        planting_date=today - timedelta(days=10),
        expected_harvest_date=today + timedelta(days=50)
    )

    session.add_all([tomato_planted, basil_planted])
    session.commit()

    session.close()
    print("Database seeded successfully.")

if __name__ == '__main__':
    create_tables()
    seed_data()