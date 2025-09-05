import click
from datetime import date
from helpers import (
    find_or_create_crop_by_name,
    find_or_create_plot_by_name,
    add_planted_crop,
    get_all_planted_crops,
    delete_planted_crop,
    add_new_crop,
    get_all_crops,
    delete_crop_by_id,
    add_new_plot,
    get_all_plots,
    delete_plot_by_id
)

def crop_menu():
    while True:
        click.secho("\n--- Manage Crops ---", fg="yellow")
        click.secho("1. Add a new crop", fg="cyan")
        click.secho("2. View all crops", fg="cyan")
        click.secho("3. Delete a crop", fg="cyan")
        click.secho("4. Back to main menu", fg="cyan")
        choice = click.prompt("Select an option", type=int)

        try:
            if choice == 1:
                name = click.prompt("Enter crop name")
                growing_days = click.prompt("Enter growing season (days)", type=int)
                water_freq = click.prompt("Enter watering frequency (days)", type=int)
                add_new_crop(name, growing_days, water_freq)
                click.secho(f"Successfully added '{name}' to your crop list!", fg="green")

            elif choice == 2:
                crops = get_all_crops()
                if not crops:
                    click.secho("No crops found.", fg="red")
                else:
                    for c in crops:
                        click.secho(f"ID: {c.id} | Name: {c.name} | Growing Season: {c.growing_season_days} days | Water Frequency: {c.water_frequency_days} days", fg="blue")

            elif choice == 3:
                crop_id = click.prompt("Enter the ID of the crop to delete", type=int)
                if delete_crop_by_id(crop_id):
                    click.secho(f"Successfully deleted crop with ID {crop_id}.", fg="green")
                else:
                    click.secho(f"No crop found with ID {crop_id}.", fg="red")

            elif choice == 4:
                break
            else:
                click.secho("Invalid option.", fg="red")
        except ValueError:
            click.secho("Invalid input. Please enter a number.", fg="red")
        except Exception as e:
            click.secho(f"An error occurred: {e}", fg="red")

def plot_menu():
    while True:
        click.secho("\n--- Manage Garden Plots ---", fg="yellow")
        click.secho("1. Add a new plot", fg="cyan")
        click.secho("2. View all plots", fg="cyan")
        click.secho("3. Delete a plot", fg="cyan")
        click.secho("4. Back to main menu", fg="cyan")
        choice = click.prompt("Select an option", type=int)

        try:
            if choice == 1:
                plot_name = click.prompt("Enter plot name")
                location = click.prompt("Enter location")
                size = click.prompt("Enter size (sq ft)", type=int)
                add_new_plot(plot_name, location, size)
                click.secho(f"Successfully added '{plot_name}'!", fg="green")

            elif choice == 2:
                plots = get_all_plots()
                if not plots:
                    click.secho("No plots found.", fg="red")
                else:
                    for p in plots:
                        click.secho(f"ID: {p.id} | Name: {p.plot_name} | Location: {p.location} | Size: {p.size_sq_ft} sq ft", fg="blue")

            elif choice == 3:
                plot_id = click.prompt("Enter the ID of the plot to delete", type=int)
                if delete_plot_by_id(plot_id):
                    click.secho(f"Successfully deleted plot with ID {plot_id}.", fg="green")
                else:
                    click.secho(f"No plot found with ID {plot_id}.", fg="red")

            elif choice == 4:
                break
            else:
                click.secho("Invalid option.", fg="red")
        except ValueError:
            click.secho("Invalid input. Please enter a number.", fg="red")
        except Exception as e:
            click.secho(f"An error occurred: {e}", fg="red")

def planted_crop_menu():
    while True:
        click.secho("\n--- Planted Crops ---", fg="yellow")
        click.secho("1. Plant a new crop", fg="cyan")
        click.secho("2. View all planted crops", fg="cyan")
        click.secho("3. Harvest a crop", fg="cyan")
        click.secho("4. Back to main menu", fg="cyan")
        choice = click.prompt("Select an option", type=int)

        try:
            if choice == 1:
                name = click.prompt("Enter crop name")
                plot = click.prompt("Enter garden plot name")
                date_str = click.prompt("Enter planting date (YYYY-MM-DD)", default=str(date.today()))

                crop = find_or_create_crop_by_name(name)
                garden_plot = find_or_create_plot_by_name(plot)
                
                if not crop:
                    click.secho(f"Crop '{name}' not found. Please add it first.", fg="red")
                    continue
                if not garden_plot:
                    click.secho(f"Garden plot '{plot}' not found. Please add it first.", fg="red")
                    continue

                planting_date = date.fromisoformat(date_str)
                add_planted_crop(crop, garden_plot, planting_date)
                click.secho(f"Successfully planted {crop.name} in {garden_plot.plot_name}!", fg="green")

            elif choice == 2:
                plants = get_all_planted_crops()
                if not plants:
                    click.secho("No crops have been planted yet.", fg="red")
                else:
                    for plant in plants:
                        harvest_date_str = plant.expected_harvest_date.isoformat() if plant.expected_harvest_date else "N/A"
                        click.secho(f"ID: {plant.id} | Crop: {plant.crop.name} | Plot: {plant.garden_plot.plot_name} | Planted on: {plant.planting_date} | Expected Harvest: {harvest_date_str}", fg="blue")

            elif choice == 3:
                plant_id = click.prompt("Enter the ID of the crop to harvest", type=int)
                if delete_planted_crop(plant_id):
                    click.secho(f"Successfully harvested and removed plant with ID {plant_id}.", fg="green")
                else:
                    click.secho(f"No plant found with ID {plant_id}.", fg="red")
            
            elif choice == 4:
                break
            else:
                click.secho("Invalid option.", fg="red")
        except ValueError:
            click.secho("Invalid input. Please enter a number.", fg="red")
        except Exception as e:
            click.secho(f"An unexpected error occurred: {e}", fg="red")

def main_menu():
    while True:
        click.secho("\n==== Urban Gardening App ====", fg='green')
        click.secho("1. Manage Crops", fg='blue')
        click.secho("2. Manage Garden Plots", fg='blue')
        click.secho("3. Manage Planted Crops", fg='blue')
        click.secho("4. Exit", fg='blue')
        
        choice = click.prompt("Select an option", type=int)

        try:
            if choice == 1:
                crop_menu()
            elif choice == 2:
                plot_menu()
            elif choice == 3:
                planted_crop_menu()
            elif choice == 4:
                click.secho("Exiting the application. Goodbye!", fg='red')
                break
            else:
                click.secho("Invalid option. Please choose a number from the menu.", fg='red')
        except ValueError:
            click.secho("Invalid input. Please enter a number.", fg="red")

if __name__ == '__main__':
    main_menu()