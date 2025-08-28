import click
from datetime import date
from helpers import (
    find_or_create_crop, 
    find_or_create_plot, 
    add_planted_crop,
    get_all_planted_crops,
    delete_planted_crop
)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', prompt='Crop name', help='The name of the crop to plant.')
@click.option('--plot', prompt='Plot name', help='The name of the garden plot.')
@click.option('--date', default=str(date.today()), help='Planting date (YYYY-MM-DD). Defaults to today.')
def plant(name, plot, date):
    try:
        crop = find_or_create_crop(name)
        if not crop.growing_season_days:
             growing_days = click.prompt("Enter approximate growing season in days", type=int)
             water_freq = click.prompt("Enter watering frequency in days", type=int)
             crop = find_or_create_crop(name, growing_days, water_freq)

        garden_plot = find_or_create_plot(plot)
        if not garden_plot.location:
             location = click.prompt("Enter the plot's location")
             size = click.prompt("Enter the plot's size in sq ft", type=int)
             garden_plot = find_or_create_plot(plot, location, size)

        planting_date = date.fromisoformat(date)
        
        add_planted_crop(crop, garden_plot, planting_date)
        click.secho(f"\nSuccessfully planted {crop.name} in {garden_plot.plot_name}!", fg="green")

    except ValueError as e:
        click.secho(f"Error: {e}", fg="red")
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg="red")


@cli.command()
def view():
    plants = get_all_planted_crops()
    if not plants:
        click.secho("No crops have been planted yet.", fg="red")
        return

    click.secho("\n--- All Planted Crops ---", fg="blue")
    for plant in plants:
        harvest_date_str = plant.expected_harvest_date.isoformat() if plant.expected_harvest_date else "N/A"
        click.secho(f"ID: {plant.id} | Crop: {plant.crop.name} | Plot: {plant.garden_plot.plot_name} | Planted on: {plant.planting_date} | Expected Harvest: {harvest_date_str}", fg="cyan")


@cli.command()
@click.option('--id', prompt='Plant ID', type=int, help='The ID of the crop to harvest.')
def harvest(id):
    if delete_planted_crop(id):
        click.secho(f"Successfully harvested and removed plant with ID {id}.", fg="green")
    else:
        click.secho(f"No plant found with ID {id}.", fg="red")


if __name__ == '__main__':
    cli()