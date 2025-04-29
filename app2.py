import json
import os
import datetime
import random
import time
import matplotlib.pyplot as plt

# Paths
USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# User management
class User:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        if data:
            self.data = data
        else:
            self.data = {
                "weight_records": [],
                "meal_records": [],
                "exercise_records": [],
                "water_records": [],
                "daily_goals": {
                    "steps": 10000,
                    "water_ml": 2000
                }
            }

    def record_weight(self, weight):
        self.data["weight_records"].append({
            "date": str(datetime.date.today()),
            "weight": weight
        })

    def record_meal(self, meal):
        self.data["meal_records"].append({
            "date": str(datetime.date.today()),
            "meal": meal
        })

    def record_exercise(self, exercise, duration):
        self.data["exercise_records"].append({
            "date": str(datetime.date.today()),
            "exercise": exercise,
            "duration_minutes": duration
        })

    def record_water(self, amount_ml):
        self.data["water_records"].append({
            "date": str(datetime.date.today()),
            "amount_ml": amount_ml
        })

    def calculate_bmi(self, height_meters):
        if not self.data["weight_records"]:
            return None
        latest_weight = self.data["weight_records"][-1]["weight"]
        bmi = latest_weight / (height_meters ** 2)
        return round(bmi, 2)

    def set_daily_goals(self, steps, water_ml):
        self.data["daily_goals"] = {
            "steps": steps,
            "water_ml": water_ml
        }

    def get_water_intake_today(self):
        today = str(datetime.date.today())
        total = sum(entry['amount_ml'] for entry in self.data["water_records"] if entry['date'] == today)
        return total

    def save(self):
        users = load_users()
        users[self.username] = {
            "password": self.password,
            "data": self.data
        }
        save_users(users)

# Health tips
HEALTH_TIPS = [
    "Drink plenty of water.",
    "Get at least 7-8 hours of sleep.",
    "Eat more fruits and vegetables.",
    "Exercise for at least 30 minutes a day.",
    "Take breaks from screens every hour.",
    "Practice deep breathing exercises.",
    "Maintain a regular eating schedule.",
    "Limit sugary drinks and snacks.",
    "Stretch every morning.",
    "Stay socially connected with friends."
]

def get_random_health_tip():
    return random.choice(HEALTH_TIPS)

