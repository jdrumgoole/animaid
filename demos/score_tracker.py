#!/usr/bin/env python3
"""Demo: Score Tracker

Demonstrates: HTMLDict reactive updates for key-value data.

Shows how:
- Dict mutations (data["player"] = score) trigger automatic updates
- Using .card() preset for nice visual display
- Real-time game score tracking
"""

import random
import time

from animaid import App, HTMLDict, HTMLString


def main() -> None:
    print("Starting Score Tracker Demo...")
    print("Watch the scores update in real-time!")
    print()

    with App(title="Demo: Score Tracker") as app:
        # Title
        title = HTMLString("Game Score Tracker").bold().xxl()
        app.add(title)

        # Initialize scores
        scores = (
            HTMLDict(
                {
                    "Player 1": 0,
                    "Player 2": 0,
                }
            )
            .card()
            .key_bold()
            .value_color("#1565c0")
        )

        app.add(scores)

        time.sleep(1)

        # Simulate a game with random score updates
        print("Simulating game rounds...")
        print()

        for round_num in range(1, 8):
            # Random player scores
            player = random.choice(["Player 1", "Player 2"])
            points = random.randint(1, 10)

            scores[player] = scores[player] + points  # Triggers automatic update!

            print(f"  Round {round_num}: {player} scores {points} points!")
            p1, p2 = scores["Player 1"], scores["Player 2"]
            print(f"           Current: Player 1: {p1}, Player 2: {p2}")
            time.sleep(0.6)

        print()

        # Determine winner
        p1_score = scores["Player 1"]
        p2_score = scores["Player 2"]

        if p1_score > p2_score:
            winner = "Player 1"
        elif p2_score > p1_score:
            winner = "Player 2"
        else:
            winner = "Tie"

        print(f"Final Score: Player 1: {p1_score}, Player 2: {p2_score}")
        print(f"Winner: {winner}!")

        # Add winner announcement
        if winner != "Tie":
            result = HTMLString(f"{winner} Wins!").success().bold().xl()
        else:
            result = HTMLString("It's a Tie!").info().bold().xl()
        app.add(result)

        print()
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
