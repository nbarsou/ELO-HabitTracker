import sqlite3

# Function to initialize the database with values
def init_database():
    conn = sqlite3.connect("elo_ratings.db")
    cursor = conn.cursor()

    # Create tables if they don't exist
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

    # Add "NBS" with an initial ELO of 400
    cursor.execute(
        "INSERT OR REPLACE INTO players (name, elo) VALUES (?, ?)", ("NBS", 400)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_database()
    print("Database initialized with initial values.")
