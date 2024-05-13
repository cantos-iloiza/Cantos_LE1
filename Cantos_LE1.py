# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong" : {"quantity" : 3, "cost" : 2},
    "Super Mario Bros" : {"quantity" : 5, "cost" : 3},
    "Tetris" : {"quantity" : 2, "cost" : 1},
    "Tekken" : {"quantity" : 4, "cost" : 4},
    "Pac-Man" : {"quantity" : 3, "cost" : 2}
}

# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function to display centered title
def display_centered_title(title):
    terminal_width = 80
    title_length = len(title)
    left_margin = (terminal_width - title_length) // 2
    print("=" * left_margin + title + "=" * left_margin)

# Function to display available games and their details
def display_available_games():
    display_centered_title("Available Games")
    for game, info in game_library.items():
        print(f"{game} : Quantity - {info['quantity']}, Rental Cost - ${info['cost']}")
    print("===============================================================================")
    input("Press ENTER to continue...")
    main()

# Function to register a new user
def register_user():
    display_centered_title("User Sign Up")
    while True: # Looping until a valid username and password are entered
        username = input("Enter New Username: ")
        if not username:
            main()
        if username in user_accounts:
            print("This Username already exists. Try again.")
            continue
        password = input("Enter New Password: ")
        if len(password) < 8:
            print("Password must have at least 8 characters.")
            continue
        else: # Adding new user to user_accounts dictionary
            user_accounts[username] = {"Password" : password, "Balance" : 0, "Points" : 0, "Inventory" : {}}
            print("Signed up successfully!")
            input("Press ENTER to continue...")
        main()

# Function for user sign-in
def user_sign_in(): 
    display_centered_title("User Sign In")
    while True: # Looping until valid credentials are entered
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in user_accounts and user_accounts[username]['Password'] == password:
            if user_accounts[username]['Balance'] == 0:
                print("Login Successfully!")
            logged_in_menu(username)
        else:
            print("Error: Invalid Username or Password.")
        input("Press Enter to Continue....")

# Function to rent a game
def rent_game(username):
    display_centered_title("Rent Game")
    print("Available Games:")
    print("===============================================================================")
    game_index = 1
    game_index_map = {}
    for game, info in game_library.items():
        print(f"{game_index}. {game} : Quantity - {info['quantity']}, Rental Cost - ${info['cost']}")
        game_index_map[game_index] = game
        game_index += 1
    print("===============================================================================")
    # Looping until the user decides to stop renting games
    while True:
        try:
            game_index_choice = int(input("Select the index number of the game you would like to rent: "))
            game_name = game_index_map.get(game_index_choice)
            if not game_name:
                print("Invalid index number. Please try again.")
                continue
            if game_library[game_name]['quantity'] == 0:
                print("Sorry, the selected game is out of stock.")
                continue
            game_quantity = int(input(f"Copies of {game_name} to rent: "))
            if game_library[game_name]['quantity'] < game_quantity:
                print("Quantity available is insufficient.")
                return
            
            cost = game_library[game_name]['cost'] * game_quantity
            points_added = cost // 2

            print("\nPayment Method")
            print("1. Pay using Balance")
            print("2. Pay using Points")
            pay = int(input("Choose your Payment Methods: "))

            if pay == 1:
                if user_accounts[username]['Balance'] < cost:
                    print("Insufficient Balance")
                    input("Press ENTER to continue....")
                else: # Deducting balance and updating inventory
                    user_accounts[username]['Balance'] -= cost
                    print ("Rented Successfully!")
                    if game_name in user_accounts[username]['Inventory']:
                        user_accounts[username]['Inventory'][game_name] += game_quantity
                    else:
                        user_accounts[username]['Inventory'][game_name] = game_quantity
            elif pay == 2:
                if user_accounts[username]['Points'] < cost:
                    print("Insufficient Points")
                    input("Press ENTER to continue....")
                else: # Deducting balance and updating inventory
                    user_accounts[username]['Points'] -= cost
                    print(f"Rented {game_name} Successfully!")
                    if game_name in user_accounts[username]['Inventory']:
                        user_accounts[username]['Inventory'][game_name] += game_quantity
                    else:
                        user_accounts[username]['Inventory'][game_name] = game_quantity
            else:
                print("Invalid Choice. Please try again.")
                continue

            # Displaying remaining balance and updating points
            print(f"\nRemaining Balance: ${user_accounts[username]['Balance']:.2f}")
            user_accounts[username]['Points'] += points_added
            print(f"Points added: {points_added}")
            game_library[game_name]['quantity'] -= game_quantity

            # Asking the user if they want to rent another game
            choice = input("Do you want to rent another game? (Y/N): ").upper()
            if choice != 'Y':
                break

            # Re-displaying available games after redeeming a free rental
            print("Available Games:")
            print("=================================================")
            game_index = 1
            game_index_map = {}
            for game, info in game_library.items():
                print(f"{game_index}. {game}: Quantity - {info['quantity']} Rental Cost - {info['cost']}")
                game_index_map[game_index] = game
                game_index += 1
            print("=================================================")

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

    input("Press ENTER to continue...")
    logged_in_menu(username)
    