# Reports
def weekly_report(user):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    print("\n--- Weekly Report ---")
    print("Weight entries:")
    for entry in user.data["weight_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['weight']} kg")

    print("\nExercises:")
    for entry in user.data["exercise_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['exercise']} for {entry['duration_minutes']} minutes")

    print("\nWater Intake:")
    total_water = 0
    for entry in user.data["water_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            total_water += entry['amount_ml']
    print(f"Total water intake in past 7 days: {total_water} ml")

# Plotting

def plot_weight_progress(user):
    dates = [entry['date'] for entry in user.data["weight_records"]]
    weights = [entry['weight'] for entry in user.data["weight_records"]]

    if not dates:
        print("No weight data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(dates, weights, marker='o')
    plt.title("Weight Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Application logic
def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    users = load_users()
    if username in users:
        print("Username already exists. Try logging in.")
        return None
    user = User(username, password)
    user.save()
    print("Account created successfully!")
    return user

def login():
    username = input("Username: ")
    password = input("Password: ")
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]["data"]
        user = User(username, password, user_data)
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Record weight")
        print("2. Record meal")
        print("3. Record exercise")
        print("4. Record water intake")
        print("5. Calculate BMI")
        print("6. Set daily goals")
        print("7. View weekly report")
        print("8. Plot weight progress")
        print("9. Show random health tip")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            weight = float(input("Enter your weight (kg): "))
            user.record_weight(weight)
            user.save()
            print("Weight recorded.")
        elif choice == "2":
            meal = input("Describe your meal: ")
            user.record_meal(meal)
            user.save()
            print("Meal recorded.")
        elif choice == "3":
            exercise = input("Type of exercise: ")
            duration = int(input("Duration (minutes): "))
            user.record_exercise(exercise, duration)
            user.save()
            print("Exercise recorded.")
        elif choice == "4":
            amount = int(input("Amount of water (ml): "))
            user.record_water(amount)
            user.save()
            print("Water intake recorded.")
        elif choice == "5":
            height = float(input("Enter your height in meters: "))
            bmi = user.calculate_bmi(height)
            if bmi:
                print(f"Your BMI is {bmi}")
            else:
                print("No weight records found.")
        elif choice == "6":
            steps = int(input("Set daily steps goal: "))
            water_ml = int(input("Set daily water intake goal (ml): "))
            user.set_daily_goals(steps, water_ml)
            user.save()
            print("Daily goals updated.")
        elif choice == "7":
            weekly_report(user)
        elif choice == "8":
            plot_weight_progress(user)
        elif choice == "9":
            print(get_random_health_tip())
        elif choice == "10":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point
def main():
    print("Welcome to Health Tracker App!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user = signup()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Thank you for using the Health Tracker App. Stay healthy!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

    # Paths
USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# User management
class User:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        if data:
            self.data = data
        else:
            self.data = {
                "weight_records": [],
                "meal_records": [],
                "exercise_records": [],
                "water_records": [],
                "daily_goals": {
                    "steps": 10000,
                    "water_ml": 2000
                }
            }

    def record_weight(self, weight):
        self.data["weight_records"].append({
            "date": str(datetime.date.today()),
            "weight": weight
        })

    def record_meal(self, meal):
        self.data["meal_records"].append({
            "date": str(datetime.date.today()),
            "meal": meal
        })

    def record_exercise(self, exercise, duration):
        self.data["exercise_records"].append({
            "date": str(datetime.date.today()),
            "exercise": exercise,
            "duration_minutes": duration
        })

    def record_water(self, amount_ml):
        self.data["water_records"].append({
            "date": str(datetime.date.today()),
            "amount_ml": amount_ml
        })

    def calculate_bmi(self, height_meters):
        if not self.data["weight_records"]:
            return None
        latest_weight = self.data["weight_records"][-1]["weight"]
        bmi = latest_weight / (height_meters ** 2)
        return round(bmi, 2)

    def set_daily_goals(self, steps, water_ml):
        self.data["daily_goals"] = {
            "steps": steps,
            "water_ml": water_ml
        }

    def get_water_intake_today(self):
        today = str(datetime.date.today())
        total = sum(entry['amount_ml'] for entry in self.data["water_records"] if entry['date'] == today)
        return total

    def save(self):
        users = load_users()
        users[self.username] = {
            "password": self.password,
            "data": self.data
        }
        save_users(users)

# Health tips
HEALTH_TIPS = [
    "Drink plenty of water.",
    "Get at least 7-8 hours of sleep.",
    "Eat more fruits and vegetables.",
    "Exercise for at least 30 minutes a day.",
    "Take breaks from screens every hour.",
    "Practice deep breathing exercises.",
    "Maintain a regular eating schedule.",
    "Limit sugary drinks and snacks.",
    "Stretch every morning.",
    "Stay socially connected with friends."
]

def get_random_health_tip():
    return random.choice(HEALTH_TIPS)

# Reports
def weekly_report(user):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    print("\n--- Weekly Report ---")
    print("Weight entries:")
    for entry in user.data["weight_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['weight']} kg")

    print("\nExercises:")
    for entry in user.data["exercise_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['exercise']} for {entry['duration_minutes']} minutes")

    print("\nWater Intake:")
    total_water = 0
    for entry in user.data["water_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            total_water += entry['amount_ml']
    print(f"Total water intake in past 7 days: {total_water} ml")

# Plotting

def plot_weight_progress(user):
    dates = [entry['date'] for entry in user.data["weight_records"]]
    weights = [entry['weight'] for entry in user.data["weight_records"]]

    if not dates:
        print("No weight data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(dates, weights, marker='o')
    plt.title("Weight Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Application logic
def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    users = load_users()
    if username in users:
        print("Username already exists. Try logging in.")
        return None
    user = User(username, password)
    user.save()
    print("Account created successfully!")
    return user

def login():
    username = input("Username: ")
    password = input("Password: ")
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]["data"]
        user = User(username, password, user_data)
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Record weight")
        print("2. Record meal")
        print("3. Record exercise")
        print("4. Record water intake")
        print("5. Calculate BMI")
        print("6. Set daily goals")
        print("7. View weekly report")
        print("8. Plot weight progress")
        print("9. Show random health tip")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            weight = float(input("Enter your weight (kg): "))
            user.record_weight(weight)
            user.save()
            print("Weight recorded.")
        elif choice == "2":
            meal = input("Describe your meal: ")
            user.record_meal(meal)
            user.save()
            print("Meal recorded.")
        elif choice == "3":
            exercise = input("Type of exercise: ")
            duration = int(input("Duration (minutes): "))
            user.record_exercise(exercise, duration)
            user.save()
            print("Exercise recorded.")
        elif choice == "4":
            amount = int(input("Amount of water (ml): "))
            user.record_water(amount)
            user.save()
            print("Water intake recorded.")
        elif choice == "5":
            height = float(input("Enter your height in meters: "))
            bmi = user.calculate_bmi(height)
            if bmi:
                print(f"Your BMI is {bmi}")
            else:
                print("No weight records found.")
        elif choice == "6":
            steps = int(input("Set daily steps goal: "))
            water_ml = int(input("Set daily water intake goal (ml): "))
            user.set_daily_goals(steps, water_ml)
            user.save()
            print("Daily goals updated.")
        elif choice == "7":
            weekly_report(user)
        elif choice == "8":
            plot_weight_progress(user)
        elif choice == "9":
            print(get_random_health_tip())
        elif choice == "10":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point
def main():
    print("Welcome to Health Tracker App!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user = signup()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Thank you for using the Health Tracker App. Stay healthy!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

    # Paths
USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# User management
class User:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        if data:
            self.data = data
        else:
            self.data = {
                "weight_records": [],
                "meal_records": [],
                "exercise_records": [],
                "water_records": [],
                "daily_goals": {
                    "steps": 10000,
                    "water_ml": 2000
                }
            }

    def record_weight(self, weight):
        self.data["weight_records"].append({
            "date": str(datetime.date.today()),
            "weight": weight
        })

    def record_meal(self, meal):
        self.data["meal_records"].append({
            "date": str(datetime.date.today()),
            "meal": meal
        })

    def record_exercise(self, exercise, duration):
        self.data["exercise_records"].append({
            "date": str(datetime.date.today()),
            "exercise": exercise,
            "duration_minutes": duration
        })

    def record_water(self, amount_ml):
        self.data["water_records"].append({
            "date": str(datetime.date.today()),
            "amount_ml": amount_ml
        })

    def calculate_bmi(self, height_meters):
        if not self.data["weight_records"]:
            return None
        latest_weight = self.data["weight_records"][-1]["weight"]
        bmi = latest_weight / (height_meters ** 2)
        return round(bmi, 2)

    def set_daily_goals(self, steps, water_ml):
        self.data["daily_goals"] = {
            "steps": steps,
            "water_ml": water_ml
        }

    def get_water_intake_today(self):
        today = str(datetime.date.today())
        total = sum(entry['amount_ml'] for entry in self.data["water_records"] if entry['date'] == today)
        return total

    def save(self):
        users = load_users()
        users[self.username] = {
            "password": self.password,
            "data": self.data
        }
        save_users(users)

# Health tips
HEALTH_TIPS = [
    "Drink plenty of water.",
    "Get at least 7-8 hours of sleep.",
    "Eat more fruits and vegetables.",
    "Exercise for at least 30 minutes a day.",
    "Take breaks from screens every hour.",
    "Practice deep breathing exercises.",
    "Maintain a regular eating schedule.",
    "Limit sugary drinks and snacks.",
    "Stretch every morning.",
    "Stay socially connected with friends."
]

def get_random_health_tip():
    return random.choice(HEALTH_TIPS)

# Reports
def weekly_report(user):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    print("\n--- Weekly Report ---")
    print("Weight entries:")
    for entry in user.data["weight_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['weight']} kg")

    print("\nExercises:")
    for entry in user.data["exercise_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['exercise']} for {entry['duration_minutes']} minutes")

    print("\nWater Intake:")
    total_water = 0
    for entry in user.data["water_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            total_water += entry['amount_ml']
    print(f"Total water intake in past 7 days: {total_water} ml")

# Plotting

def plot_weight_progress(user):
    dates = [entry['date'] for entry in user.data["weight_records"]]
    weights = [entry['weight'] for entry in user.data["weight_records"]]

    if not dates:
        print("No weight data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(dates, weights, marker='o')
    plt.title("Weight Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Application logic
def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    users = load_users()
    if username in users:
        print("Username already exists. Try logging in.")
        return None
    user = User(username, password)
    user.save()
    print("Account created successfully!")
    return user

def login():
    username = input("Username: ")
    password = input("Password: ")
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]["data"]
        user = User(username, password, user_data)
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Record weight")
        print("2. Record meal")
        print("3. Record exercise")
        print("4. Record water intake")
        print("5. Calculate BMI")
        print("6. Set daily goals")
        print("7. View weekly report")
        print("8. Plot weight progress")
        print("9. Show random health tip")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            weight = float(input("Enter your weight (kg): "))
            user.record_weight(weight)
            user.save()
            print("Weight recorded.")
        elif choice == "2":
            meal = input("Describe your meal: ")
            user.record_meal(meal)
            user.save()
            print("Meal recorded.")
        elif choice == "3":
            exercise = input("Type of exercise: ")
            duration = int(input("Duration (minutes): "))
            user.record_exercise(exercise, duration)
            user.save()
            print("Exercise recorded.")
        elif choice == "4":
            amount = int(input("Amount of water (ml): "))
            user.record_water(amount)
            user.save()
            print("Water intake recorded.")
        elif choice == "5":
            height = float(input("Enter your height in meters: "))
            bmi = user.calculate_bmi(height)
            if bmi:
                print(f"Your BMI is {bmi}")
            else:
                print("No weight records found.")
        elif choice == "6":
            steps = int(input("Set daily steps goal: "))
            water_ml = int(input("Set daily water intake goal (ml): "))
            user.set_daily_goals(steps, water_ml)
            user.save()
            print("Daily goals updated.")
        elif choice == "7":
            weekly_report(user)
        elif choice == "8":
            plot_weight_progress(user)
        elif choice == "9":
            print(get_random_health_tip())
        elif choice == "10":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point
def main():
    print("Welcome to Health Tracker App!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user = signup()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Thank you for using the Health Tracker App. Stay healthy!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


    # Paths
USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# User management
class User:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        if data:
            self.data = data
        else:
            self.data = {
                "weight_records": [],
                "meal_records": [],
                "exercise_records": [],
                "water_records": [],
                "daily_goals": {
                    "steps": 10000,
                    "water_ml": 2000
                }
            }

    def record_weight(self, weight):
        self.data["weight_records"].append({
            "date": str(datetime.date.today()),
            "weight": weight
        })

    def record_meal(self, meal):
        self.data["meal_records"].append({
            "date": str(datetime.date.today()),
            "meal": meal
        })

    def record_exercise(self, exercise, duration):
        self.data["exercise_records"].append({
            "date": str(datetime.date.today()),
            "exercise": exercise,
            "duration_minutes": duration
        })

    def record_water(self, amount_ml):
        self.data["water_records"].append({
            "date": str(datetime.date.today()),
            "amount_ml": amount_ml
        })

    def calculate_bmi(self, height_meters):
        if not self.data["weight_records"]:
            return None
        latest_weight = self.data["weight_records"][-1]["weight"]
        bmi = latest_weight / (height_meters ** 2)
        return round(bmi, 2)

    def set_daily_goals(self, steps, water_ml):
        self.data["daily_goals"] = {
            "steps": steps,
            "water_ml": water_ml
        }

    def get_water_intake_today(self):
        today = str(datetime.date.today())
        total = sum(entry['amount_ml'] for entry in self.data["water_records"] if entry['date'] == today)
        return total

    def save(self):
        users = load_users()
        users[self.username] = {
            "password": self.password,
            "data": self.data
        }
        save_users(users)

# Health tips
HEALTH_TIPS = [
    "Drink plenty of water.",
    "Get at least 7-8 hours of sleep.",
    "Eat more fruits and vegetables.",
    "Exercise for at least 30 minutes a day.",
    "Take breaks from screens every hour.",
    "Practice deep breathing exercises.",
    "Maintain a regular eating schedule.",
    "Limit sugary drinks and snacks.",
    "Stretch every morning.",
    "Stay socially connected with friends."
]

def get_random_health_tip():
    return random.choice(HEALTH_TIPS)

# Reports
def weekly_report(user):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    print("\n--- Weekly Report ---")
    print("Weight entries:")
    for entry in user.data["weight_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['weight']} kg")

    print("\nExercises:")
    for entry in user.data["exercise_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['exercise']} for {entry['duration_minutes']} minutes")

    print("\nWater Intake:")
    total_water = 0
    for entry in user.data["water_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            total_water += entry['amount_ml']
    print(f"Total water intake in past 7 days: {total_water} ml")

# Plotting

def plot_weight_progress(user):
    dates = [entry['date'] for entry in user.data["weight_records"]]
    weights = [entry['weight'] for entry in user.data["weight_records"]]

    if not dates:
        print("No weight data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(dates, weights, marker='o')
    plt.title("Weight Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Application logic
def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    users = load_users()
    if username in users:
        print("Username already exists. Try logging in.")
        return None
    user = User(username, password)
    user.save()
    print("Account created successfully!")
    return user

def login():
    username = input("Username: ")
    password = input("Password: ")
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]["data"]
        user = User(username, password, user_data)
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Record weight")
        print("2. Record meal")
        print("3. Record exercise")
        print("4. Record water intake")
        print("5. Calculate BMI")
        print("6. Set daily goals")
        print("7. View weekly report")
        print("8. Plot weight progress")
        print("9. Show random health tip")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            weight = float(input("Enter your weight (kg): "))
            user.record_weight(weight)
            user.save()
            print("Weight recorded.")
        elif choice == "2":
            meal = input("Describe your meal: ")
            user.record_meal(meal)
            user.save()
            print("Meal recorded.")
        elif choice == "3":
            exercise = input("Type of exercise: ")
            duration = int(input("Duration (minutes): "))
            user.record_exercise(exercise, duration)
            user.save()
            print("Exercise recorded.")
        elif choice == "4":
            amount = int(input("Amount of water (ml): "))
            user.record_water(amount)
            user.save()
            print("Water intake recorded.")
        elif choice == "5":
            height = float(input("Enter your height in meters: "))
            bmi = user.calculate_bmi(height)
            if bmi:
                print(f"Your BMI is {bmi}")
            else:
                print("No weight records found.")
        elif choice == "6":
            steps = int(input("Set daily steps goal: "))
            water_ml = int(input("Set daily water intake goal (ml): "))
            user.set_daily_goals(steps, water_ml)
            user.save()
            print("Daily goals updated.")
        elif choice == "7":
            weekly_report(user)
        elif choice == "8":
            plot_weight_progress(user)
        elif choice == "9":
            print(get_random_health_tip())
        elif choice == "10":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point
def main():
    print("Welcome to Health Tracker App!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user = signup()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Thank you for using the Health Tracker App. Stay healthy!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


    # Paths
USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# User management
class User:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        if data:
            self.data = data
        else:
            self.data = {
                "weight_records": [],
                "meal_records": [],
                "exercise_records": [],
                "water_records": [],
                "daily_goals": {
                    "steps": 10000,
                    "water_ml": 2000
                }
            }

    def record_weight(self, weight):
        self.data["weight_records"].append({
            "date": str(datetime.date.today()),
            "weight": weight
        })

    def record_meal(self, meal):
        self.data["meal_records"].append({
            "date": str(datetime.date.today()),
            "meal": meal
        })

    def record_exercise(self, exercise, duration):
        self.data["exercise_records"].append({
            "date": str(datetime.date.today()),
            "exercise": exercise,
            "duration_minutes": duration
        })

    def record_water(self, amount_ml):
        self.data["water_records"].append({
            "date": str(datetime.date.today()),
            "amount_ml": amount_ml
        })

    def calculate_bmi(self, height_meters):
        if not self.data["weight_records"]:
            return None
        latest_weight = self.data["weight_records"][-1]["weight"]
        bmi = latest_weight / (height_meters ** 2)
        return round(bmi, 2)

    def set_daily_goals(self, steps, water_ml):
        self.data["daily_goals"] = {
            "steps": steps,
            "water_ml": water_ml
        }

    def get_water_intake_today(self):
        today = str(datetime.date.today())
        total = sum(entry['amount_ml'] for entry in self.data["water_records"] if entry['date'] == today)
        return total

    def save(self):
        users = load_users()
        users[self.username] = {
            "password": self.password,
            "data": self.data
        }
        save_users(users)

# Health tips
HEALTH_TIPS = [
    "Drink plenty of water.",
    "Get at least 7-8 hours of sleep.",
    "Eat more fruits and vegetables.",
    "Exercise for at least 30 minutes a day.",
    "Take breaks from screens every hour.",
    "Practice deep breathing exercises.",
    "Maintain a regular eating schedule.",
    "Limit sugary drinks and snacks.",
    "Stretch every morning.",
    "Stay socially connected with friends."
]

def get_random_health_tip():
    return random.choice(HEALTH_TIPS)

# Reports
def weekly_report(user):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    print("\n--- Weekly Report ---")
    print("Weight entries:")
    for entry in user.data["weight_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['weight']} kg")

    print("\nExercises:")
    for entry in user.data["exercise_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['exercise']} for {entry['duration_minutes']} minutes")

    print("\nWater Intake:")
    total_water = 0
    for entry in user.data["water_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            total_water += entry['amount_ml']
    print(f"Total water intake in past 7 days: {total_water} ml")

# Plotting

def plot_weight_progress(user):
    dates = [entry['date'] for entry in user.data["weight_records"]]
    weights = [entry['weight'] for entry in user.data["weight_records"]]

    if not dates:
        print("No weight data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(dates, weights, marker='o')
    plt.title("Weight Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Application logic
def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    users = load_users()
    if username in users:
        print("Username already exists. Try logging in.")
        return None
    user = User(username, password)
    user.save()
    print("Account created successfully!")
    return user

def login():
    username = input("Username: ")
    password = input("Password: ")
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]["data"]
        user = User(username, password, user_data)
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Record weight")
        print("2. Record meal")
        print("3. Record exercise")
        print("4. Record water intake")
        print("5. Calculate BMI")
        print("6. Set daily goals")
        print("7. View weekly report")
        print("8. Plot weight progress")
        print("9. Show random health tip")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            weight = float(input("Enter your weight (kg): "))
            user.record_weight(weight)
            user.save()
            print("Weight recorded.")
        elif choice == "2":
            meal = input("Describe your meal: ")
            user.record_meal(meal)
            user.save()
            print("Meal recorded.")
        elif choice == "3":
            exercise = input("Type of exercise: ")
            duration = int(input("Duration (minutes): "))
            user.record_exercise(exercise, duration)
            user.save()
            print("Exercise recorded.")
        elif choice == "4":
            amount = int(input("Amount of water (ml): "))
            user.record_water(amount)
            user.save()
            print("Water intake recorded.")
        elif choice == "5":
            height = float(input("Enter your height in meters: "))
            bmi = user.calculate_bmi(height)
            if bmi:
                print(f"Your BMI is {bmi}")
            else:
                print("No weight records found.")
        elif choice == "6":
            steps = int(input("Set daily steps goal: "))
            water_ml = int(input("Set daily water intake goal (ml): "))
            user.set_daily_goals(steps, water_ml)
            user.save()
            print("Daily goals updated.")
        elif choice == "7":
            weekly_report(user)
        elif choice == "8":
            plot_weight_progress(user)
        elif choice == "9":
            print(get_random_health_tip())
        elif choice == "10":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point
def main():
    print("Welcome to Health Tracker App!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user = signup()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Thank you for using the Health Tracker App. Stay healthy!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


    # Paths
USERS_FILE = "users.json"

# Helper functions
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# User management
class User:
    def __init__(self, username, password, data=None):
        self.username = username
        self.password = password
        if data:
            self.data = data
        else:
            self.data = {
                "weight_records": [],
                "meal_records": [],
                "exercise_records": [],
                "water_records": [],
                "daily_goals": {
                    "steps": 10000,
                    "water_ml": 2000
                }
            }

    def record_weight(self, weight):
        self.data["weight_records"].append({
            "date": str(datetime.date.today()),
            "weight": weight
        })

    def record_meal(self, meal):
        self.data["meal_records"].append({
            "date": str(datetime.date.today()),
            "meal": meal
        })

    def record_exercise(self, exercise, duration):
        self.data["exercise_records"].append({
            "date": str(datetime.date.today()),
            "exercise": exercise,
            "duration_minutes": duration
        })

    def record_water(self, amount_ml):
        self.data["water_records"].append({
            "date": str(datetime.date.today()),
            "amount_ml": amount_ml
        })

    def calculate_bmi(self, height_meters):
        if not self.data["weight_records"]:
            return None
        latest_weight = self.data["weight_records"][-1]["weight"]
        bmi = latest_weight / (height_meters ** 2)
        return round(bmi, 2)

    def set_daily_goals(self, steps, water_ml):
        self.data["daily_goals"] = {
            "steps": steps,
            "water_ml": water_ml
        }

    def get_water_intake_today(self):
        today = str(datetime.date.today())
        total = sum(entry['amount_ml'] for entry in self.data["water_records"] if entry['date'] == today)
        return total

    def save(self):
        users = load_users()
        users[self.username] = {
            "password": self.password,
            "data": self.data
        }
        save_users(users)

# Health tips
HEALTH_TIPS = [
    "Drink plenty of water.",
    "Get at least 7-8 hours of sleep.",
    "Eat more fruits and vegetables.",
    "Exercise for at least 30 minutes a day.",
    "Take breaks from screens every hour.",
    "Practice deep breathing exercises.",
    "Maintain a regular eating schedule.",
    "Limit sugary drinks and snacks.",
    "Stretch every morning.",
    "Stay socially connected with friends."
]

def get_random_health_tip():
    return random.choice(HEALTH_TIPS)

# Reports
def weekly_report(user):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    print("\n--- Weekly Report ---")
    print("Weight entries:")
    for entry in user.data["weight_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['weight']} kg")

    print("\nExercises:")
    for entry in user.data["exercise_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            print(f"{entry['date']}: {entry['exercise']} for {entry['duration_minutes']} minutes")

    print("\nWater Intake:")
    total_water = 0
    for entry in user.data["water_records"]:
        date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d").date()
        if week_ago <= date <= today:
            total_water += entry['amount_ml']
    print(f"Total water intake in past 7 days: {total_water} ml")

# Plotting

def plot_weight_progress(user):
    dates = [entry['date'] for entry in user.data["weight_records"]]
    weights = [entry['weight'] for entry in user.data["weight_records"]]

    if not dates:
        print("No weight data to plot.")
        return

    plt.figure(figsize=(10,5))
    plt.plot(dates, weights, marker='o')
    plt.title("Weight Progress")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Application logic
def signup():
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    users = load_users()
    if username in users:
        print("Username already exists. Try logging in.")
        return None
    user = User(username, password)
    user.save()
    print("Account created successfully!")
    return user

def login():
    username = input("Username: ")
    password = input("Password: ")
    users = load_users()
    if username in users and users[username]["password"] == password:
        user_data = users[username]["data"]
        user = User(username, password, user_data)
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Invalid credentials.")
        return None

def main_menu(user):
    while True:
        print("\n--- Main Menu ---")
        print("1. Record weight")
        print("2. Record meal")
        print("3. Record exercise")
        print("4. Record water intake")
        print("5. Calculate BMI")
        print("6. Set daily goals")
        print("7. View weekly report")
        print("8. Plot weight progress")
        print("9. Show random health tip")
        print("10. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            weight = float(input("Enter your weight (kg): "))
            user.record_weight(weight)
            user.save()
            print("Weight recorded.")
        elif choice == "2":
            meal = input("Describe your meal: ")
            user.record_meal(meal)
            user.save()
            print("Meal recorded.")
        elif choice == "3":
            exercise = input("Type of exercise: ")
            duration = int(input("Duration (minutes): "))
            user.record_exercise(exercise, duration)
            user.save()
            print("Exercise recorded.")
        elif choice == "4":
            amount = int(input("Amount of water (ml): "))
            user.record_water(amount)
            user.save()
            print("Water intake recorded.")
        elif choice == "5":
            height = float(input("Enter your height in meters: "))
            bmi = user.calculate_bmi(height)
            if bmi:
                print(f"Your BMI is {bmi}")
            else:
                print("No weight records found.")
        elif choice == "6":
            steps = int(input("Set daily steps goal: "))
            water_ml = int(input("Set daily water intake goal (ml): "))
            user.set_daily_goals(steps, water_ml)
            user.save()
            print("Daily goals updated.")
        elif choice == "7":
            weekly_report(user)
        elif choice == "8":
            plot_weight_progress(user)
        elif choice == "9":
            print(get_random_health_tip())
        elif choice == "10":
            print("Logged out successfully.")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point
def main():
    print("Welcome to Health Tracker App!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user = signup()
            if user:
                main_menu(user)
        elif choice == "2":
            user = login()
            if user:
                main_menu(user)
        elif choice == "3":
            print("Thank you for using the Health Tracker App. Stay healthy!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()