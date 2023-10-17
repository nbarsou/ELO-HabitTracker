#!/user/bin/env python3
"""
Author: Nicolás Barrón Sour
Date Created: 09/10/2023
Description: Allows you to track and update your ELO rating as you compete with yourself in daily habit-tracking games, providing a numerical measure of your progress and skill in maintaining these habits.
"""

# Imports
import sqlite3
import climage
from datetime import datetime

# Global Values
numberHabits = 5
elo_deduction = 50  # ELO deduction for each missed day

# Function declarations
def db_innit():
    conn = sqlite3.connect("elo_ratings.db")
    cursor = conn.cursor()

    cursor.execute(
        """
		CREATE TABLE IF NOT EXISTS games (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			player_name TEXT,
			opponent_name TEXT,
			player_result INTEGER,
			game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	"""
    )

    cursor.execute(
        """
		CREATE TABLE IF NOT EXISTS players (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT UNIQUE,
			elo INTEGER
		)
	"""
    )

    conn.commit()
    conn.close()


def calculate_elo_rating(player_rating, opponent_rating, result):
    k = 10  # K-factor, determines how much ratings change after a game
    expected_result = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
    new_rating = player_rating + k * (result - expected_result)
    return round(new_rating)


def record_game(player_name, opponent_name, player_result, game_date=None):
    conn = sqlite3.connect("elo_ratings.db")
    cursor = conn.cursor()

    if game_date is None:
        game_date = datetime.now()

    # Insert the game record into the "games" table with the provided or current timestamp
    cursor.execute(
        "INSERT INTO games (player_name, opponent_name, player_result, game_date) VALUES (?, ?, ?, ?)",
        (player_name, opponent_name, player_result, game_date),
    )

    # Get the ID of the last inserted record
    record_id = cursor.lastrowid

    # Get the current ratings for the players
    cursor.execute("SELECT elo FROM players WHERE name = ?", (player_name,))
    player_rating = cursor.fetchone()[0]

    cursor.execute("SELECT elo FROM players WHERE name = ?", (opponent_name,))
    opponent_rating = cursor.fetchone()[0]

    # Calculate the new ratings
    new_player_rating = calculate_elo_rating(
        player_rating, opponent_rating, player_result
    )
    new_opponent_rating = calculate_elo_rating(
        opponent_rating, player_rating, 1 - player_result
    )

    # Update the ratings in the database
    cursor.execute(
        "UPDATE players SET elo = ? WHERE name = ?", (new_player_rating, player_name)
    )
    cursor.execute(
        "UPDATE players SET elo = ? WHERE name = ?",
        (new_opponent_rating, opponent_name),
    )

    conn.commit()
    conn.close()
    return record_id


def get_player_rating(player_name):
    conn = sqlite3.connect("elo_ratings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT elo FROM players WHERE name = ?", (player_name,))
    rating = cursor.fetchone()[0]

    conn.close()
    return rating


def deductMissingDays():
    conn = sqlite3.connect("elo_ratings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT game_date FROM games ORDER BY game_date DESC LIMIT 1")
    result = cursor.fetchone()

    if not result:
        print("No records found in the games table.")
        return

    last_day = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S.%f")
    elapsed_time = datetime.today() - last_day
    if elapsed_time.days > 1:
        elo_deduction_total = elapsed_time.days * elo_deduction
        new_elo = get_player_rating("NBS") - elo_deduction_total
        print("More than 1 day has passed since the last record.")
        print(
            f"You missed {elapsed_time.days} days. Deducted {elo_deduction_total} ELO."
        )
        print(f"Your new rank is {get_rank_name(new_elo)} with {new_elo}")
    else:
        # Perform other logic when the difference in days is 1 or less
        print(f"{elapsed_time} has passed since the last record.")
        # Your other logic here

    conn.close()


def get_rank_name(elo):
    if elo < 800:
        return "Iron"
    elif elo < 1000:
        return "Bronze"
    elif elo < 1200:
        return "Silver"
    elif elo < 1400:
        return "Gold"
    elif elo < 1600:
        return "Platinum"
    elif elo < 1800:
        return "Diamond"
    elif elo < 2000:
        return "Master"
    elif elo < 2200:
        return "Grandmaster"
    else:
        return "Challenger"


def print_rank(elo):
    if elo < 800:
        output = climage.convert("RankImages/iron.png")
    elif elo < 1000:
        output = climage.convert("RankImages/bronze.png")
    elif elo < 1200:
        output = climage.convert("RankImages/silver.png")
    elif elo < 1400:
        output = climage.convert("RankImages/gold.png")
    elif elo < 1600:
        output = climage.convert("RankImages/platinum.png")
    elif elo < 1800:
        output = climage.convert("RankImages/diamond.png")
    elif elo < 2000:
        output = climage.convert("RankImages/master.png")
    elif elo < 2200:
        output = climage.convert("RankImages/grandmaster.png")
    else:
        output = climage.convert("RankImages/challenger.png")

    print(output)


def main():
    # Initialize the database
    db_innit()

    # Welcome message
    prev_elo = get_player_rating("NBS")
    print(
        f'Hello welcome to ELO habit tracker, your current rank is {get_rank_name(get_player_rating("NBS"))} with {get_player_rating("NBS")}'
    )
    print_rank(get_player_rating("NBS"))

    num_habits = int(input("How many habits did you do:"))

    # Deduct ELO for missed days
    deductMissingDays()

    for _ in range(num_habits):
        # Record a game where you won against yourself
        record_game("NBS", "NBS", 0)

    new_elo = get_player_rating("NBS")

    if prev_elo < new_elo:
        print(f"You won some ELO, your rank is {get_rank_name(new_elo)} with {new_elo}")
    else:
        print(
            f"You lost some ELO, your rank is {get_rank_name(new_elo)} with {new_elo}"
        )

    print_rank(get_player_rating("NBS"))
    exit()


# Main body
if __name__ == "__main__":
    main()
