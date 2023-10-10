# ELO Habit Tracker

---

## Description

The ELO Habit Tracker is a Python script that allows you to track and update your ELO rating as you compete with yourself in daily habit-tracking games. It provides a numerical measure of your progress and skill in maintaining these habits. The ELO rating system is commonly used in chess and other competitive games to assess a player's skill level.

## Features

- **ELO Rating System:** The script uses the ELO rating system to calculate and update your skill level based on your performance in daily habit-tracking games.

- **Database Storage:** All game results and player ratings are stored in a SQLite database (`elo_ratings.db`) for easy retrieval and tracking over time.

- **Rank and Visualization:** The script assigns you a rank based on your ELO rating and displays a corresponding rank image to visualize your progress.

## Requirements

To run this script, you need:

- Python 3.x installed on your computer.

## Installation

1. Clone or download this repository to your local machine.

2. Make sure you have Python 3.x installed.

3. Install the required dependencies:

   ```
   pip install climage
   ```

4. Run the script using the following command:

   ```
   python elo_habit_tracker.py
   ```

## How to Use

1. Upon running the script, it initializes the database and displays your current rank and ELO rating. You need to manualy your name and starting elo to the database. 

2. Enter the number of habits you completed for the day, currently set to 10 a day. 

3. The script records your game results, where you both win and lose against yourself (since you're competing with yourself).

4. Your ELO rating is updated based on your game results.

5. The script will inform you if your ELO rating increased or decreased and display your new rank and rank image.

6. You can continue using the script daily to track your progress in maintaining your habits.

## ELO Rating System

The ELO rating system is widely used in competitive games to measure the relative skill levels of players. In this script:

- The K-factor (rate of change) is set to 10.
- The expected result is calculated based on the difference in ELO ratings between the player and the opponent.
- The new ELO rating is updated according to the game result.

## Ranks and Rank Images

Your ELO rating corresponds to a specific rank, and the script displays a corresponding rank image. Here are the ranks:

- Iron
- Bronze
- Silver
- Gold
- Platinum
- Diamond
- Master
- Grandmaster
- Challenger

Rank images are visual representations of these ranks and are displayed for each rank.

## Credits

This script uses the `climage` library to display rank images. You can find the rank images in the "RankImages" folder.

---

Enjoy tracking your habits and improving your ELO rating with the ELO Habit Tracker!
