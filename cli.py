import click
from datetime import date
from helpers import (
    find_or_create_crop, 
    find_or_create_plot, 
    add_planted_crop,
    get_all_planted_crops,
    delete_planted_crop,
    create_database_tables
)

def plant_crop():
    """Prompts user for details to plant a new crop."""
    click.secho("\n--- Plant a New Crop ---", fg="green")
    name = click.prompt("Enter crop name")
    plot = click.prompt("Enter garden plot name")
    date_str = click.prompt("Enter planting date (YYYY-MM-DD)", default=str(date.today()))

    try:
        # Find or create crop
        crop = find_or_create_crop(name)
        if not crop.growing_season_days:
             growing_days = click.prompt("Enter approximate growing season in days", type=int)
             water_freq = click.prompt("Enter watering frequency in days", type=int)
             crop = find_or_create_crop(name, growing_days, water_freq)

        # Find or create plot
        garden_plot = find_or_create_plot(plot)
        if not garden_plot.location:
             location = click.prompt("Enter the plot's location")
             size = click.prompt("Enter the plot's size in sq ft", type=int)
             garden_plot = find_or_create_plot(plot, location, size)

        planting_date = date.fromisoformat(date_str)
        
        # Add the planted crop
        add_planted_crop(crop, garden_plot, planting_date)
        click.secho(f"Successfully planted {crop.name} in {garden_plot.plot_name}!", fg="green")

    except ValueError as e:
        click.secho(f"Error: {e}", fg="red")
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg="red")

def view_crops():
    """Displays all planted crops."""
    plants = get_all_planted_crops()
    if not plants:
        click.secho("No crops have been planted yet.", fg="red")
        return

    click.secho("\n--- All Planted Crops ---", fg="blue")
    for plant in plants:
        harvest_date_str = plant.expected_harvest_date.isoformat() if plant.expected_harvest_date else "N/A"
        click.secho(f"ID: {plant.id} | Crop: {plant.crop.name} | Plot: {plant.garden_plot.plot_name} | Planted on: {plant.planting_date} | Expected Harvest: {harvest_date_str}", fg="cyan")

def harvest_crop():
    """Prompts user to harvest a crop by ID."""
    click.secho("\n--- Harvest a Crop ---", fg="green")
    try:
        plant_id = click.prompt("Enter the ID of the crop to harvest", type=int)
        if delete_planted_crop(plant_id):
            click.secho(f"Successfully harvested and removed plant with ID {plant_id}.", fg="green")
        else:
            click.secho(f"No plant found with ID {plant_id}.", fg="red")
    except ValueError:
        click.secho("Invalid input. Please enter a number.", fg="red")

def main_menu():
    """Main menu loop for the CLI application."""
    while True:
        click.secho("\n==== Urban Gardening App ====", fg='yellow')
        click.secho("1. Plant a new crop", fg='blue')
        click.secho("2. View all planted crops", fg='blue')
        click.secho("3. Harvest a crop", fg='blue')
        click.secho("4. Exit", fg='blue')
        
        choice = click.prompt("Select an option", type=int)

        if choice == 1:
            plant_crop()
        elif choice == 2:
            view_crops()
        elif choice == 3:
            harvest_crop()
        elif choice == 4:
            click.secho("Exiting the application. Goodbye!", fg='red')
            break
        else:
            click.secho("Invalid option. Please choose a number from the menu.", fg='red')


if __name__ == '__main__':
    create_database_tables()
    main_menu()