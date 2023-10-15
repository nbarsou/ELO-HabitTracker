import sqlite3


def print_database_contents():
    conn = sqlite3.connect("elo_ratings.db")
    cursor = conn.cursor()

    # Query and print the contents of the "players" table
    print("Players:")
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    for player in players:
        print(f"ID: {player[0]}, Name: {player[1]}, ELO: {player[2]}")

    # Query and print the contents of the "games" table
    print("\nGames:")
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
    for game in games:
        print(
            f"ID: {game[0]}, Player Name: {game[1]}, Opponent Name: {game[2]}, Player Result: {game[3]}, Game Date: {game[4]}"
        )

    conn.close()


if __name__ == "__main__":
    print_database_contents()
