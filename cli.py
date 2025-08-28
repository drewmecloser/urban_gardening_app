import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Crop, GardenPlot, PlantedCrop
from datetime import date, timedelta

engine = create_engine('sqlite:///gardening.db')
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='Crop name', help='The name of the crop to plant.')
@click.option('--plot', prompt='Plot name', help='The name of the garden plot.')
@click.option('--date', default=str(date.today()), help='Planting date (YYYY-MM-DD). Defaults to today.')
def plant(name, plot, date):
    session = get_session()
    
    crop = session.query(Crop).filter_by(name=name.title()).first()
    if not crop:
        click.echo(f"Crop '{name.title()}' not found. Creating a new entry...")
        growing_days = click.prompt("Enter approximate growing season in days", type=int)
        water_freq = click.prompt("Enter watering frequency in days", type=int)
        crop = Crop(name=name.title(), growing_season_days=growing_days, water_frequency_days=water_freq)
        session.add(crop)
        session.commit()
    
    garden_plot = session.query(GardenPlot).filter_by(plot_name=plot.title()).first()
    if not garden_plot:
        click.echo(f"Garden plot '{plot.title()}' not found. Creating a new entry...")
        location = click.prompt("Enter the plot's location")
        size = click.prompt("Enter the plot's size in sq ft", type=int)
        garden_plot = GardenPlot(plot_name=plot.title(), location=location, size_sq_ft=size)
        session.add(garden_plot)
        session.commit()

    try:
        planting_date = date.fromisoformat(date)
    except ValueError:
        click.echo("Invalid date format. Using today's date.")
        planting_date = date.today()

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
    session.close()
    click.echo(f"\nSuccessfully planted {crop.name} in {garden_plot.plot_name}!")


@cli.command()
def view():
    session = get_session()
    plants = session.query(PlantedCrop).all()
    
    if not plants:
        click.echo("No crops have been planted yet.")
        return

    click.echo("\n--- All Planted Crops ---")
    for plant in plants:
        harvest_date_str = plant.expected_harvest_date.isoformat() if plant.expected_harvest_date else "N/A"
        click.echo(f"ID: {plant.id}")
        click.echo(f"  - Crop: {plant.crop.name}")
        click.echo(f"  - Plot: {plant.garden_plot.plot_name}")
        click.echo(f"  - Planted on: {plant.planting_date}")
        click.echo(f"  - Expected Harvest: {harvest_date_str}\n")
    
    session.close()

@cli.command()
@click.option('--id', prompt='Plant ID', type=int, help='The ID of the crop to harvest.')
def harvest(id):
    session = get_session()
    plant_to_harvest = session.query(PlantedCrop).filter_by(id=id).first()
    
    if plant_to_harvest:
        session.delete(plant_to_harvest)
        session.commit()
        click.echo(f"Successfully harvested and removed plant with ID {id}.")
    else:
        click.echo(f"No plant found with ID {id}.")
    
    session.close()

if __name__ == '__main__':
    cli()
