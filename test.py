import sqlite3
import unittest
from datetime import datetime, timedelta
from elo import (
    db_innit,
    record_game,
    get_player_rating,
    get_rank_name,
)


class TestEloHabitTracker(unittest.TestCase):
    def setUp(self):
        # Create a temporary SQLite database
        self.conn = sqlite3.connect("elo_ratings.db")
        self.cursor = self.conn.cursor()
        self.elo = self.cursor.execute(
            "SELECT elo FROM players WHERE name = 'NBS'"
        ).fetchone()[0]
        # Initialize the database
        db_innit()

        # Initialize a list to keep track of added records
        self.added_records = []

    def tearDown(self):
        # Clean up: Delete the records added by the test
        for record in self.added_records:
            self.cursor.execute("DELETE FROM games WHERE id = ?", (record,))
        self.cursor.execute(
            "UPDATE players SET elo = ? WHERE name = 'NBS'", (self.elo,)
        )

        self.conn.commit()
        self.conn.close()

    def test_elo_habit_tracker_with_history(self):
        # Simulate habit tracking history with different dates (1 day missed)
        for _ in range(4):
            record_id = record_game("NBS", "NBS", 0)
            self.added_records.append(record_id)  # Track the added record

        # Create a date for the missed day (e.g., one day before today)
        today = datetime.now()
        missed_day = today + timedelta(days=1)
        record_id = record_game("NBS", "NBS", 1, game_date=missed_day)  # Day 4 (Missed)
        self.added_records.append(record_id)  # Track the added record

        # Get and assert the player's current ELO rating and rank
        elo = get_player_rating("NBS")
        rank = get_rank_name(elo)
        expected_elo = get_player_rating("NBS")  # Retrieve the expected ELO
        expected_rank = get_rank_name(expected_elo)
        self.assertEqual(elo, expected_elo)
        self.assertEqual(rank, expected_rank)

    def test_elo_habit_tracker_no_missed_days(self):
        # Simulate habit tracking history (no days missed)
        for _ in range(4):
            record_id = record_game("NBS", "NBS", 0)
            self.added_records.append(record_id)  # Track the added record

        # Get and assert the player's current ELO rating and rank
        elo = get_player_rating("NBS")
        rank = get_rank_name(elo)
        expected_elo = get_player_rating("NBS")  # Retrieve the expected ELO
        expected_rank = get_rank_name(expected_elo)
        self.assertEqual(elo, expected_elo)
        self.assertEqual(rank, expected_rank)


if __name__ == "__main__":
    unittest.main()
