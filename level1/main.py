"""
Project:  Number Guessing Game
Level:    1 — Absolute Beginner (Syntax & Basics)
Author:   Amine Bouazzi
Date:     13/11/2026
Repo:     python-journey / level-01-guessing-game
"""
import random

MIN_NUMBER = 1
MAX_NUMBER = 100


# --- Utilities ---------------------------------------------------------------

def random_number() -> int:
    """Return a random integer in [MIN_NUMBER, MAX_NUMBER]."""
    return random.randint(MIN_NUMBER, MAX_NUMBER)


# --- Game logic --------------------------------------------------------------

def check_guess(guess: int, secret: int) -> str:
    """
    Compare guess to secret.

    Returns:
        "correct"   — guess equals secret
        "too high"  — guess > secret
        "too low"   — guess < secret
    """
    if guess == secret:
        return "correct"
    if guess > secret:
        return "too high"
    return "too low"


# --- Presentation ------------------------------------------------------------

def print_intro() -> None:
    """Print the game banner and short rules."""
    print("=" * 44)
    print("   🎯 Guess the Number (1–100)")
    print("   I'm thinking of a number between 1 and 100.")
    print("   Type your guess and I'll tell you if it's high or low.")
    print("=" * 44)


# --- Core --------------------------------------------------------------------

def play_round() -> None:
    """Play one full round: generate secret, loop until correct guess."""
    secret = random_number()
    attempts = 0

    while True:
        raw = input("Your guess: ")
        guess = int(raw)          # validation added in STORY-02
        attempts += 1

        result = check_guess(guess, secret)

        if result == "correct":
            print(f"🎉 Correct! You guessed it in {attempts} attempt(s).")
            return

        print(f"   {result}")


def main() -> None:
    """Entry point for the Number Guessing Game."""

    print_intro()
    play_round()    



if __name__ == "__main__":
    main()