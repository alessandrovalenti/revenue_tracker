import os
import sys
from revenue_tracker import database
from revenue_tracker.utils import validate_date

def menu():

    print("1. Add revenue")
    print("2. Visualize revenues")
    print("3. Manage revenues")
    print("4. Exit")

    choice = input("\nPlease select an option: ")

    match choice:
        case '1':
            # Call the function to add revenue
            add_revenue()
        case '2':
            # Call the function to visualize revenues
            if not database.table_exists():
                print("Revenues table does not exist.")
                return
            print("1. Visualize last 5 revenues")
            print("2. Visualize revenue by date")
            print("3. Visualize all revenues")
            print("4. Back")
            choice = input("\nPlease select an option: ")
            print()
            match choice:
                case '1':
                    print(database.get_last_revenues(n=5))
                    print()
                case '2':
                    date = input("Enter the date (YYYY-MM-DD) to visualize: ")
                    if not validate_date(date):
                        print("\nInvalid date format. Please enter in YYYY-MM-DD format.\n")
                        return
                    print(database.get_revenue_by_date(date))
                    print()
                case '3':
                    print(database.get_table())
                    print()
                case '4':
                    return
                case _:
                    print("\nInvalid choice.\n")
        case '3':
            # Call the function to manage revenues
            if not database.table_exists():
                print("Revenues table does not exist.")
                return
            print("1. Delete revenue by date")
            print("2. Delete revenue by ID")
            print("3. Delete all table")
            print("4. Back")
            choice = input("\nPlease select an option: ")
            match choice:
                case '1':
                    date = input("Enter the date (YYYY-MM-DD) of the revenue to delete: ")
                    city = input("Enter the city of the revenue to delete: ")
                    if not validate_date(date):
                        print("\nInvalid date format. Please enter in YYYY-MM-DD format.\n")
                        return
                    count = database.del_revenue_by_date(date, city)
                    if count == 0:
                        print(f"\nNo revenue found for {date} in {city}.\n")
                    else:
                        print(f"\nRevenue on {date} in {city} has been deleted.\n")
                case '2':
                    id_input = input("Enter the ID of the revenue to delete: ")
                    try:
                        id_value = int(id_input)
                        count = database.del_revenue_by_id(id_value)
                        if count == 0:
                            print(f"\nNo revenue found with ID {id_value}.\n")
                        else:
                            print(f"\nRevenue with ID {id_value} has been deleted.\n")
                    except ValueError:
                        print("\nInvalid ID. Please enter a valid ID.\n")
                case '3':
                    confirm = input("Are you sure you want to delete the entire table? (yes/no): ")
                    if confirm.lower() == 'yes':
                        database.del_table()
                        print("\nAll revenues have been deleted.\n")
                    else:
                        print("\nOperation cancelled.\n")
                case '4':
                    return
                case _:
                    print("\nInvalid choice.\n")

        case '4':
            print("\nExiting the application.\n")
            print("-"*40)
            choice = -1
        case _:
            print("Invalid choice. Please try again.\n")
    
    return choice
 

def add_revenue():

    print()
    date = input("Enter the date (YYYY-MM-DD): ")
    if not validate_date(date):
        print("Invalid date format. Please enter in YYYY-MM-DD format.\n")
        return
    
    city = input("Enter the city: ")


    declared_input = input("Enter the declared revenue: ")
    declared_revenue = float(declared_input) if declared_input.strip() else None

    revenue_input = input("Enter total revenue (default=Null): ")
    revenue = float(revenue_input) if revenue_input.strip() else None

    kind = input("Enter the kind of day (default=ordinary): ")
    kind = kind.strip() or None

    who = input("Enter who was at the market (format=X,Y,...): ")
    who = who.strip() or None

    notes = input("Enter any additional notes: ")
    notes = notes.strip() or None

    # Call the function to add the income to the database
    try:
        database.get_table()
    except Exception as e:
        print(f"No database found, creating a new one")
        database.create_table()
    if database.add_revenue(date, city, declared_revenue, revenue, kind, who, notes):
        return
    else:
        print(f"\nSaved data: {date}, {city}, {declared_revenue} EUR\n")


def visualize_revenues():
    # Call the function to visualize revenues
    try:
        df = database.get_table()
        print()
        print(df)
        print()
    except Exception as e:
        print(f"\nNo database found.\n")