# Function to return a game
def return_game(username):
    display_centered_title("Return Game")
    print("User's Game Inventory:")
    print("===============================================================================")
    inventory = user_accounts[username]['Inventory']
    game_index = 1
    game_index_map = {}
    for game, quantity in inventory.items():
        print(f"{game_index}. {game}: Quantity - {quantity}")
        game_index_map[game_index] = game
        game_index += 1
    print("===============================================================================")
    while True:
        try:
            return_index = int(input("Enter the index number of the game you want to return: "))
            return_item = game_index_map.get(return_index)
            if not return_item:
                print("Invalid index number. Please try again.")
                return
            game_quantity = int(input(f"Copies of {return_item} to return: "))
            if return_item in inventory:
                inventory[return_item] -= game_quantity
                if inventory[return_item] < 0:
                    print("Invalid quantity. Please enter a valid quantity to return.")
                    return
                game_library[return_item]['quantity'] += game_quantity
                print(f"Returned {game_quantity} copies of {return_item} Successfully")
            else:
                print("Game Not Found.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        input("Press ENTER to continue...")
        logged_in_menu(username)

# Function to top up user's account balance
def top_up_account(username):
    display_centered_title("Top Up Account")
    top_up_amount = float(input("Enter amount: $"))
    user_accounts[username]['Balance'] += top_up_amount
    print("Topped up successfully!")
    print(f"Username: {username}, New Balance: ${user_accounts[username]['Balance']:.2f}")

    input("Press ENTER to continue...")
    logged_in_menu(username)

# Function to display user's game inventory
def display_inventory(username):
    display_centered_title("User's Game Inventory")
    print("=================================================")
    inventory = user_accounts[username]['Inventory']
    for game, quantity in inventory.items():
        print(f"{game}: Quantity - {quantity}")
    print("=================================================")
    
    input("Press ENTER to continue...")
    logged_in_menu(username)

# Function to redeem free rental games using user's points
def redeem_free_rental(username):
    while True:
        if user_accounts[username]['Points'] >= 3:
            display_centered_title("Redeem Free Rental")
            print(f"Congratulations! You have {user_accounts[username]['Points']} points to redeem FREE Game Rental/s!")
            print("--Notice: You can exchange 3 points to rent a free game!--")
            print("Available Games:")
            print("================================================================================")
            game_index = 1
            game_index_map = {}
            for game, info in game_library.items():
                print(f"{game_index}. {game}: Quantity - {info['quantity']}")
                game_index_map[game_index] = game
                game_index += 1
            print("================================================================================")
            try:
                game_index_choice = int(input("Select the number of the game you would like to rent for free: "))
                game_name = game_index_map.get(game_index_choice)
                if not game_name:
                    print("Invalid index number. Please try again.")
                    continue
                if game_name in game_library:
                    if game_library[game_name]['quantity'] > 0:
                        print(f"Rented {game_name} Successfully!")
                        user_accounts[username]['Points'] -= 3
                        game_library[game_name]['quantity'] -= 1
                        print(f"Remaining Points: {user_accounts[username]['Points']}")
                        
                        # Adding the rented game to the user's inventory
                        if game_name in user_accounts[username]['Inventory']:
                            user_accounts[username]['Inventory'][game_name] += 1
                        else:
                            user_accounts[username]['Inventory'][game_name] = 1
                            
                    else:
                        print("Sorry, the game you selected is currently out of stock.")
                else:
                    print("Game not Found")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("\nSorry, you have insufficient points.")

        choice = input("Do you want to redeem another free rental game? (Y/N): ").upper()
        if choice != 'Y':
            break
        
        # Re-displaying available games after redeeming a free rental
        print("Available Games:")
        print("=================================================")
        game_index = 1
        game_index_map = {}
        for game, info in game_library.items():
            print(f"{game_index}. {game}: Quantity - {info['quantity']}")
            game_index_map[game_index] = game
            game_index += 1
        print("=================================================")

    input("Press ENTER to continue...")
    logged_in_menu(username)

# Function to check user's balance and points
def check_balance(username):
    display_centered_title("Check Balance")
    print(f"\nCurrent Balance: ${user_accounts[username]['Balance']:.2f}")
    print(f"Available Points: {user_accounts[username]['Points']}")

    input("Press ENTER to continue...")
    logged_in_menu(username)

# Function to display the user menu after login
def logged_in_menu(username):
    display_centered_title("User Menu")
    print(f"Welcome to Video Game Rental, {username}!")
    print("Main Menu")
    print("--Notice: New Users should top up their accounts first before renting!--")
    print("1. Rent A Game")
    print("2. Return A Game")
    print("3. Top Up Account")
    print("4. Display User's Game Inventory")
    print("5. Redeem Free Rental Games")
    print("6. Check Balance and Points")
    print("7. Logout")
    print("===============================================================================")
    
    while True: # Looping until a valid choice is entered
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                rent_game(username)
            elif choice == 2:
                return_game(username)
            elif choice == 3:
                top_up_account(username)
            elif choice == 4:
                display_inventory(username)
            elif choice == 5:
                redeem_free_rental(username)
            elif choice == 6:
                check_balance(username)
            elif choice == 7:
                print("Logging out....")
                logged_in = False
                main()
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Value error: {e}")

# Function for admin login
def admin_login():
    display_centered_title("Admin Sign In")
    while True: # Looping until correct admin credentials are entered
        username = input("Enter Admin Username: ")
        password = input("Enter Admin Password: ")
        if username == admin_username and password == admin_password:
            print("Admin Login Successfully")
            input("Press ENTER to continue...")
            admin_menu()
            break
        else:
            print("Invalid Admin Credentials. Please try again.")
            
# Function to display the entire game inventory for the admin
def display_game_inventory():
    display_centered_title("Game Inventory")
    for game, info in game_library.items():
        print(f"{game}: Quantity - {info['quantity']}, Rental Cost - ${info['cost']}")
    print("================================================================================")
    
    input("Press ENTER to continue...")
    admin_menu()

# Function for updating game inventory by the admin
def admin_update():
    while True:
        display_centered_title("Update Game Inventory")
        print("1. Update Stock")
        print("2. Update Rental Game Cost")
        print("3. Return")
        choice = input("Enter your choice: ")

        if choice == '1':
            update_stock()
        elif choice == '2':
            update_cost()
        elif choice == '3':
            print("Returning to the Admin Menu...")
            input("Press ENTER to continue...")
            admin_menu()
            break
        else:
            print("Invalid Choice. Please Enter 1 to 3 options only.")

# Function to update game quantity by the admin
def update_stock():
    while True:
        display_centered_title("Update Game Quantity")
        print("Game Inventory:")
        print("================================================================================")
        game_index = 1
        game_index_map = {}
        for game, info in game_library.items():
            print(f"{game_index}. {game}: Quantity - {info['quantity']}")
            game_index_map[game_index] = game
            game_index += 1
        print("================================================================================")
        try:
            game_index_choice = int(input("Enter the index number of the Game: "))
            game_name = game_index_map.get(game_index_choice)
            if not game_name:
                print("Invalid index number. Please try again.")
                continue
            if game_name in game_library:
                add_quantity = int(input("Enter the Quantity to add: "))
                game_library[game_name]["quantity"] += add_quantity
                print(f"Added {add_quantity} copies to {game_name}. Updated Quantity: {game_library[game_name]['quantity']}")
            else:
                print("Game not Found.")
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        admin_update()

# Function to update rental game cost by the admin
def update_cost():
    while True:
        display_centered_title("Update Rental Game Cost")
        print("Game Inventory:")
        print("================================================================================")
        game_index = 1
        game_index_map = {}
        for game, info in game_library.items():
            print(f"{game_index}. {game}: Quantity - {info['quantity']} Rental Cost - ${info['cost']}")
            game_index_map[game_index] = game
            game_index += 1
        print("================================================================================")
        try:
            game_index_choice = int(input("Enter the index number of the Game: "))
            game_name = game_index_map.get(game_index_choice)
            if not game_name:
                print("Invalid index number. Please try again.")
                continue
            if game_name in game_library:
                new_cost = float(input("Enter the new cost of the game: $"))
                game_library[game_name]['cost'] = new_cost
                print(f"Updated cost of {game_name} is now ${new_cost}")
            else:
                print("Game not Found.")
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        admin_update()

# Function for admin menu
def admin_menu():
    while True:
        display_centered_title("Admin Menu")
        print("Welcome back, Admin!")
        print("1. Display Game Inventory")
        print("2. Update Game Inventory")
        print("3. Log out")
        print("================================================================================")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            display_game_inventory()
        elif choice == 2:
            admin_update()
        elif choice == 3:
            print("Logging out...\n")
            main()
            break

# Main function to start the program
def main():
    display_centered_title("Video Game Rental System")
    print("Main Menu")
    print("1. Display Available Games")
    print("2. Sign Up (User)")
    print("3. Sign In (User)")
    print("4. Admin Sign In")
    print("5. Exit")
    print("================================================================================")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        display_available_games()
    elif choice == 2:
        register_user()
    elif choice == 3:
        user_sign_in()
    elif choice == 4:
        admin_login()
    elif choice == 5:
        print("Exiting...")
        exit
    else:
        print("Invalid choice. Please enter a number between 1 and 5 only.")

# Starting the program
if __name__ == "__main__":
    main()
