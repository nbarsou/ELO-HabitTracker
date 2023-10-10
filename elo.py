#!/user/bin/env python3
"""
Author: Nicolás Barrón Sour
Date Created: 09/10/2023
Description:  Allows you to track and update your ELO rating as you compete with yourself in daily habit-tracking games, providing a numerical measure of your progress and skill in maintaining these habits.
"""

# Imports
import sqlite3
import climage
# Initialize colorama to enable colored text

# Function declarations
def db_innit():
	conn = sqlite3.connect('elo_ratings.db')
	cursor = conn.cursor()

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS games (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			player_name TEXT,
			opponent_name TEXT,
			player_result INTEGER,
            prev_player_elo INTEGER,
            prev_opponent_elo INTEGER,
            new_player_elo INTEGER,
            new_opponent_elo INTEGET,
			game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	''')

	cursor.execute('''
		CREATE TABLE IF NOT EXISTS players (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT UNIQUE,
			elo INTEGER
		)
	''')

	conn.commit()
	conn.close()

def calculate_elo_rating(player_rating, opponent_rating, result):
    k = 10  # K-factor, determines how much ratings change after a game
    expected_result = 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))
    new_rating = player_rating + k * (result - expected_result)
    return round(new_rating)

def record_game(player_name, opponent_name, player_result):
    conn = sqlite3.connect('elo_ratings.db')
    cursor = conn.cursor()


    # Get the current ratings for the players
    cursor.execute('SELECT elo FROM players WHERE name = ?', (player_name,))
    player_rating = cursor.fetchone()[0]

    cursor.execute('SELECT elo FROM players WHERE name = ?', (opponent_name,))
    opponent_rating = cursor.fetchone()[0]

    # Calculate the new ratings
    new_player_rating = calculate_elo_rating(player_rating, opponent_rating, player_result)
    new_opponent_rating = calculate_elo_rating(opponent_rating, player_rating, 1 - player_result)

    # Insert the game record into the "games" table
    cursor.execute('INSERT INTO games (player_name, opponent_name, player_result, player_elo, opponent_elo) VALUES (?, ?, ?)', (player_name, opponent_name, player_result, get_player_rating(player_name), get_player_rating(opponent_name), new_player_rating, new_opponent_rating))

    # Update the ratings in the database
    cursor.execute('UPDATE players SET elo = ? WHERE name = ?', (new_player_rating, player_name))
    cursor.execute('UPDATE players SET elo = ? WHERE name = ?', (new_opponent_rating, opponent_name))

    conn.commit()
    conn.close()

def get_player_rating(player_name):
    conn = sqlite3.connect('elo_ratings.db')
    cursor = conn.cursor()

    cursor.execute('SELECT elo FROM players WHERE name = ?', (player_name,))
    rating = cursor.fetchone()[0]

    conn.close()
    return rating

def get_rank_name(elo):
    if elo < 800:
        return 'Iron'
    elif elo < 1000:
        return 'Bronze'
    elif elo < 1200:
        return 'Silver'
    elif elo < 1400:
        return 'Gold'
    elif elo < 1600:
        return 'Platinum'
    elif elo < 1800:
        return 'Diamond'
    elif elo < 2000:
        return 'Master'
    elif elo < 2200:
        return 'Grandmaster'
    else:
        return 'Challenger'

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
    # Innitalize the database  
    db_innit();

    # Welcome message
    prev_elo = get_player_rating('NBS')
    print(f'Hello welcome to ELO habit tracker, your current rank is {get_rank_name(get_player_rating("NBS"))} with {get_player_rating("NBS")}')
    print_rank(get_player_rating('NBS'))
    num_habits = int(input("How many habits did you do:"))
    for _ in range(num_habits):
        # Record a game where you won against yourself
        record_game('NBS', 'NBS', 0)

    for _ in range(11 - num_habits):
        # Record a game where you lost against yourself
        record_game('NBS', 'NBS', 1)

    new_elo = get_player_rating('NBS')

    if prev_elo < new_elo:
        print(f'You won some ELO, your rank is {get_rank_name(new_elo)} with {new_elo}')
    else:
        print(f'You lost some ELO, your rank is {get_rank_name(new_elo)} with {new_elo}')
    print_rank(get_player_rating('NBS'))
    exit()

# Main body
if __name__ == '__main__':
	main()


